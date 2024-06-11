def product_schema(product) -> dict:
  return {
    "id": str(product["_id"]),
    "name": product["name"],
    "price": product["price"],
    "quantity": product["quantity"]
  }