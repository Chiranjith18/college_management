import requests

ASSIGNMENT_SERVICE_URL = "http://localhost:8002/assignments/api/"
SUBMISSION_SERVICE_URL = "http://localhost:8003/submissions/api/"
AUTH_SERVICE_URL = "http://localhost:8001/accounts/api/"
REQUEST_TIMEOUT_SECONDS = 5
session = requests.Session()

def get_assignment(assignment_id):
    try:
        response = session.get(f"{ASSIGNMENT_SERVICE_URL}{assignment_id}/", timeout=REQUEST_TIMEOUT_SECONDS)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException:
        return None

def get_all_assignments():
    try:
        response = session.get(ASSIGNMENT_SERVICE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        return response.json() if response.status_code == 200 else []
    except requests.RequestException:
        return []

def get_submission(submission_id):
    try:
        response = session.get(f"{SUBMISSION_SERVICE_URL}{submission_id}/", timeout=REQUEST_TIMEOUT_SECONDS)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException:
        return None

def get_all_submissions():
    try:
        response = session.get(SUBMISSION_SERVICE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        return response.json() if response.status_code == 200 else []
    except requests.RequestException:
        return []

def get_user(user_id):
    try:
        response = session.get(f"{AUTH_SERVICE_URL}users/{user_id}/", timeout=REQUEST_TIMEOUT_SECONDS)
        return response.json() if response.status_code == 200 else None
    except requests.RequestException:
        return None
