import requests
import sys

BASE_URL = "http://localhost"

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"

def test(name: str, fn):
    try:
        fn()
        print(f"  {PASS} {name}")
        return True
    except AssertionError as e:
        print(f"  {FAIL} {name} — {e}")
        return False
    except Exception as e:
        print(f"  {FAIL} {name} — {e}")
        return False

def run_catalog_tests() -> bool:
    print("\n📦 Catalog Service")
    passed = True

    def create_restaurant():
        res = requests.post(f"{BASE_URL}/api/restaurants", json={
            "name": "Test Restaurant",
            "description": "A test restaurant",
            "address": "123 Test St"
        })
        assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
        data = res.json()
        assert "id" in data, "Response missing id"
        assert data["name"] == "Test Restaurant"

    def list_restaurants():
        res = requests.get(f"{BASE_URL}/api/restaurants")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        assert isinstance(res.json(), list)

    passed &= test("POST /api/restaurants — create a restaurant", create_restaurant)
    passed &= test("GET  /api/restaurants — list restaurants", list_restaurants)
    return passed

def run_customer_tests() -> bool:
    print("\n👤 Customer Service")
    passed = True

    def register_customer():
        res = requests.post(f"{BASE_URL}/api/customers/register", json={
            "username": "testuser_e2e",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        })
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert "id" in data
        assert data["username"] == "testuser_e2e"

    def login_customer():
        res = requests.post(f"{BASE_URL}/api/customers/login", json={
            "username": "testuser_e2e",
            "password": "password123"
        })
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    passed &= test("POST /api/customers/register — register a customer", register_customer)
    passed &= test("POST /api/customers/login — login a customer", login_customer)

    return passed

def run_cart_tests() -> bool:
    print("\n🛒 Order Cart Service")
    passed = True

    user_id = "550e8400-e29b-41d4-a716-446655440000"
    item_id = "550e8400-e29b-41d4-a716-446655440001"
    restaurant_id = "550e8400-e29b-41d4-a716-446655440002"

    def add_item_to_cart():
        res = requests.post(f"{BASE_URL}/api/cart/{user_id}/items", json={
            "item_id": item_id,
            "restaurant_id": restaurant_id,
            "name": "Margherita Pizza",
            "price": 12.99,
            "quantity": 2
        })
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert "items" in data
        assert str(item_id) in data["items"]

    def get_cart():
        res = requests.get(f"{BASE_URL}/api/cart/{user_id}")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert "user_id" in data
        assert "items" in data

    passed &= test("POST /api/cart/{user_id}/items — add item to cart", add_item_to_cart)
    passed &= test("GET  /api/cart/{user_id} — get cart", get_cart)
    
    return passed

def run_order_tests() -> bool:
    print("\n📋 Order Service")
    passed = True

    def create_order():
        res = requests.post(f"{BASE_URL}/api/orders", json={
            "userId": "550e8400-e29b-41d4-a716-446655440000",
            "restaurantId": "550e8400-e29b-41d4-a716-446655440001",
            "items": [
                {
                    "itemId": "550e8400-e29b-41d4-a716-446655440002",
                    "restaurantId": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "Margherita Pizza",
                    "price": 12.99,
                    "quantity": 2
                }
            ],
            "totalPrice": 25.98
        })
        assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
        data = res.json()
        assert "id" in data
        assert data["status"] == "PENDING"
        assert data["totalPrice"] == 25.98

    def list_orders():
        res = requests.get(f"{BASE_URL}/api/orders")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        assert isinstance(res.json(), list)

    passed &= test("POST /api/orders — create an order", create_order)
    passed &= test("GET  /api/orders — list orders", list_orders)
    return passed


def run_queue_tests() -> bool:
    print("\n📨 Message Service")
    passed = True

    def send_message():
        res = requests.post(f"{BASE_URL}/api/send", json={
            "msg": "hello from e2e test"
        })
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert "message" in data
        assert data["message"] == "hello from e2e test"

    passed &= test("POST /api/send — send and echo a message", send_message)
    return passed


def main():
    print("=" * 50)
    print("  E2E Test Suite — Food Ordering Microservice")
    print("=" * 50)

    results = [
        run_catalog_tests(),
        run_customer_tests(),
        run_cart_tests(),
        run_order_tests(),
        run_queue_tests(),
    ]

    total_services = len(results)
    passed_services = sum(results)

    print("\n" + "=" * 50)
    if all(results):
        print(f"\033[92m  All services passed! ({passed_services}/{total_services})\033[0m")
        sys.exit(0)
    else:
        print(f"\033[91m  Some services failed. ({passed_services}/{total_services} passed)\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()

