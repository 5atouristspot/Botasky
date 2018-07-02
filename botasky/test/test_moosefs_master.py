import unittest
import requests
import json

class MosefsMasterExample(unittest.TestCase):
    def test_moosefs_master_port_fail(self):
        fail_request = requests.get(url='http://192.168.1.116:3621/api/v1000/moosefs/master',
                                    auth=('da', 'xinxin'),
                                    params={'host': '192.168.71.142', 'port': 20, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})
        print(fail_request.url)
        print(fail_request.status_code)

        text_info = eval(json.dumps(fail_request.text))
        print(text_info)

        self.assertEqual(500, fail_request.status_code)
        #self.assertEqual('Unauthorized Access', text_info)

    def test_moosefs_master_host_fail(self):
        fail_request = requests.get(url='http://192.168.1.116:3621/api/v1000/moosefs/master',
                                    auth=('da', 'xinxin'),
                                    params={'host': '192.168.71.11', 'port': 22, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})

        print(fail_request.url)
        print(fail_request.status_code)

        text_info = eval(json.dumps(fail_request.text))
        print(text_info)

        self.assertEqual(500, fail_request.status_code)
        #self.assertEqual('Unauthorized Access', text_info)


    def test_moosefs_master_ok(self):
        ok_request = requests.get(url='http://192.168.1.116:3621/api/v1000/moosefs/master',
                                  auth=('da', 'xinxin'),
                                  params={'host': '192.168.71.142', 'port': 22, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})
        print(ok_request.url)
        print(ok_request.status_code)
        text_info = eval(ok_request.text)
        print(text_info)

        self.assertEqual(200, ok_request.status_code)
        self.assertEqual([0, '0\n'], text_info['data'])

if __name__ == '__main__':
    unittest.main()