# Implementation Plan - Split College Management into Microservices

This plan outlines the steps to decompose the current monolithic Django project into four independent microservices.

## User Review Required

> [!IMPORTANT]
> As requested, we will use a **single shared database** for all services.
> However, to maintain a microservices architecture, services will **not** query each other's tables directly. Instead, they will use API calls to request data from the owning service.

## Proposed Changes

### Phase 1: Foundation & Project Initialization
- Create 4 independent Django projects: `auth_service`, `assignment_service`, `submission_service`, and `grading_service`.
- Initialize each with `django-admin startproject`.
- Install `djangorestframework` and `requests` in the environment.

### Phase 2: App Migration
Move the existing apps into their respective service directories:
1. **Auth Service**: `accounts`, `profiles`
2. **Assignment Service**: `assignments`
3. **Submission Service**: `submissions`
4. **Grading Service**: `grading`, `student_dashboard`, `teacher_dashboard`

### Phase 3: Model Refactoring (Decoupling)
- **Submission Service**: Replace `ForeignKey` to `Assignment` with `assignment_id` (Integer).
- **Grading Service**: Replace direct imports of `Submission` and `Assignment` with API client calls.
- **Cross-Service Auth**: Replace `ForeignKey(User)` with `user_id` (Integer). We will implement a utility to fetch user info from the Auth Service.

### Phase 4: API Implementation (Django REST Framework)
- Create Serializers and API views for each service to expose required data.
- **Auth Service**: `/api/users/<id>/`
- **Assignment Service**: `/api/assignments/<id>/`
- **Submission Service**: `/api/submissions/<id>/`

### Phase 5: Inter-Service Communication
- Create a `service_clients.py` utility in each service that needs to talk to others.
- Use `requests` to perform HTTP calls between services.
- Update views in `grading_service`, `student_dashboard`, and `teacher_dashboard` to use these clients instead of direct model queries.

### Phase 6: URL & Settings Configuration
- Configure all services to point to the **same shared SQLite database** (initially).
- Set up `INSTALLED_APPS` and `URL` patterns for each service.
- Each service will only include the `INSTALLED_APPS` relevant to its domain.

## Verification Plan

### Automated Tests
- Run `python manage.py test` in each service directory.
- Verify API endpoints using `curl` or browser.

### Manual Verification
1. Start `auth_service` on port 8001.
2. Start `assignment_service` on port 8002.
3. Start `submission_service` on port 8003.
4. Start `grading_service` on port 8004.
5. Perform a full workflow: Login -> Create Assignment -> Submit -> Grade.
