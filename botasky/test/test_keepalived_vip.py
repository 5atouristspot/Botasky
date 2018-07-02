import unittest
import requests
import json


class VipExample(unittest.TestCase):
    def test_keepalived_vip_port_fail(self):
        fail_request = requests.get(url='http://192.168.1.116:3621/api/v1000/keepalived/vip',
                                    auth=('da', 'xinxin'),
                                    params={'vip': '192.168.71.11', 'host': '192.168.71.142', 'port': 20, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})
        print(fail_request.url)
        print(fail_request.status_code)

        text_info = eval(json.dumps(fail_request.text))
        print(text_info)

        self.assertEqual(500, fail_request.status_code)
        #self.assertEqual('Unauthorized Access', text_info)

    def test_keepalived_vip_host_fail(self):
        fail_request = requests.get(url='http://192.168.1.116:3621/api/v1000/keepalived/vip',
                                    auth=('da', 'xinxin'),
                                    params={'vip': '192.168.71.11', 'host': '192.168.71.1', 'port': 22, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})

        print(fail_request.url)
        print(fail_request.status_code)

        text_info = eval(json.dumps(fail_request.text))
        print(text_info)

        self.assertEqual(500, fail_request.status_code)
        #self.assertEqual('Unauthorized Access', text_info)

    def test_keepalived_vip_ok(self):
        ok_request = requests.get(url='http://192.168.1.116:3621/api/v1000/keepalived/vip',
                                  auth=('da', 'xinxin'),
                                  params={'vip': '192.168.71.11', 'host': '192.168.71.142', 'port': 22, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})
        print(ok_request.url)
        print(ok_request.status_code)
        text_info = eval(ok_request.text)
        print(text_info)

        self.assertEqual(200, ok_request.status_code)
        self.assertEqual([0, '192.168.71.11\n'], text_info['data'])

    def test_keepalived_vip_fail(self):
        ok_request = requests.get(url='http://192.168.1.116:3621/api/v1000/keepalived/vip',
                                  auth=('da', 'xinxin'),
                                  params={'vip': '192.168.71.12', 'host': '192.168.71.142', 'port': 22, 'muser': 'root', 'mpassword': 'tfkj706tfkj706'})
        print(ok_request.url)
        print(ok_request.status_code)
        text_info = eval(ok_request.text)
        print(text_info)

        self.assertEqual(200, ok_request.status_code)
        self.assertEqual([0, ''], text_info['data'])

if __name__ == '__main__':
    unittest.main()