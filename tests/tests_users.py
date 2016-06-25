from flask_testing import LiveServerTestCase
import requests


class FifteenthNightUserTests(LiveServerTestCase):

    def test_login_invalid_username(self):
        req = requests.post(
            self.login_url, data={"example@test.com", "1234"})
        print(req.content)
        self.assertTrue(False)

    def test_login_invalid_password(self):
        req = requests.post(
            self.login_url, data={"example@example.com", "123"})
        print(req.content)
        self.assertTrue(False)

    def test_login_valid_credentials(self):
        req = requests.post(
            self.login_url, data={"example@example.com", "1234"})
        print(req.content)
        self.assertTrue(False)

    def test_logout_when_logged_in(self):
        s = requests.Session()
        s.post(
            self.login_url, data={"example@example.com", "1234"})
        r = s.get(self.logout_url)
        self.assertFalse(r)

    def test_logout_when_logged_out(self):
        r = requests.get(self.logout_url)
        self.assertFalse(r)

    def test_reset_password_valid_old(self):
        s = requests.Session()
        s.post(
            self.login_url, data={"example@example.com", "1234"})
        r = s.get(self.reset_url)
        self.assertFalse(r)

    def test_reset_password_invalid_old(self):
        s = requests.Session()
        s.post(
            self.login_url, data={"example@example.com", "1234"})
        r = s.get(self.reset_url)
        self.assertFalse(r)

    def test_reset_password_dont_match(self):
        s = requests.Session()
        s.post(
            self.login_url, data={"example@example.com", "1234"})
        r = s.get(self.reset_url)
        self.assertFalse(r)
