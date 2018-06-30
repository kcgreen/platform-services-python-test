'''
Created on Jun 28, 2018

@author: ken_green
'''
import json
import logging
import math
import re
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

logger = logging.getLogger('tornado.application')

class CustomersHandler(tornado.web.RequestHandler):

    def initialize(self):
        # Create db client
        self.client = MongoClient('mongodb', 27017)

    def prepare(self):
        # Incorporate request JSON into arguments dictionary
        if self.request.body:
            try:
                self.json_data = json.loads(str(self.request.body, encoding='utf-8'))
            except ValueError:
                message = 'ARGERROR: Unable to parse JSON.'
                return self.send_error(400, message=message) # Bad request data
        
    def on_finish(self):
        # Close db client
        self.client.close()

    # post
    # expects: email address, order total as JSON payload data
    # returns: new customer rewards profile
    @coroutine
    def post(self):
        try:
            # Get payload data and validate
            if 'emailAddress' in self.json_data:
                email_address = self.json_data['emailAddress']
                if not is_email_address(email_address):
                    message = 'ARGERROR: emailAddress not email address.'
                    logger.warn(message)
                    return self.send_error(400, message=message) # return 400 when invalid
            else:
                message = 'ARGERROR: Missing JSON argument: emailAddress.'
                logger.warn(message)
                return self.send_error(400, message=message) # return 400 when missing
            if 'orderTotal' in self.json_data:
                try:
                    if str(self.json_data['orderTotal']).lower() in ('nan', 'inf'):
                        raise ValueError
                    order_total = float(self.json_data['orderTotal'])
                except ValueError:
                    message = 'ARGERROR: orderTotal not number.'
                    logger.warn(message)
                    return self.send_error(400, message=message) # return 400 when invalid
            else:
                message = 'ARGERROR: Missing JSON argument: orderTotal.'
                logger.warn(message)
                return self.send_error(400, message=message) # return 400 when missing
                
            # Get the Customers database collection
            db = self.client['Customers']
            # See if no customers in database or this customer already in the database
            if (db.customers.count() == 0) or (len(list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))) == 0):
                # New customer needs all data assigned
                customer = {'emailAddress'             : email_address,
                            'rewardsPoints'            : 0,
                            'rewardsTier'              : '',
                            'rewardsTierName'          : '',
                            'nextRewardsTier'          : '',
                            'nextRewardsTierName'      : '',
                            'nextRewardsTierProgress'  : '1.00'}
                # Process customer rewards
                customer = process_rewards(customer, order_total)
                # Insert customer into database
                db.customers.insert(customer)
                # Verify insert successful
                result = list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))
                if len(result) > 0:
                    customer = result[0]
                    logger.info(customer)
                    # Write customer
                    return self.write(json.dumps(customer))
                else:
                    message = 'POSTERROR: Customer not added.'
                    logger.error(message)
                    return self.send_error(400, message=message)
            else:
                message = 'POSTERROR: Not a new customer use PUT to update.'
                logger.warn(message)
                return self.send_error(400, message=message)
        except:
            logger.error('POSTERROR: Error handling POST.')
            raise

    # get
    # expects: email address as query string parameter
    # returns: customer rewards profile
    @coroutine
    def get(self):
        try:
            # Get query string parameter
            email_address = self.get_query_argument('emailAddress', None) # default None to return all customers
            # Get the Customers database collection
            db = self.client['Customers']
            if email_address is None:
                # Return all customers
                customers = sorted(list(db.customers.find({}, {'_id': 0})), key=lambda k: k['emailAddress'])
                logger.info(customers)
                # Write customer
                return self.write(json.dumps(customers))
            else:
                # See if customers in database
                if db.customers.count() > 0:
                    # Return one customer matching email address parameter
                    result = list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))
                    if len(result) > 0:
                        customer = result[0]
                        logger.info(customer)
                        # Write customer
                        return self.write(json.dumps(customer))
                    else:
                        message = 'GETERROR: Customer not found.'
                        logger.info(message)
                        return self.write(json.dumps({}))
                else:
                    message = 'GETERROR: No customers in database.'
                    logger.info(message)
                    return self.write(json.dumps({}))
        except:
            logger.error('GETERROR: Error handling GET.')
            raise

    # put
    # expects: email address, order total as JSON payload data
    # returns: updated customer rewards profile
    @coroutine
    def put(self):
        try:
            # Get payload data and validate
            if 'emailAddress' in self.json_data:
                email_address = self.json_data['emailAddress']
                if not is_email_address(email_address):
                    message = 'ARGERROR: emailAddress not email address.'
                    logger.warn(message)
                    return self.send_error(400, message=message) # return 400 when invalid
            else:
                message = 'ARGERROR: Missing JSON argument: emailAddress.'
                logger.warn(message)
                return self.send_error(400, message=message) # return 400 when missing
            if 'orderTotal' in self.json_data:
                try:
                    if str(self.json_data['orderTotal']).lower() in ('nan', 'inf'):
                        raise ValueError
                    order_total = float(self.json_data['orderTotal'])
                except ValueError:
                    message = 'ARGERROR: orderTotal not number.'
                    logger.warn(message)
                    return self.send_error(400, message=message) # return 400 when invalid
            else:
                message = 'ARGERROR: Missing JSON argument: orderTotal.'
                logger.warn(message)
                return self.send_error(400, message=message) # return 400 when missing
                
            # Get the Customers database collection
            db = self.client['Customers']
            # See if customers in database and this customer already in the database
            if db.customers.count() > 0:
                # Return one customer matching email address parameter
                result = list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))
                if len(result) > 0:
                    # Current customer
                    customer = result[0]
                    # Process customer rewards
                    customer = process_rewards(customer, order_total)
                    # Current customer just needs updating
                    db.customers.update({'emailAddress' : email_address}, {'$set': customer})
                    # Verify insert successful
                    result = list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))
                    if len(result) > 0:
                        customer = result[0]
                        logger.info(customer)
                        # Write customer
                        return self.write(json.dumps(customer))
                    else:
                        message = 'PUTERROR: Customer not updated.'
                        logger.error(message)
                        return self.send_error(400, message=message)
                else:
                    message = 'PUTERROR: New customer use POST to add.'
                    logger.warn(message)
                    return self.send_error(400, message=message)
            else:
                message = 'PUTERROR: No customers in database.'
                logger.info(message)
                return self.write(json.dumps({}))
        except:
            logger.error('PUTERROR: Error handling PUT.')
            raise

    # delete
    # expects: email address as query string parameter
    # returns: deleted customer rewards profile
    @coroutine
    def delete(self):
        try:
            # Get query string parameter
            email_address = self.get_query_argument('emailAddress', None) # default None
            # Get the Customers database collection
            db = self.client['Customers']
            if email_address is None:
                # Do nothing
                message = 'ARGERROR: Missing query string parameter: emailAddress.'
                logger.warn(message)
                return self.send_error(400, message=message) # return 400 when missing
            else:
                # See if customers in database
                if db.customers.count() > 0:
                    # Return one customer matching email address parameter
                    result = list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))
                    if len(result) > 0:
                        customer = result[0]
                        # Delete one customer matching email address parameter
                        db.customers.remove({'emailAddress' : email_address})
                        # Verify remove successful
                        result = list(db.customers.find({'emailAddress' : email_address}, {'_id': 0}))
                        if len(result) == 0:
                            logger.info(customer)
                            # Write customer
                            return self.write(json.dumps(customer))
                        else:
                            message = 'DELETEERROR: Customer not deleted.'
                            logger.error(message)
                            return self.send_error(400, message=message)
                    else:
                        message = 'DELETEERROR: Customer not found.'
                        logger.info(message)
                        return self.write(json.dumps({}))
                else:
                    message = 'DELETEERROR: No customers in database.'
                    logger.info(message)
                    return self.write(json.dumps({}))
        except:
            logger.error('DELETEERROR: Error handling DELETE.')
            raise


# is_email_address
# expects: email address
# returns: True or False
def is_email_address(email_address):
    try:
        # Sipmle check for valid email
        return re.match(r'[^@]+@[^@]+\.[^@]+', email_address)
    except:
        return False


#process_rewards
# expects: customer rewards profile, order total
# returns: customer rewards profile
def process_rewards(customer, order_total):
    try:
        # Add points to customer rewards total
        customer['rewardsPoints'] = math.floor(customer['rewardsPoints'] + order_total)
        # Make points total non-negative
        if customer['rewardsPoints'] < 0:
            customer['rewardsPoints'] = 0
        # Create db client
        client = MongoClient('mongodb', 27017)
        # Get the Rewards database collection in ascending order by points
        db = client['Rewards']
        # See if rewards in database
        if db.rewards.count() > 0:
            rewards_data = sorted(list(db.rewards.find({}, {'_id': 0})), key=lambda k: k['points']) 
            # Remember points value for the customer's current rewards tier
            customers_current_rewards_tier_points = 0
            # Locate the appropriate customer rewards tier
            for reward in rewards_data:
                # Looking for next customer rewards tier
                if customer['rewardsPoints'] < reward['points']:
                    customer['nextRewardsTier'] = reward['tier']
                    customer['nextRewardsTierName'] = reward['rewardName']
                    customer['nextRewardsTierProgress'] = format(
                        ((reward['points'] - customer['rewardsPoints']) /
                         (reward['points'] - customers_current_rewards_tier_points)),
                        '.2f')
                    break
                # Customer has at least reached this tear
                customers_current_rewards_tier_points = reward['points']
                customer['rewardsTier'] = reward['tier']
                customer['rewardsTierName'] = reward['rewardName']
            # Check for customer in bottom tier
            if customer['rewardsPoints'] < rewards_data[0]['points']:
                customer['rewardsTier'] = ''
                customer['rewardsTierName'] = ''
            # Check for customer in top tier
            if customer['rewardsPoints'] >= rewards_data[-1]['points']:
                customer['nextRewardsTier'] = ''
                customer['nextRewardsTierName'] = ''
                customer['nextRewardsTierProgress'] = '0.00'
        else:
            message = 'PROCESSINGRROR: No rewards in database.'
            logger.error(message)
        return customer
    except:
        raise
        