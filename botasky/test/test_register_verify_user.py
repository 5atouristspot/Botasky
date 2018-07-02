import unittest
import requests
import json

#http://192.168.1.116:3621/api/v1000/verify?username=da&password=xinxin
#http://192.168.1.116:3621/api/v1000/register?username=da&password=xinxin

class RegisterVerifyExample(unittest.TestCase):
    '''test Register and Verify user '''

    def test_register_user_fail(self):
        fail_request = requests.get(url='http://192.168.1.105:3621/api/v1000/register',
                                    params={'username': 'da', 'password': 'xinxin'})
        print(fail_request.url)
        print(fail_request.status_code)

        #text to type dic
        text_info = eval(fail_request.text)
        print(text_info["status"])

        self.assertEqual(200, fail_request.status_code)
        self.assertEqual('[FAIL]', text_info['status'])
        #self.assertIn('FAIL', text_info['status'])

    '''
    def test_register_user_ok(self):
        fail_request = requests.get(url='http://192.168.1.105:3621/api/v1000/register',
                                    params={'username': 'da', 'password': 'xinxin'})
        print(fail_request.url)
        print(fail_request.status_code)

        #text to type dic
        text_info = eval(fail_request.text)
        print(text_info["status"])

        self.assertEqual(200, fail_request.status_code)
        self.assertEqual('[OK]', text_info['status'])
        #self.assertIn('FAIL', text_info['status'])
    '''

    def test_verify_user_fail(self):
        fail_request = requests.get(url='http://192.168.1.105:3621/api/v1000/resource',
                                    auth=('da','xinxi'))
        print(fail_request.url)
        print(fail_request.status_code)

        text_info = eval(json.dumps(fail_request.text))
        print(text_info)

        self.assertEqual(401, fail_request.status_code)
        self.assertEqual('Unauthorized Access', text_info)

    def test_verify_user_ok(self):
        ok_request = requests.get(url='http://192.168.1.105:3621/api/v1000/resource',
                                  auth=('da', 'xinxin'))

        print(ok_request.url)
        print(ok_request.status_code)

        text_info = eval(ok_request.text)
        print(text_info)

        self.assertEqual(200, ok_request.status_code)
        self.assertEqual('Hello', text_info['data'])

if __name__ == '__main__':
    unittest.main()
