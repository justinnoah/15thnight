import urlparse

from flask_testing import LiveServerTestCase

from _15thnight.database import Model
from _15thnight.models import User


class FifteenthNightTestBase(LiveServerTestCase):

    def create_app(self):
        from _15thnight import create_app
        app = create_app(True)
        return app

    def setUp(self):
        from _15thnight.database import Model, connect_to_db
        connect_to_db(self.app.config["DATABASE_URL"])
        Model.metadata.create_all(bind=Model.db_session.get_bind())

        # Useful URLs for testing
        self.test_url = self.app.config["HOST_NAME"]
        self.login_url = urlparse.urljoin(self.test_url, "/login")
        self.logout_url = urlparse.urljoin(self.test_url, "/logout")
        self.reset_url = urlparse.urljoin(self.test_url, "/reset")

        # Admin User
        User(
            'admin@example.com', '1234', '5415551234', None, None,
            None, None, 'admin'
        ).save()
        self.user_admin = User.get(email="admin@example.com").first()
        # Advocate User
        User(
            'advocate@example.com', '1234', '5415551234', None, None,
            None, None, 'advocate'
        ).save()
        self.user_advocate = User.get(email="advocate@example.com").first()
        # Provider User
        User(
            'Provider@example.com', '1234', '5415551234', None, None,
            None, None, 'provider'
        ).save()
        self.user_advocate = User.get(email="provider@example.com").first()

    def tearDown(self):
        Model.metadata.drop_all()
