from uuid import uuid4

from core.repository import BaseRepository


TEMPLATES = {
    "categories": "categories",
    "products": "products",
    "customers": "customers",
    "orders": "orders",
    "order_items": "order_items",
}


def seed_instance(instance_id):
    repos = {name: BaseRepository(collection) for name, collection in TEMPLATES.items()}
    existing = repos["products"].get_all()
    if any(x.get("application_instance_id") == instance_id for x in existing): return

    category_map = {}
    for row in repos["categories"].get_all():
        if row.get("application_instance_id"): continue
        new_id = f"cat_{uuid4().hex[:8]}"; category_map[row["id"]] = new_id
        repos["categories"].insert({**row, "id": new_id, "application_instance_id": instance_id})

    product_map = {}
    for row in repos["products"].get_all():
        if row.get("application_instance_id"): continue
        new_id = f"prod_{uuid4().hex[:8]}"; product_map[row["id"]] = new_id
        repos["products"].insert({**row, "id": new_id, "category_id": category_map.get(row.get("category_id"), row.get("category_id")), "application_instance_id": instance_id})

    customer_map = {}
    for row in repos["customers"].get_all():
        if row.get("application_instance_id"): continue
        new_id = f"cus_{uuid4().hex[:8]}"; customer_map[row["id"]] = new_id
        repos["customers"].insert({**row, "id": new_id, "application_instance_id": instance_id})

    order_map = {}
    for row in repos["orders"].get_all():
        if row.get("application_instance_id"): continue
        new_id = f"ord_{uuid4().hex[:8]}"; order_map[row["id"]] = new_id
        repos["orders"].insert({**row, "id": new_id, "customer_id": customer_map.get(row.get("customer_id"), row.get("customer_id")), "application_instance_id": instance_id})

    for row in repos["order_items"].get_all():
        if row.get("application_instance_id"): continue
        repos["order_items"].insert({**row, "id": f"item_{uuid4().hex[:8]}", "order_id": order_map.get(row.get("order_id"), row.get("order_id")), "product_id": product_map.get(row.get("product_id"), row.get("product_id")), "application_instance_id": instance_id})
