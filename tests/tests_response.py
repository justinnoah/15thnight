from flask_testing import LiveServerTestCase


class FifteenthNightResponseTests(LiveServerTestCase):

    def create_app(self):
        from _15thnight import create_app
        app = create_app(True)
        return app

    def setUp(self):
        from _15thnight.database import Model, connect_to_db
        connect_to_db(self.app.config["DATABASE_URL"])
        Model.metadata.create_all(bind=Model.db_session.get_bind())

    def test_get_responses_zero_resoponses(self):
        self.assertTrue(False)

    def test_get_responses_some_resoponses(self):
        self.assertTrue(False)

    def test_create_response_valid(self):
        self.assertTrue(False)

    def test_create_response_invalid_keys(self):
        self.assertTrue(False)

    def test_create_response_invalid_data(self):
        self.assertTrue(False)

    def test_create_response_duplicates(self):
        self.assertTrue(False)

    def test_delete_response_valid_uuid(self):
        self.assertTrue(False)

    def test_delete_response_invalid_uuid(self):
        self.assertTrue(False)

    def test_update_response_valid_uuid_valid_data(self):
        self.assertTrue(False)

    def test_update_response_valid_uuid_invalid_data(self):
        self.assertTrue(False)

    def test_update_response_invalid_uuid(self):
        self.assertTrue(False)
