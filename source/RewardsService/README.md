# Objective
Create RESTful endpoint(s) to calculate, store, and retrieve customer rewards data from MongoDB.

# Background
* You will be using the [Tornado](http://www.tornadoweb.org) Python web framework and a MongoDB docker image.
* When starting up the 'rewardsservice' docker container in the [Setup](#setup) below, a mongo 'Rewards' database will be created for you with a "rewards" collection containing each reward a user can earn and how many points are needed to reach each reward.
    ```
    [
        { "tier": "A", "rewardName": "5% off purchase", "points": 100 },
        { "tier": "B", "rewardName": "10% off purchase", "points": 200 },
        { "tier": "C", "rewardName": "15% off purchase", "points": 300 },
        { "tier": "D", "rewardName": "20% off purchase", "points": 400 },
        { "tier": "E", "rewardName": "25% off purchase", "points": 500 },
        { "tier": "F", "rewardName": "30% off purchase", "points": 600 },
        { "tier": "G", "rewardName": "35% off purchase", "points": 700 },
        { "tier": "H", "rewardName": "40% off purchase", "points": 800 },
        { "tier": "I", "rewardName": "45% off purchase", "points": 900 },
        { "tier": "J", "rewardName": "50% off purchase", "points": 1000 }
    ]
    ```

# Instructions:
* Design and implement the following endpoints.
    * **Endpoint 1:**
        * Accept a customer's order data: **email adress**  (ex. "customer01@gmail.com") and **order total** (ex. 100.80).
        * Calculate and store the following customer rewards data into MongoDB. For each dollar a customer spends, the customer will earn 1 reward point. For example, a customer whose order total is $100.80 earns 100 points and belongs to Rewards Tier A. Note: a customer can only belong to one rewards tier. For example, a customer with 205 reward points belongs to Rewards Tier B and cannot use the reward from Tier A. Once a customer has reached the top rewards tier, there are no additional rewards the customer can earn.
            * **Email Address:** the customer's email address (ex. "customer01@gmail.com")
            * **Reward Points:** the customer's rewards points (ex. 100)
            * **Rewards Tier:** the rewards tier the customer has reached (ex. "A")
            * **Reward Tier Name:** the name of the rewards tier (ex. "5% off purchase")
            * **Next Rewards Tier:** the next rewards tier the customer can reach (ex. "B")
            * **Next Rewards Tier Name:** the name of next rewards tier (ex. "10% off purchase")
            * **Next Rewards Tier Progress:** the percentage the customer is away from reaching the next rewards tier (ex. 0.5)
    * **Endpoint 2:** Accept a customer's email address, and return the customer's rewards data that was stored in Endpoint 1.
    * **Endpoint 3:** Return the same rewards data as Endpoint 2 but for all customers.
* For bonus points, add error handling and unit tests.

# Setup
* Install docker and docker-compose dependencies.
* $ cd APP_PATH/platform-services-python-test/source/RewardsService
* $ docker-compose build
* $ docker-compose up -d
* Services are accessible at http://localhost:7050/

>**Note**
>
>Using VirtualBox to host Docker? Make the following setup adjustments:
>* In the `docker-compose.yaml` file, find `volumes:` and replace "`- ./data/db:/data/db`" with "`- /var/lib/boot2docker/my-mongodb-data/:/data/db`".
>* Services are accessible from a browser at `http://w.x.y.z:7050/` where `w.x.y.z` is the address of the VirtualBox virtual machine.

# Summary for RewardsService

* Added url pattern for /customers endpoint:  [http://rewardsservice:7050/customers](http://localhost:7050/customers)
* Added class CustomersHandler as tonado.web.RequestHandler:

    Http Verb | Payload Data (JSON) (a)  | Result
    --- | --- | --- |
    POST | {'emailAddress': 'a.foo@bar.com',  'orderTotal': 74.99} |  Create One
    PUT	 | {'emailAddress': 'a.foo@bar.com',  'orderTotal': '151.01'} |  Update One

    (a) 'orderTotal' value can be number or number as a string (except: 'NaN' or 'inf').
				 
    Http Verb | Query String Parameter | Result
    --- | --- | --- |
    GET | ?emailAddress=a.foo@bar.com | Read One (b)
    GET | | Read All (b)
    DELETE | ?emailAddress=a.foo@bar.com | Delete One

    (b) GET method always returns a JSON list of customer profiles: ` [{}, {}, ...]`

* Created 'Customers' Mongo database with a "customers" collection for customer data:

    ```
    [
        {"rewardsPoints": 643, "nextRewardsTierProgress": "0.57", "nextRewardsTier": "G", "rewardsTierName": "30% off purchase", "rewardsTier": "F", "emailAddress": "amy@foo.bar.net", "nextRewardsTierName": "35% off purchase"}, 
        {"rewardsPoints": 175, "nextRewardsTierProgress": "0.25", "nextRewardsTier": "B", "rewardsTierName": "5% off purchase", "rewardsTier": "A", "emailAddress": "ann@foo.bar", "nextRewardsTierName": "10% off purchase"}, 
        {"rewardsPoints": 599, "nextRewardsTierProgress": "0.01", "nextRewardsTier": "F", "rewardsTierName": "25% off purchase", "rewardsTier": "E", "emailAddress": "betty@foo.bar", "nextRewardsTierName": "30% off purchase"}, 
        {"rewardsPoints": 200, "nextRewardsTierProgress": "1.00", "nextRewardsTier": "C", "rewardsTierName": "10% off purchase", "rewardsTier": "B", "emailAddress": "carly@foo.bar.net", "nextRewardsTierName": "15% off purchase"}, 
        {"rewardsPoints": 137, "nextRewardsTierProgress": "0.63", "nextRewardsTier": "B", "rewardsTierName": "5% off purchase", "rewardsTier": "A", "emailAddress": "denise@foo.bar.com", "nextRewardsTierName": "10% off purchase"}, 
        {"rewardsPoints": 1295, "nextRewardsTierProgress": "0.00", "nextRewardsTier": "", "rewardsTierName": "50% off purchase", "rewardsTier": "J", "emailAddress": "ellen@foo.bar", "nextRewardsTierName": ""}, 
        {"rewardsPoints": 0, "nextRewardsTierProgress": "1.00", "nextRewardsTier": "A", "rewardsTierName": "", "rewardsTier": "", "emailAddress": "fran@foo.bar", "nextRewardsTierName": "5% off purchase"}, 
        {"rewardsPoints": 123, "nextRewardsTierProgress": "0.77", "nextRewardsTier": "B", "rewardsTierName": "5% off purchase", "rewardsTier": "A", "emailAddress": "gina@foo.bar.net", "nextRewardsTierName": "10% off purchase"}, 
        {"rewardsPoints": 249, "nextRewardsTierProgress": "0.51", "nextRewardsTier": "C", "rewardsTierName": "10% off purchase", "rewardsTier": "B", "emailAddress": "hellen@foo.bar", "nextRewardsTierName": "15% off purchase"}, 
        {"rewardsPoints": 683, "nextRewardsTierProgress": "0.17", "nextRewardsTier": "G", "rewardsTierName": "30% off purchase", "rewardsTier": "F", "emailAddress": "isabella@foo.bar.com", "nextRewardsTierName": "35% off purchase"}, 
        {"rewardsPoints": 79, "nextRewardsTierProgress": "0.21", "nextRewardsTier": "A", "rewardsTierName": "", "rewardsTier": "", "emailAddress": "jan@foo.bar.foo.bar.com", "nextRewardsTierName": "5% off purchase"}, 
        {"rewardsPoints": 243, "nextRewardsTierProgress": "0.57", "nextRewardsTier": "C", "rewardsTierName": "10% off purchase", "rewardsTier": "B", "emailAddress": "katie@foo.bar.foo.bar.foo.bar.net", "nextRewardsTierName": "15% off purchase"}
    ]
    ```
