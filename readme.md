# Django RBAC System with JWT Authentication

A simple Role-Based Access Control (RBAC) system built using Django REST Framework and JWT authentication.  
This project allows admins to create roles with specific permissions and assign them to users.  

---

## 🚀 Features
- User authentication using JWT (access & refresh tokens)
- Role management (create, update, delete roles)
- Permission management (stored in DB, seeded via script)
- Assign roles to users
- Token-based login, logout & refresh
- Admin-only role & user creation

---

## 🛠️ Tech Stack
- Backend: Django, Django REST Framework
- Authentication: JWT (`djangorestframework-simplejwt`)
- Database: PostgreSQL


---

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/your-username/rbac-system.git
cd rbac-system

### 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run migrations
python manage.py migrate

### 5. Seed initial data
<!-- Seed permissions: -->
python manage.py runscript seed_rbac
<!-- Seed admin role & one admin user: -->
python manage.py runscript seed_rbac

The default admin user created(not superuser):

### 1. Clone the repository


### 1. Clone the repository
### 1. Clone the repository
### 1. Clone the repository
### 1. Clone the repository
