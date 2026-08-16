from .application import ApplicationRuntime


class CoffeeRuntime(ApplicationRuntime):
    TITLE = "Coffee"
    PAGE_NAMES = [
        "coffee_dashboard",
        "coffee_products",
        "coffee_categories",
        "coffee_customers",
        "coffee_orders",
    ]
