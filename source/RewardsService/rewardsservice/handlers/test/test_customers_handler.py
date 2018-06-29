'''
Created on Jun 28, 2018

@author: ken_green
'''
import json
import unittest

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase, gen_test


class TestCustomerRewards0(AsyncTestCase):
    
    @gen_test
    def test_http_get(self):
        # No customers in database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=z.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
    
    @gen_test
    def test_http_put(self):
        # No customers in database
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'z.foo@bar.com', 'orderTotal': 10000})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
    
    @gen_test
    def test_http_del(self):
        # No customers in database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=z.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass


class TestCustomerRewards1(AsyncTestCase):
    
    @gen_test
    def test_http_post(self):
        # Missing emailAddress
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'orderTotal': 75})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Invalid emailAddress
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foobar.com', 'orderTotal': 75})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Missing orderTotal
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com'})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Invalid orderTotal
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com', 'orderTotal': '75'})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
            # Test response data
            self.assretEqual('', response.body['rewardsTier'])
        except:
            pass
        # < Tier A
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com', 'orderTotal': 75})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('', response.body['rewardsTier'])
        except:
            pass
        # < Tier D <
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'b.foo@bar.com', 'orderTotal': 450})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('D', response.body['rewardsTier'])
        except:
            pass
        # == Tier E
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'c.foo@bar.com', 'orderTotal': 500})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('E', response.body['rewardsTier'])
        except:
            pass
        # > Tier J
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'd.foo@bar.com', 'orderTotal': 1049})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('J', response.body['rewardsTier'])
        except:
            pass
        # < Tier A
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'e.foo@bar.com', 'orderTotal': -75})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('', response.body['rewardsTier'])
        except:
            pass
        # < Tier A <
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'f.foo@bar.com', 'orderTotal': 199.99})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('A', response.body['rewardsTier'])
        except:
            pass
        # Existing customer
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='POST',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com', 'orderTotal': 10000})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        
        
class TestCustomerRewards2(AsyncTestCase):
    
    @gen_test
    def test_http_get(self):
        # All customers from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # One customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=a.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # One customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=b.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # One customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=c.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # One customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=d.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # One customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=e.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # One customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=f.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # Customer not in database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=z.foo@bar.com',
                                          method='GET'
                                          )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass


class TestCustomerRewards3(AsyncTestCase):
    
    @gen_test
    def test_http_put(self):
        # Missing emailAddress
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'orderTotal': 75})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Invalid emailAddress
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foobar.com', 'orderTotal': 75})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Missing orderTotal
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com'})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Invalid orderTotal
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com', 'orderTotal': '75'})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
            # Test response data
            self.assretEqual('', response.body['rewardsTier'])
        except:
            pass
        # < Tier A <
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'a.foo@bar.com', 'orderTotal': 75})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('A', response.body['rewardsTier'])
        except:
            pass
        # == Tier E
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'b.foo@bar.com', 'orderTotal': 50})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('E', response.body['rewardsTier'])
        except:
            pass
        # < Tier F <
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'c.foo@bar.com', 'orderTotal': 175})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('F', response.body['rewardsTier'])
        except:
            pass
        # < Tier H <
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'd.foo@bar.com', 'orderTotal': -150.99})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('H', response.body['rewardsTier'])
        except:
            pass
        # > Tier J
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'e.foo@bar.com', 'orderTotal': 2500})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('J', response.body['rewardsTier'])
        except:
            pass
        # < Tier A
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'f.foo@bar.com', 'orderTotal': -100})
                                           )
            # Test response code
            self.assertEqual(200, response.code)
            # Test response data
            self.assretEqual('', response.body['rewardsTier'])
        except:
            pass
        # New customer
        try:
            client = AsyncHTTPClient()
            response =  yield client.fetch('http://rewardsservice:7050/customers',
                                           method='PUT',
                                           headers={'content-type': 'application/json; charset=utf-8'},
                                           body=json.dumps({'emailAddress': 'z.foo@bar.com', 'orderTotal': 10000})
                                           )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        
        
class TestCustomerRewards4(AsyncTestCase):
    
    @gen_test
    def test_http_delete(self):
        # Missing emailAddress
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Customer not in database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=z.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(400, response.code)
        except:
            pass
        # Delete one customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=a.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # Delete one customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=b.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # Delete one customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=c.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # Delete one customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=d.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # Delete one customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=e.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass
        # Delete one customer from database
        try:
            client = AsyncHTTPClient()
            response = yield client.fetch('http://rewardsservice:7050/customers?emailAddress=f.foo@bar.com',
                                          method='DELETE'
                                          )
            # Test response code
            self.assertEqual(200, response.code)
        except:
            pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()