# Microservices Walkthrough — College Assignment Portal

## 1. Start All Services

Open **4 separate PowerShell terminals** from `c:\Users\chira\OneDrive\Desktop\task`:

### Terminal 1 — Auth Service (port 8001)
```powershell
cd auth_service
..\tri\Scripts\python manage.py runserver 8001
```

### Terminal 2 — Assignment Service (port 8002)
```powershell
cd assignment_service
..\tri\Scripts\python manage.py runserver 8002
```

### Terminal 3 — Submission Service (port 8003)
```powershell
cd submission_service
..\tri\Scripts\python manage.py runserver 8003
```

### Terminal 4 — Grading Service (port 8004)
```powershell
cd grading_service
..\tri\Scripts\python manage.py runserver 8004
```

---

## 2. Testing Workflow

### Step 1: Sign Up
1. Go to `http://localhost:8001/accounts/signup/`
2. Create a **Teacher** account (e.g. `teacher1` / password)
3. Create a **Student** account (e.g. `student1` / password)

### Step 2: Login as Teacher
1. Go to `http://localhost:8001/accounts/login/`
2. Login with your teacher credentials
3. You'll be auto-redirected to the Teacher Dashboard at `http://localhost:8004/dashboard/teacher/`

### Step 3: Create Assignment
1. Click **Create Assignment** in the navbar → goes to `http://localhost:8002/assignments/create/`
2. Fill in Title, Description, Deadline and save

### Step 4: Login as Student
1. Logout, then login with student credentials
2. You'll be redirected to `http://localhost:8004/dashboard/student/`
3. You should see the assignment created by the teacher

### Step 5: Submit Assignment
1. Click **Submit Now** → goes to `http://localhost:8003/submissions/submit/<id>/`
2. Upload a file and submit

### Step 6: Grade (Teacher)
1. Logout, login as teacher again
2. Go to `http://localhost:8004/dashboard/teacher/`
3. Click **Grade Now**, enter marks/feedback, save

---

## 3. Architecture Summary

| Service | Port | Apps | Purpose |
|---------|------|------|---------|
| Auth | 8001 | accounts, profiles | Login, Signup, User API |
| Assignment | 8002 | assignments | Create/list assignments |
| Submission | 8003 | submissions | Submit/edit student work |
| Grading | 8004 | grading, student_dashboard, teacher_dashboard | Dashboards & grading |

### Key Design Decisions
- **Shared `SECRET_KEY`**: All services use the same key so Django sessions work across ports.
- **Shared `db.sqlite3`**: Single database in the project root, referenced by all services.
- **`MicroserviceAuthMiddleware`**: Each non-auth service has middleware that reads `_auth_user_id` from the Django session and looks up the user in `accounts_user` via direct SQL. This avoids needing the `accounts` app in every service.
- **`LOGIN_URL`**: Non-auth services redirect to `http://localhost:8001/accounts/login/` for authentication.
- **REST APIs**: Each service exposes DRF endpoints (e.g. `/assignments/api/`, `/submissions/api/`) for inter-service communication.
