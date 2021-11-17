import json

import server
import unittest

from common.variables import ENCODING


class TestServer(unittest.TestCase):

    def test_create_server_response(self):
        test_response = server.create_server_response()
        right_response = json.dumps({"response": 200, "alert": "Привет от сервера"}).encode(ENCODING)

        self.assertEqual(test_response, right_response)



if __name__ == "__main__":
    unittest.main()
