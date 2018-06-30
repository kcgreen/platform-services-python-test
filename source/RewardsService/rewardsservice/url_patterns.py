from handlers.customers_handler import CustomersHandler
from handlers.rewards_handler import RewardsHandler


url_patterns = [
    (r'/customers', CustomersHandler),
    (r'/rewards', RewardsHandler),
]
