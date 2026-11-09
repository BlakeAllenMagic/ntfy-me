import requests
import sys

PRODUCT_URL = "https://desky.com/products/resin-river-standing-table.js"
PRODUCT_PAGE = "https://desky.com/products/resin-river-standing-table?variant=46587346092354"

VARIANT_ID = 46587346092354
NTFY_TOPIC = "blake-desky-river"

response = requests.get(
    PRODUCT_URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)
response.raise_for_status()

product = response.json()

variant = next(
    (v for v in product["variants"] if v["id"] == VARIANT_ID),
    None
)

if variant is None:
    print(f"ERROR: Variant {VARIANT_ID} was not found.")
    sys.exit(1)

print(f"Product: {product['title']}")
print(f"Variant: {variant['title']}")
print(f"Available: {variant['available']}")

if variant["available"]:
    print("DESK IS IN STOCK! Sending notification...")

    notification = requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=(
            "Your Desky Walnut Emerald River desk is IN STOCK!\n\n"
            f"{variant['title']}\n\n"
            "Tap here to buy it."
        ).encode("utf-8"),
        headers={
            "Title": "DESKY IS IN STOCK!",
            "Priority": "urgent",
            "Tags": "tada,furniture",
            "Click": PRODUCT_PAGE,
        },
        timeout=30,
    )

    notification.raise_for_status()

    print("Notification sent.")
else:
    print("Still sold out. No notification sent.")
