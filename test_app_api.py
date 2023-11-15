import app_api as app_api
from models import *
import json
import unittest


# _______________________________________
# Class-based Tests
# ________________________________________

class TestCastingAgencyMethods(unittest.TestCase):

    #@pytest.mark.skip(reason="this feature is broken") # to skip a test
    def setUp(self):
        app = Flask(__name__) #in app.py = OK
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL_TEST']
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy(app) #in models.py = OK
        db.init_app(app)


    def tearDown(self):
        pass


    #@pytest.mark.xfail(reason="cannot get actors at the moment") # if you expect it to fail
    def test_actors(self):
        response = app.test_client().get("/actors")
        print(response.status)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

