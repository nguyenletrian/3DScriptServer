from core.crud import crud_router


def _router(name, collection, prefix):
    return crud_router({"name": name, "collection": collection, "prefix": prefix, "tag": name.title(), "instance_scoped": True, "write_admin_only": False})

router = _router("coffee_products", "products", "/coffee/products")
routers = [
    router,
    _router("coffee_categories", "categories", "/coffee/categories"),
    _router("coffee_customers", "customers", "/coffee/customers"),
    _router("coffee_orders", "orders", "/coffee/orders"),
    _router("coffee_order_items", "order_items", "/coffee/order-items"),
]
