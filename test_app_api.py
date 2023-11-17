import pytest
import app_api as app_api
from models import *
import unittest
import os
import json

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

        self.new_actor = os.environ['NEW_ACTOR_UNITTEST']
        self.new_movie = os.environ['NEW_MOVIE_UNITTEST']
        self.new_showing = os.environ['NEW_SHOWING_UNITTEST']

    def tearDown(self):
        pass

#   NOTE 1: Uncomment any of the 3 test blocks below to run the tests for the grouped endpoints
#   NOTE 2: Remember to change the ID values after running the delete tests
#   NOTE 3: Delete tests will fail if a foreign key is still referenced in a child table 

#  ----------------------------------------------------------------
#   TEST BLOCK: ACTORS ENDPOINTS
#  ----------------------------------------------------------------


    #testcase 1: test actors() == success
    def test_actors(self):
        response = app.test_client().get("/actors")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])
        self.assertTrue(len(data["actors"]))
    
    #testcase 2: test actors() == error
    def test_actors_404_error(self):
        response = app.test_client().get("/actorss")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")


    #testcase 3: test show_actor() == success
    def test_show_actor(self):
        response = app.test_client().get("/actors/75")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_actor_id"], 75)
        self.assertTrue(len(data['actor_details']))

    
    #testcase 4: test show_actor() == error
    def test_show_actor_404_error(self):
        response = app.test_client().get("/actors/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
    
    #testcase 5: test create_actor_form() == success
    def test_create_actor_form(self):
        response = app.test_client().get("/actors/create")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["get_form"], True)
    
    #testcase 6: test create_actor_submission() == success
    def test_create_actor_submission(self):
        new_actor_json = json.loads(self.new_actor)
        response = app.test_client().post("/actors/create", json=new_actor_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])
        self.assertTrue(data["created_actor_name"])
    
    #testcase 7: test create_actor_submission() == error, wrong URL, 400; bad request
    def test_create_actor_submission_404_error(self):
        response = app.test_client().post("/actors/create/data")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
    
    #testcase 8: test edit_actor_form() == success
    def test_edit_actor_form(self):
        response = app.test_client().get("/actors/77/edit")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["get_form"], True)
        self.assertEqual(data["actor_id"], 77)
    
    #testcase 9: test edit_actor_submission() == success
    def test_edit_actor_submission(self):
        new_actor_json = json.loads(self.new_actor)
        response = app.test_client().post("/actors/1/edit", json=new_actor_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["actor_id"], 1) 

    #testcase 10: test edit_actor_submission() == error, wrong URL, 404; resource not found
    def test_edit_actor_submission_404_error(self):
        response = app.test_client().post("/actors/10000/edit")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
    
    #testcase 11: test delete_actor() == success
    def test_delete_actor(self):
        response = app.test_client().get("/actors/67/delete")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_actor_id"], 67)
        self.assertTrue(data["total_actors"])

    #testcase 12: test delete_actor() == error, wrong URL, 404; resource not found
    def test_delete_actor_404_error(self):
        response = app.test_client().get("/actors/44000/delete")
        print('***HAPAAA')
        print(response)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        
    


#  ----------------------------------------------------------------
#  TEST BLOCK: MOVIES ENDPOINTS
#  ----------------------------------------------------------------

    """
    #testcase 1: test movies() == success
    def test_movies(self):
        response = app.test_client().get("/movies")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])

    #testcase 2: test movies() == error, wrong url
    def test_movies_404_error(self):
        response = app.test_client().get("/moviessss")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")


    #testcase 3: test show_movie() == success
    def test_show_movie(self):
        response = app.test_client().get("/movies/3")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_movie"], 3)


    #testcase 4: test show_movie() == error
    def test_show_movie_404_error(self):
        response = app.test_client().get("/movies/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    #testcase 5: test create_movie_form() == success
    def test_create_movie_form(self):
        response = app.test_client().get("/movies/create")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["get_form"], True)

    #testcase 6: test create_movie_submission() == success
    def test_create_movie_submission(self):
        new_movie_json = json.loads(self.new_movie)
        response = app.test_client().post("/movies/create", json=new_movie_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])
        self.assertTrue(data["new_movie_name"])

    #testcase 7: test create_movies_submission() == error, wrong URL, 404
    def test_create_movie_submission_404_error(self):
        response = app.test_client().post("/movies/create/data")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    #testcase 8: test edit_movie_form() == success
    def test_edit_movie_form(self):
        response = app.test_client().get("/movies/4/edit")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["get_form"], True)
        self.assertEqual(data["movie_id"], 4)

    #testcase 9: test edit_movie_submission() == success
    def test_edit_movie_submission(self):
        new_movie_json = json.loads(self.new_movie)
        response = app.test_client().post("/movies/3/edit", json=new_movie_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["movie_id"], 3)

    #testcase 10: test edit_movie_submission() == error, wrong URL, 404; resource not found
    def test_edit_movie_submission_404_error(self):
        response = app.test_client().post("/movie/10000/edit")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    #testcase 11: test delete_movie() == success
    def test_delete_movie(self):
        response = app.test_client().delete("/movies/10/delete")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_movie_id"], 10)
        self.assertTrue(data["total_movies"])

    #testcase 12: test delete_movie() == error, wrong URL, 404; resource not found
    def test_delete_movie_404_error(self):
        response = app.test_client().delete("/movies/44000/delete/nothing")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found") 
        
    """

#  ----------------------------------------------------------------
#  TEST BLOCK: SHOWINGS ENDPOINTS
#  ----------------------------------------------------------------

    """
    #testcase 1: test showings() == success
    def test_showings(self):
        response = app.test_client().get("/showings")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_showings"])

    #testcase 2: test showings() == error, wrong url
    def test_showings_404_error(self):
        response = app.test_client().get("/showingsssssss")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    
    #testcase 3: test create_showing_submission() == success
    def test_create_showing_submission(self):
        new_showing_json = json.loads(self.new_showing)
        response = app.test_client().post("/showings/create", json=new_showing_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_showings"])
        self.assertTrue(data["showing_lead_actor_id"])


    #testcase 4: test create_showing_submission() == error, wrong URL, 404
    def test_create_showing_submission_404_error(self):
        response = app.test_client().post("/showings/create/dataaaaaa")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    """
    
    
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

