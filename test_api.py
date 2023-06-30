import unittest
from flask import Flask
import app

class SudokuAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_start(self):
        response = self.app.get('/start')
        self.assertEqual(response.status_code, 200)
   
    def test_move_valid(self):
        data = {
            'row': 0,
            'column': 0,
            'value': 5
        }
        response = self.app.post('/move', data=data)
        self.assertEqual(response.status_code, 200)
   

    def test_move_invalid(self):
        data = {
            'row': 0,
            'column': 0,
            'value': 9
        }
        response = self.app.post('/move', data=data)
        self.assertEqual(response.status_code, 200)
    

if __name__ == '__main__':
    unittest.main()

