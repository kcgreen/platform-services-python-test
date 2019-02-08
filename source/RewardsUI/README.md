# Objective
* Using the [Django](https://www.djangoproject.com/) Python web framework, create a Customer Rewards Dashboard that calls the RESTful endpoints created in [RewardsService](https://github.com/URBN-Interview/platform-services-python-test/tree/master/source/RewardsService).

# Instructions:
* Modify the [incomplete dashboard](https://github.com/URBN-Interview/platform-services-python-test/blob/master/source/RewardsUI/rewards/index.html) to add the following features:
    * **Add Orders** section:
        * Submit a customer's order data
    * **User Rewards** section:
        * Display a table of the rewards data of all customers
        * Filter the table for a specific customer
* For bonus points, add CSS and error handling.

# Setup
* Install docker and docker-compose dependencies.
* $ cd APP_PATH/platform-services-python-test/source/RewardsUI
* $ docker-compose build
* $ docker-compose up -d
* Open http://localhost:8000/rewards/ in your browser.

>**Note**
>
>Using VirtualBox to host Docker? Make the following setup adjustments:
>* In the `global/settings.py` file, find "`ALLOWED_HOSTS = []`" and replace with "`ALLOWED_HOSTS = ['w.x.y.z']`" where `w.x.y.z` is the address of the VirtualBox virtual machine.
>* Rewards Dashboard is accessible from a browser at `http://w.x.y.z:8000/rewards/` where `w.x.y.z` is the address of the VirtualBox virtual machine.

# Summary for RewardsUI

* Created proxy for requests from RewardsUI service to RewardsService.  New endpoint for RewardsUI rewards service matches /customers RewardsService url pattern (see above):  [http://rewardsui:8000/customers](http://localhost:8000/customers)
* Endpoint will only proxy:  POST, GET, PUT, and DELETE methods.
* Customer Rewards Dashboard:  [http://rewardsui:8000/rewards](http://localhost:8000/rewards)

### How To Use the Customer Rewards Dashboard

>**Add**
>---
>Enter valid email address and valid order total.
>
>**Search**
>---
>Enter valid email address to return one customer.
>Leave blank to return all customers.
>
> **Update (add to order total)**
>---
>Select anywhere on customer row of table (except delete radio button).
>Enter valid order total.
>
>**Delete**
>---
>Select radio button on customer row of table.
>Confirm by re-entering email address.
