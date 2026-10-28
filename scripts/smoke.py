"""Exercise normal account, vehicle, community, and shop flows on a local stack."""
import html
import json
import os
import re
import time
import uuid
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

BASE = os.environ.get("CRAPI_URL", "http://localhost:8888").rstrip("/")
MAIL = os.environ.get("CRAPI_MAIL_URL", "http://localhost:8025").rstrip("/")
for endpoint in (BASE, MAIL):
    if urlparse(endpoint).hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Smoke checks create data and must target a local stack")


def request(path, data=None, token=None, base=BASE):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = Request(base + path, headers=headers,
                  data=json.dumps(data).encode() if data is not None else None)
    try:
        with urlopen(req, timeout=30) as response:
            body = response.read().decode()
            assert 200 <= response.status < 300, response.status
            return json.loads(body) if body else None
    except HTTPError as exc:
        raise AssertionError(f"{req.method} {path}: HTTP {exc.code}") from exc


def main():
    with urlopen(BASE, timeout=30) as response:
        assert "Vehicle services" in response.read().decode()
    suffix = uuid.uuid4().hex[:12]
    email = f"driver-{suffix}@example.com"
    password = "Driver!12345"
    request("/identity/api/auth/signup", {
        "name": "Local Driver", "email": email,
        "number": "9" + str(int(suffix, 16))[-9:], "password": password,
    })
    token = request("/identity/api/auth/login", {
        "email": email, "password": password,
    })["token"]
    dashboard = request("/identity/api/v2/user/dashboard", token=token)
    assert email in json.dumps(dashboard), "Account not present in dashboard"
    print("PASS registration, login, and profile")

    # Use the owner's actual welcome email to register the assigned vehicle.
    for attempt in range(30):
        messages = request("/api/v2/search?" + urlencode({
            "kind": "to", "query": email,
        }), base=MAIL)
        bodies = " ".join(item["Content"]["Body"] for item in messages["items"])
        plain = html.unescape(re.sub(r"<[^>]+>", "", bodies))
        vin = re.search(r"VIN:\s*([A-Z0-9]+)", plain)
        pin = re.search(r"Pincode:\s*([0-9]+)", plain)
        if vin and pin:
            break
        time.sleep(1)
    assert vin and pin, "Vehicle welcome email was not received"
    request("/identity/api/v2/vehicle/add_vehicle", {
        "vin": vin.group(1), "pincode": pin.group(1),
    }, token)
    vehicles = request("/identity/api/v2/vehicle/vehicles", token=token)
    assert vin.group(1) in json.dumps(vehicles), "Registered vehicle is missing"
    print("PASS mail delivery and vehicle registration")

    title = "Road trip " + suffix
    request("/community/api/v2/community/posts", {
        "title": title, "content": "Planning my next service before a road trip.",
    }, token)
    posts = request("/community/api/v2/community/posts/recent?limit=30&offset=0", token=token)
    assert title in json.dumps(posts), "New post is missing"
    print("PASS community post creation and retrieval")

    products = request("/workshop/api/shop/products?limit=30&offset=0", token=token)
    assert products["products"], "Product catalog is empty"
    product = min(products["products"], key=lambda item: float(item["price"]))
    request("/workshop/api/shop/orders", {"product_id": product["id"], "quantity": 1}, token)
    orders = request("/workshop/api/shop/orders/all", token=token)
    assert orders["orders"], "Order history is empty"
    print("PASS product catalog, order creation, and order history")


if __name__ == "__main__":
    main()
