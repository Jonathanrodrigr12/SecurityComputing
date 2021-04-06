import unittest
import os
import json

from project.app import AppMicroserviceIp
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT

class TestAppIp(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IP_EXAMPLE = "83.44.196.93"
    COUNTRY = "España"
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
        'Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTc1ODc5NjQsInZhbCI6InJvY2UuYWRtaUBnbWFpbC5jb20ifQ.1Ro-wlFYLL9FtG-iEKzNqg_90L58wORVb4jwvG1Ev18'}
        cls.url = "http://localhost:8080/app_ip"

    @classmethod
    def tearDownClass(cls):
        "tear down test fixtures"
        print('### Tearing down the flask server ###')

    def test_get_ip(self):
        """ Test the response object"""
        method = "/get_ip?ip={}"\
                 .format(self.IP_EXAMPLE)
        get = self.app.get(self.url+method, headers=self.headers)
        self.assertEqual(get.status_code, 200)
        data = json.loads(get.get_data())
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data, dict)

    def test_get_country(self):
        """ Test the response object"""
        method = "/get_country?name={}"\
            .format(self.COUNTRY)
        get = self.app.get(self.url+method, headers=self.headers)
        self.assertEqual(get.status_code, 200)
        data = json.loads(get.get_data())
        self.assertGreater(len(data), 0) 
        self.assertIsInstance(data, dict)   

if __name__ == '__main__':
    unittest.main()