import requests
from django.conf import settings

ASSIGNMENT_SERVICE_URL = "http://localhost:8002/assignments/api/"
AUTH_SERVICE_URL = "http://localhost:8001/accounts/api/"

def get_assignment(assignment_id):
    response = requests.get(f"{ASSIGNMENT_SERVICE_URL}{assignment_id}/")
    if response.status_code == 200:
        return response.json()
    return None

def get_user(user_id):
    response = requests.get(f"{AUTH_SERVICE_URL}users/{user_id}/")
    if response.status_code == 200:
        return response.json()
    return None
