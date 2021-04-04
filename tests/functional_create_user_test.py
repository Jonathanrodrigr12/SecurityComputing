import unittest
import os
import json

from project.app import AppMicroserviceIp
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT

class TestCreateUser(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    METHOD = "/create_user"
    @classmethod
    def setUpClass(cls):
        "set up test fixtures"
        print('### Setting up flask server ###')
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(cls.BASE_DIR,
                                                              "config.yml")
        app_service = AppMicroserviceIp(path="project")
        app_service.reload_conf()
        app = app_service.create_app()
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.headers = {'Content-Type': 'application/json', 'User-Id': "asd",
        'Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc1NDc0NTEsInZhbCI6InJvY2UuYWRtaUBnbWFpbC5jb20ifQ.7F8Zgta-jRYfpy4-kG-HFvEXfXDwuE5PheOnL12aPAk'}
        cls.url = "http://localhost:8080/app_ip"

    @classmethod
    def tearDownClass(cls):
        "tear down test fixtures"
        print('### Tearing down the flask server ###')

    def test_create_user_with_user_used(self):
        """ Test the response object"""
        params = {'email': 'roce.admi@gmail.com', 'password': '1234'}
        get = self.app.post(self.url+self.METHOD, json=params)
        self.assertEqual(get.status_code, 400)
        data = json.loads(get.get_data())
        self.assertGreater(len(data), 0)  

    def test_create_user_with_new_user(self):
        """ Test the response object"""
        params = {'email': 'jonathan.admi@gmail.co', 'password': '1234'}
        get = self.app.post(self.url+self.METHOD, json=params, headers=self.headers)
        self.assertEqual(get.status_code, 200)
        data = json.loads(get.get_data())
        self.assertGreater(len(data), 0)

    def test_create_user_without_user(self):
        """ Test the response object"""
        params = {'email': 'jonathan.admi@gmail.co', 'password': '1234'}
        get = self.app.post(self.url+self.METHOD, json=params)
        self.assertEqual(get.status_code, 400)
        data = json.loads(get.get_data())
        self.assertGreater(len(data), 0)     

if __name__ == '__main__':
    unittest.main()