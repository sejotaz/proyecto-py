def product_schema(product) -> dict:
  return {
    "id": str(product["_id"]),
    "name_product": product["name_product"],
    "price": product["price"],
    "quantity": product["quantity"]
  }

def products_schema(products) -> list:
  return [product_schema(product) for product in products]