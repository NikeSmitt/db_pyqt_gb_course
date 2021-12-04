import json
import unittest
import client
from common.variables import ENCODING


class TestClient(unittest.TestCase):

    def test_create_presence_request(self):
        test_message = json.loads(client.create_presence_request().decode(ENCODING))

        test_message['time'] = 1.1

        right_message = {
            'action': 'presence',
            'time': 1.1,
            'type': "status",
            "user": {
                "account_name": 'NightTrain',
                "status": 'Hello there!'
                }
            }

        self.assertEqual(
            json.dumps(test_message).encode(ENCODING),
            json.dumps(right_message).encode(ENCODING)
        )

    def test_process_response_200(self):
        test_data_with_response = json.dumps({"response": 200, "alert": "Привет от сервера"}).encode(ENCODING)


        test_response = client.process_response(test_data_with_response)
        self.assertEqual(test_response, {200: 'Ok'})



    def test_process_responce_400(self):
        test_data_without_response = json.dumps({"response": 400}).encode(ENCODING)

        test_response = client.process_response(test_data_without_response)
        self.assertEqual(test_response, {400: 'Error'})


if __name__ == "__main__":
    unittest.main()
