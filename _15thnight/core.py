from _15thnight.queue import queue_send_alert
from _15thnight.email_client import send_email
from _15thnight.models import Response
from _15thnight.twilio_client import send_sms


def send_out_alert(alert_form, user):
    """
    Send out an alert to providers.
    """
    kwargs = dict({
        "alert_form": alert_form,
        "user": user,
    })
    queue_send_alert.apply_async(kwargs, countdown=0)


def respond_to_alert(provider, message, alert):
    """
    Send a response from a provider to an advocate.
    """
    advocate = alert.user

    response_message = "%s" % provider.email
    if provider.phone_number:
        response_message += ", %s" % provider.phone_number

    response_message += " is availble for: "
    available = dict(
        shelter=provider.shelter,
        clothes=provider.clothes,
        food=provider.food,
        other=provider.other
    )

    response_message += "%s" % ", ".join(k for k, v in available.items() if v)
    response_message += " Message: " + response_message

    if advocate.phone_number:
        send_sms(
            alert.user,
            response_message
        )

    send_email(
        to=advocate.email,
        subject='Alert Response',
        body=response_message
    )

    response = Response(user=provider, alert=alert, message=message)
    response.save()
    return response
