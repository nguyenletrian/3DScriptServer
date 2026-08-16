from core.repository import BaseRepository


TEMPLATES = {
    "categories": "categories",
    "products": "products",
    "customers": "customers",
    "orders": "orders",
    "order_items": "order_items",
}


def _next_id(items):
    ids = [item.get("id") for item in items if isinstance(item.get("id"), int) and not isinstance(item.get("id"), bool)]
    return max(ids, default=0) + 1


def _normalize_instance_ids(repos, instance_id):
    rows = {name: [x for x in repos[name].get_all() if x.get("application_instance_id") == instance_id] for name in TEMPLATES}
    if not any(rows.values()): return
    if all(isinstance(row.get("id"), int) and not isinstance(row.get("id"), bool) for items in rows.values() for row in items): return

    maps = {}
    for name in ("categories", "products", "customers", "orders", "order_items"):
        maps[name] = {}
        for row in rows[name]:
            if isinstance(row.get("id"), int) and not isinstance(row.get("id"), bool): continue
            new_id = _next_id(repos[name].get_all()); maps[name][row["id"]] = new_id
            repos[name].update(row["id"], {"id": new_id})

    for row in rows["products"]:
        if row.get("category_id") in maps["categories"]: repos["products"].update(maps["products"].get(row["id"], row["id"]), {"category_id": maps["categories"][row["category_id"]]})
    for row in rows["orders"]:
        if row.get("customer_id") in maps["customers"]: repos["orders"].update(maps["orders"].get(row["id"], row["id"]), {"customer_id": maps["customers"][row["customer_id"]]})
    for row in rows["order_items"]:
        data = {}
        if row.get("order_id") in maps["orders"]: data["order_id"] = maps["orders"][row["order_id"]]
        if row.get("product_id") in maps["products"]: data["product_id"] = maps["products"][row["product_id"]]
        if data: repos["order_items"].update(maps["order_items"].get(row["id"], row["id"]), data)


def seed_instance(instance_id):
    repos = {name: BaseRepository(collection) for name, collection in TEMPLATES.items()}
    _normalize_instance_ids(repos, instance_id)
    if any(x.get("application_instance_id") == instance_id for x in repos["products"].get_all()): return

    category_map = {}
    for row in repos["categories"].get_all():
        if row.get("application_instance_id"): continue
        new_id = _next_id(repos["categories"].get_all()); category_map[row["id"]] = new_id
        repos["categories"].insert({**row, "id": new_id, "application_instance_id": instance_id})

    product_map = {}
    for row in repos["products"].get_all():
        if row.get("application_instance_id"): continue
        new_id = _next_id(repos["products"].get_all()); product_map[row["id"]] = new_id
        repos["products"].insert({**row, "id": new_id, "category_id": category_map.get(row.get("category_id"), row.get("category_id")), "application_instance_id": instance_id})

    customer_map = {}
    for row in repos["customers"].get_all():
        if row.get("application_instance_id"): continue
        new_id = _next_id(repos["customers"].get_all()); customer_map[row["id"]] = new_id
        repos["customers"].insert({**row, "id": new_id, "application_instance_id": instance_id})

    order_map = {}
    for row in repos["orders"].get_all():
        if row.get("application_instance_id"): continue
        new_id = _next_id(repos["orders"].get_all()); order_map[row["id"]] = new_id
        repos["orders"].insert({**row, "id": new_id, "customer_id": customer_map.get(row.get("customer_id"), row.get("customer_id")), "application_instance_id": instance_id})

    for row in repos["order_items"].get_all():
        if row.get("application_instance_id"): continue
        new_id = _next_id(repos["order_items"].get_all())
        repos["order_items"].insert({**row, "id": new_id, "order_id": order_map.get(row.get("order_id"), row.get("order_id")), "product_id": product_map.get(row.get("product_id"), row.get("product_id")), "application_instance_id": instance_id})
