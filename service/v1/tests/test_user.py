import json
import unittest
from wsgi import app


create_url = "/myservice/v1/user/createuser"
auth_token_url = "/myservice/v1/user/authtoken"
refresh_token_url = "/myservice/v1/user/refresh-token"
logout_url = "/myservice/v1/user/logout"
user_details_url = "/myservice/v1/user/userdetails"


class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_create_user_existing_success(self):
        """
        Test case for checking existing user
        """
        payload = {"email": "narsimha@gmail.com", "password": "123456"}
        res = self.client.post(create_url, json=payload)
        assert res.status_code == 200
        assert json.loads(res.data) == {'message': 'User email already registered'}

    def test_create_user_missing_params(self):
        """
        Test case for create_user with missing parameters
        """
        payload = {"email": "sunny@gmail.com"}
        res = self.client.post(create_url, json=payload)
        assert res.status_code == 400
        assert json.loads(res.data) == {'message': "{'password': ['Missing data for required field.']}"}

    def test_create_user_empty_params(self):
        """
        Test case for create_user with empty parameters
        """
        payload = {}
        res = self.client.post(create_url, json=payload)
        assert res.status_code == 400

    def test_auth_token_user_success(self):
        """
        Test case for authentication token for user
        """
        url = f"{auth_token_url}?email=chintu@gmail.com&password=Chintu1443"
        res = self.client.post(url)
        assert res.status_code == 200
        assert 'token' in json.loads(res.data)

    def test_auth_token_user_invalid_params(self):
        """
        Test case for authentication token with invalid parameters
        """
        url = f"{auth_token_url}?email=sunny_1@gmail.com"
        res = self.client.post(url)
        assert res.status_code == 400
        assert json.loads(res.data) == {'message': 'Invalid Credential'}


    def test_refresh_token_success(self):
        """
        Test case for refreshing authorization token
        """
        auth_url = "/myservice/v1/user/authtoken?email={}&password={}".format("chintu@gmail.com", "Chintu1443")
        token_resp = json.loads(self.client.post(auth_url).data)
        print(token_resp)
        refresh_token_url = "/myservice/v1/user/refresh-token"  
        headers = {"x-refresh-tokens": token_resp['refresh']}  
        res = self.client.post(refresh_token_url, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('token', data)
        self.assertIsInstance(data['token'], str)



    def test_refresh_token_missing_token(self):
        """
        Test case for refreshing authorization token with missing token
        """
        headers = {}
        res = self.client.post(refresh_token_url, headers=headers)
        print(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data), {'message': 'Missing refresh token'})

    def test_refresh_token_invalid_token(self):
        """
        Test case for refreshing authorization token with invalid token
        """
        headers = {"x-refresh-tokens": "invalid_refresh_token"}
        res = self.client.post(refresh_token_url, headers=headers)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(json.loads(res.data), {'message': 'Invalid refresh token'})

    def test_user_details_success(self):
        """
        Test case for checking user details
        """
        url = "/myservice/v1/user/authtoken?email={}&password={}".format("chintu@gmail.com", "Chintu1443")
        token_resp = json.loads(self.client.get(url).data)
        headers = {"x-access-tokens": token_resp}
        res = self.client.get(user_details_url, headers=headers)
        assert res.status_code == 200

    def test_user_details_invalid_token(self):
        """
        Test case for user_details with invalid token
        """
        # auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE1ODgxNTU4ODd9.5-S32oT8HxZyYvmfRG6BCzsb1KfkXyQVGIGeFM64wP8"
        headers = {"x-access-tokens": "invalid_access_token"}
        res = self.client.get(user_details_url, headers=headers)
        assert res.status_code == 200
        assert json.loads(res.data) == {"message": "Invalid access token"}


    def test_user_details_without_token(self):
        """
        Test case for user_details without token
        """
        headers = {}
        res = self.client.get(user_details_url, headers=headers)
        assert res.status_code == 200
        assert json.loads(res.data) == {"message": "Access token is missing"}

    def test_user_logout_success(self):
        """
        Test case for logging out user and blacklisting token
        """
        url = f"{auth_token_url}?email=chintu@gmail.com&password=Chintu1443"
        token_resp = json.loads(self.client.post(url).data)
        access_token = token_resp["token"]
        headers = {"x-access-tokens":access_token }
        res = self.client.post(logout_url, headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data),{'message': 'User logged out successfully'})

    def test_user_logout_invalid_token(self):
        """
        Test case for logging out user with invalid token
        """
        headers = {"x-access-tokens": "Invalid token"}
        res = self.client.post(logout_url, headers=headers)
        print(res)
        assert res.status_code == 200
        assert json.loads(res.data) == {"message": "Invalid access token"}


