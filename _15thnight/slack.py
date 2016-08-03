from slackclient import SlackClient as SC

from _15thnight.models import Alert, Category, SlackMessage, User

try:
    from config import HOST_NAME
except:
    from configdist import HOST_NAME


class SlackChannels(object):
    # A set of (channel name, channel id) tuples
    __channels = dict()

    def __init__(self, token):
        """Requires a user with channel:write."""
        self.sc = SC(token)

    def add_existing_channels(self):
        existing_categories = list(c.name for c in Category.all())
        for category in existing_categories:
            self.add_channel(category)

    def add_channel(self, category):
        """Listen to or create new channel called `category`."""

        # Slack only deals in lowercase
        category = category.lower()

        live_channels = self.sc.api_call("channels.list").get("channels")
        if live_channels:
            existing_channels = dict({
                ch["name"]: ch["id"] for ch in live_channels
            })
        else:
            existing_channels = dict()

        if category in existing_channels.keys():
            self.__channels[category] = existing_channels[category]
        else:
            # TODO: Create channel
            print("CREATE CHANNEL: %s" % category)
            res = self.sc.api_call("channels.join", name=category)
            print("%s:\n%s" % (category, res))
            if res["ok"]:
                self.__channels[category] = res["channel"]["id"]

    def remove_channel(self, category):
        """Create a new channel or join existing for the new category."""
        if category in self.__channels.keys():
            # TODO: Delete channel
            del self.__channels[category]

    @property
    def channels(self):
        return self.__channels.keys()


class SlackBot(object):
    """Slackbot connection."""

    def __init__(self, bot_token, user_token):
        """Requires a bot user for rtm."""
        self.sc = SC(bot_token)
        self.categories = SlackChannels(user_token)

    def add_category(self, name):
        """Add channel method for adding and creating new channels."""
        self.categories.add_channel(name)

    def remove_category(self, name):
        self.categories.remove_channel(name)

    def send_message(self, alert):
        """Send message to users in approprate channels."""
        alert_id = alert.id
        url = "%s/respond_to/%s" % (HOST_NAME, alert_id)

        pm_alert = (
            "*Alert ID:* %s\n"
            "*Date/Time:* %s\n"
            "*Gender:* %s | *Age:* %s | *Needs:* %s\n"
            "*Description:* %s\n\n"
            "To reply via the web, click: %s\n\n"
            "If you are able to help, respond with *%s* followed by a message."
            "\nDon't forget to include your *name* and *phone number* or *emai"
            "l*.\nExamples:\n"
            "%s I can help this child. Call me, John, at 555-555-5555\n"
            "%s I, Jane, am able to help. I can be reached via email at "
            "jane.doe@example.com"
        ) % (alert_id, alert.created_at.strftime('%m/%d/%y %I:%M%p'),
             alert.gender, alert.age, alert.get_needs(), alert.description,
             url, alert_id, alert_id, alert_id)

        member_set = set()
        # Verify the channel id has been found
        for category in alert.categories:
            channel_id = self.categories.channels.get(category.lower())
            if channel_id:
                members = self.sc.api_call(
                    "channels.info", channel=channel_id
                )["channel"].get("members", [])

                for member in members:
                    member_set.add(member)

        for member in member_set:
            ok = self.sc.api_call("im.open", user=member)
            if ok["ok"]:
                im_id = ok["channel"]["id"]
                res = self.sc.api_call(
                    "chat.postMessage", channel=im_id, text=pm_alert)
                if res["ok"]:
                    sm = SlackMessage(
                        channel=im_id, timestamp=res["ts"], alert_id=alert_id)
                    sm.save()

    def accept_response(self, msg, alert_id):
        """
        Given a valid message, do the things necessary to accept the alert.

        First, check that the message was sent to the user, and the alert still
        needs a response, then do things.
        """
        channel = msg.get('channel')
        # This print statement is for the celery log
        print(
            "Check the DB for channel: %s, and alert: %s" %
            (channel, alert_id)
        )

        valid = SlackMessage.get_valid_message(alert_id, channel)
        if valid:
            slack_email = "slackuser@example.com"
            slack_user = User.query.filter_by(email=slack_email).first()
            if not slack_user:
                print(
                    "Unable to find the slack user, "
                    "was the app setup correctly?"
                )
            else:
                from _15thnight.core import respond_to_alert
                respond_to_alert(alert_id, msg.get("text"), slack_user, True)
