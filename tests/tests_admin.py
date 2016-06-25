from flask_testing import LiveServerTestCase


class FifteenthNightAdminTests(LiveServerTestCase):

    def create_app(self):
        from _15thnight import create_app
        app = create_app(True)
        return app

    def setUp(self):
        from _15thnight.database import Model, connect_to_db
        connect_to_db(self.app.config["DATABASE_URL"])
        Model.metadata.create_all(bind=Model.db_session.get_bind())

    def test_admin(self):
        self.assertTrue(False)
