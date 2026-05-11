import requests

ASSIGNMENT_SERVICE_URL = "http://localhost:8002/assignments/api/"
SUBMISSION_SERVICE_URL = "http://localhost:8003/submissions/api/"
AUTH_SERVICE_URL = "http://localhost:8001/accounts/api/"

def get_assignment(assignment_id):
    response = requests.get(f"{ASSIGNMENT_SERVICE_URL}{assignment_id}/")
    return response.json() if response.status_code == 200 else None

def get_all_assignments():
    response = requests.get(ASSIGNMENT_SERVICE_URL)
    return response.json() if response.status_code == 200 else []

def get_submission(submission_id):
    response = requests.get(f"{SUBMISSION_SERVICE_URL}{submission_id}/")
    return response.json() if response.status_code == 200 else None

def get_all_submissions():
    response = requests.get(SUBMISSION_SERVICE_URL)
    return response.json() if response.status_code == 200 else []

def get_user(user_id):
    response = requests.get(f"{AUTH_SERVICE_URL}users/{user_id}/")
    return response.json() if response.status_code == 200 else None
