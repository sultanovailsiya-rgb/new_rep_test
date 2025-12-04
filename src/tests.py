import unittest
# src/tests.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import app as tested_app
import json

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_get_hello_endpoint(self):
        r = self.app.get('/')
        self.assertEqual(r.data, b'Hello World!')

    def test_post_hello_endpoint(self):
        r = self.app.post('/')
        self.assertEqual(r.status_code, 405)

    def test_get_api_endpoint(self):
        r = self.app.get('/api')
        self.assertEqual(r.json, {'status': 'test'})

    def test_correct_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'name': 'Den', 'age': 100}))
        self.assertEqual(r.json, {'status': 'OK'})
        self.assertEqual(r.status_code, 200)

        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'name': 'Den'}))
        self.assertEqual(r.json, {'status': 'OK'})
        self.assertEqual(r.status_code, 200)

    def test_not_dict_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps([{'name': 'Den'}]))
        self.assertEqual(r.json, {'status': 'bad input'})
        self.assertEqual(r.status_code, 400)

    def test_no_name_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'age': 100}))
        self.assertEqual(r.json, {'status': 'bad input'})
        self.assertEqual(r.status_code, 400)

    def test_bad_age_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'name': 'Den', 'age': '100'}))
        self.assertEqual(r.json, {'status': 'bad input'})
        self.assertEqual(r.status_code, 400)

    def test_add_success(self):
        r = self.app.get('/add?a=2&b=3')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, b'5.0')

    def test_max_number_valide(self):
        r = self.app.get('/max_number?a=10&b=5')
        self.assertEqual(r.data, b'10')
        
    def test_max_number_not_valid(self):
        r = self.app.get('/max_number?a=abc&b=5')
        self.assertEqual(r.data, b'a \xd0\xb8 b - \xd0\x9d\xd0\x95 \xd1\x87\xd0\xb8\xd1\x81\xd0\xbb\xd0\xb0')

if __name__ == '__main__':
    unittest.main()
