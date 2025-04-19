import requests

# ========== CONFIGURATION ===========
BASE_URL = "https://thingsboard.cloud"
CUSTOMER_USERS = {
    "General IP": {"username": "bob_hernanadez123@fiu.edu", "password": "123456"},
    "Field Researcher": {"username": "ejohnson@fiu.edu", "password": "123456"},
    "Data Analyst": {"username": "alyssa_roberts112@fiu.edu", "password": "123456"},
    "Public Viewer": {"username": "william_miller453@fiu.edu", "password": "123456"},
}

DEVICE_ID = "1808cd70-1bc6-11f0-86ac-951bbb28eae1"
DASHBOARD_ID = "20ad3a60-1bcb-11f0-86ac-951bbb28eae1"

# ========== UTILITIES ==========

def login(username, password):
    url = f"{BASE_URL}/api/auth/login"
    r = requests.post(url, json={"username": username, "password": password})
    r.raise_for_status()
    return r.json()["token"]

def get_headers(token):
    return {
        "Content-Type": "application/json",
        "X-Authorization": f"Bearer {token}"
    }

def print_result(action, status, expected):
    result = "PASS" if status == expected else "FAIL"
    print(f"[{result}] {action} | Status: {status} | Expected: {expected}")

# ========== TEST ACTIONS ==========

def can_access_api(role):
    creds = CUSTOMER_USERS[role]
    try:
        token = login(creds["username"], creds["password"])
        print(f"[PASS] {role} logged in.")
        return token
    except Exception as e:
        print(f"[FAIL] {role} cannot login: {e}")
        return None

def can_post_telemetry(token, device_id):
    url = f"{BASE_URL}/api/plugins/telemetry/DEVICE/{device_id}/timeseries/ANY"
    payload = {"ph": 7.2, "temp": 21.9}
    r = requests.post(url, json=payload, headers=get_headers(token))
    print_result("post telemetry", r.status_code, expected=200)

def can_view_telemetry(token, device_id):
    url = f"{BASE_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys=ph,temp"
    r = requests.get(url, headers=get_headers(token))
    print_result("view telemetry", r.status_code, expected=200)

def can_download_report(token):
    url = f"{BASE_URL}/api/customer/report/download"
    r = requests.get(url, headers=get_headers(token))
    print_result("download report", r.status_code, expected=200)

def can_send_alert(token):
    url = f"{BASE_URL}/api/customer/alert"
    payload = {"message": "Sensor abnormal pH alert"}
    r = requests.post(url, json=payload, headers=get_headers(token))
    print_result("send alert", r.status_code, expected=200)

def can_view_dashboard(token, dashboard_id):
    url = f"{BASE_URL}/api/dashboard/{dashboard_id}"
    r = requests.get(url, headers=get_headers(token))
    print_result("view dashboard", r.status_code, expected=200)

# ========== MAIN TEST DRIVER ==========

def run_customer_user_tests():
    for role in CUSTOMER_USERS:
        print(f"\n===== TESTING CUSTOMER ROLE: {role.upper()} =====")
        token = can_access_api(role)
        if not token:
            continue

        if role == "Field Researcher":
            can_post_telemetry(token, DEVICE_ID)
            can_view_telemetry(token, DEVICE_ID)
            can_download_report(token)

        elif role == "Data Analyst":
            can_view_telemetry(token, DEVICE_ID)
            can_download_report(token)
            can_send_alert(token)

        elif role == "Public Viewer":
            can_view_dashboard(token, DASHBOARD_ID)

        elif role == "General IP":
            # No specific API calls, login-only test
            pass

if __name__ == "__main__":
    run_customer_user_tests()
