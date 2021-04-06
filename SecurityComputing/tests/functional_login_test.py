import unittest
import os
import json

from project.app import AppMicroserviceIp
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT

class TestLogin(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
        'Token': ''}
        cls.url = "http://localhost:8080/app_ip"

    @classmethod
    def tearDownClass(cls):
        "tear down test fixtures"
        print('### Tearing down the flask server ###')

    def test_login(self):
        """ Test the response object"""
        params = {'user': 'roce.admi@gmail.com', 'password': '1234'}
        method = "/login"
        get = self.app.post(self.url+method, json=params)
        self.assertEqual(get.status_code, 200)
        data = json.loads(get.get_data())
        self.headers['Token'] = data['data'][0]['token']
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)

    def test_close_session(self):
        """ Test the response object"""
        method = "/close_session"
        get = self.app.get(self.url+method, headers=self.headers)
        self.assertEqual(get.status_code, 200)
        data = json.loads(get.get_data())
        self.assertGreater(len(data), 0) 
        self.assertIsInstance(data, dict)   

if __name__ == '__main__':
    unittest.main()