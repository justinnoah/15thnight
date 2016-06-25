import requests

from _15thnight.models import Alert, User

from .base import FifteenthNightTestBase


class AlertTests(FifteenthNightTestBase):

    def test_create_alert_as_admin(self):
        alert_data = {

        }

        s = requests.Session()
        s.post()
        self.assertTrue(False)

    def test_create_alert_as_advocatie(self):
        alert_data = {

        }
        self.assertTrue(False)

    def test_create_alert_as_provider(self):
        alert_data = {

        }
        self.assertTrue(False)

    def test_create_alert_duplicate_data(self):
        self.assertTrue(False)

    def test_create_alert_logged_out(self):
        self.assertTrue(False)

    def test_create_alert_with_bad_data(self):
        self.assertTrue(False)

    def test_get_alerts_as_admin(self):
        self.assertTrue(False)

    def test_get_alerts_as_advocate(self):
        self.assertTrue(False)

    def test_get_alerts_as_provider(self):
        self.assertTrue(False)

    def test_get_alerts_logged_out(self):
        self.assertTrue(False)

    def test_update_alert_as_admin(self):
        self.assertTrue(False)

    def test_update_alert_as_advocate(self):
        self.assertTrue(False)

    def test_update_alert_as_provider(self):
        self.assertTrue(False)

    def test_update_alert_logged_out(self):
        self.assertTrue(False)

    def test_delete_alert_as_admin(self):
        self.assertTrue(False)

    def test_delete_alert_as_advocate(self):
        self.assertTrue(False)

    def test_delete_alert_as_provider(self):
        self.assertTrue(False)

    def test_delete_alert_with_invalid_id(self):
        self.assertTrue(False)

    def test_delete_alert__with_valid_id_logged_out(self):
        self.assertTrue(False)
