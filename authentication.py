import requests

# ========== CONFIGURATION ===========
BASE_URL = "https://thingsboard.cloud"
CUSTOMER_USERS = {
    "General IP": {"username": "bob_hernanadez123@fiu.edu", "password": "123456"},
    "Field Researcher": {"username": "ejohnson@fiu.edu", "password": "123456"},
    "Data Analyst": {"username": "alyssa_roberts112@fiu.edu", "password": "123456"},
    "Public Viewer": {"username": "william_miller453@fiu.edu", "password": "123456"},
}

DEVICES = {
    "Salinity": {"id": "1808cd70-1bc6-11f0-86ac-951bbb28eae1"},
    "Water Temp": {"id": "42095320-1bc5-11f0-9092-2f72379381be"},
    "Water Depth": {"id": "fdddc650-1650-11f0-8f83-43727cd6bc90"},
    "Dissolved Oxygen": {"id": "cb6f6cb0-164f-11f0-86ac-951bbb28eae1"},
    "pH": {"id": "a231d090-164a-11f0-9092-2f72379381be"},
}

DASHBOARDS = {
    "Administrator": {"id": "e1d5d440-1bd0-11f0-b4bd-8b00c50fcae5"},
    "Analyzer and Reporting": {"id": "a5f986b0-1bcb-11f0-863b-f730addc68ba"},
    "Inputs: Water Quality": {"id": "20ad3a60-1bcb-11f0-86ac-951bbb28eae1"},
    "IT Operations": {"id": "ad6012e0-1bc4-11f0-86ac-951bbb28eae1"},
    "Water Quality": {"id": "b35c0aa0-166f-11f0-9092-2f72379381be"},
}


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
    id = DEVICES[device_id]
    url = f"{BASE_URL}/api/plugins/telemetry/DEVICE/{id['id']}/timeseries/ANY"
    payload = {"ph": 7.2, "temp": 21.9}
    r = requests.post(url, json=payload, headers=get_headers(token))
    print_result("post telemetry", r.status_code, expected=200)

def can_view_telemetry(token, device_id):
    id = DEVICES[device_id]
    url = f"{BASE_URL}/api/plugins/telemetry/DEVICE/{id['id']}/values/timeseries?keys=ph,temp"
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
    id = DASHBOARDS[dashboard_id]
    url = f"{BASE_URL}/api/dashboard/{id['id']}"
    r = requests.get(url, headers=get_headers(token))
    print_result("view dashboard", r.status_code, expected=200)

# ========== MAIN TEST DRIVER ==========

def run_customer_user_tests():
    for device in DEVICES:
        print(f"\n================ TESTING DEVICE: {device.upper()} ================")
        print(f"\n==================================================================")
        for role in CUSTOMER_USERS:
            print(f"\n===== TESTING CUSTOMER ROLE: {role.upper()} =====")
            token = can_access_api(role)
            if not token:
                continue

            if role == "Field Researcher":
                can_post_telemetry(token, device)
                can_view_telemetry(token, device)
                can_download_report(token)
                can_send_alert(token)

            elif role == "Data Analyst":
                can_post_telemetry(token, device)
                can_view_telemetry(token, device)
                can_download_report(token)
                can_send_alert(token)


            elif role == "Public Viewer":
                can_post_telemetry(token, device)
                can_view_telemetry(token, device)
                can_download_report(token)
                can_send_alert(token)

            elif role == "General IP":
                can_post_telemetry(token, device)
                can_view_telemetry(token, device)
                can_download_report(token)
                can_send_alert(token)
    
    for dash in DASHBOARDS:
        print(f"\n=============== TESTING DASHBOARD: {dash.upper()} ================")
        print(f"\n==================================================================")
        for role in CUSTOMER_USERS:
            print(f"\n===== TESTING CUSTOMER ROLE: {role.upper()} =====")
            token = can_access_api(role)
            if not token:
                continue

            if role == "Field Researcher":
                can_view_dashboard(token, dash)

            elif role == "Data Analyst":
                can_view_dashboard(token, dash)

            elif role == "Public Viewer":
                can_view_dashboard(token, dash)

            elif role == "General IP":
                can_view_dashboard(token, dash)

if __name__ == "__main__":
    run_customer_user_tests()
