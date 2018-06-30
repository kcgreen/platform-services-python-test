from django.conf.urls import url

from customers.proxy import proxy_to

urlpatterns = [
    url(r'^$', proxy_to, {'target_url': 'http://rewardsservice:7050/customers'}),
]
