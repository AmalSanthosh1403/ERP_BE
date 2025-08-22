# API Documentation – User & Role Management -->

This project provides APIs for user management and role management with JWT authentication.
Only admins can manage roles and users, while employees can be created without roles.

##  Authentication APIs
### 1. Login

URL: /login/

Method: POST

Description: Login with username & password to get JWT tokens.

Request Body:

{
  "username": "admin",
  "password": "admin123"
}


Response:

{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
  "user_id": 9,
  "username": "admin1",
  "role": "admin_role"
}

### 2. Refresh Token

URL: /refresh/

Method: POST

Description: Get a new access token using refresh token.

Request Body:

{
  "refresh": "your_refresh_token"
}


Response:

{
  "access": "new_access_token"
  "refresh": "new_refresh_token"
}

### 3. Logout

URL: /logout/

Method: POST

Description: Blacklist the refresh token and logout the user.

Request Body:

{
  "refresh": "your_refresh_token"
}


Response:

{
  "message": "Logged out successfully"
}

## User Management APIs
### 1. List Users

URL: /users/

Method: GET

Auth Required: ✅ Yes (Admin only)

Response:

[
  {
    "id": 1,
    "username": "employee1",
    "email": "emp1@example.com",
    "role": null
  },
  {
    "id": 2,
    "username": "manager1",
    "email": "manager@example.com",
    "role": {
      "id": 2,
      "name": "Manager",
      "code": "manager"
    }
  }
]

### 2. Create User

URL: /users/

Method: POST

Auth Required: ✅ Yes (Admin only)

Request Body:

{
  "username": "employee2",
  "email": "emp2@example.com",
  "password": "test123",
   "role_id": null
}


Response:

{
  "id": 3,
  "username": "employee2",
  "email": "emp2@example.com",
  "role": null
}

### 3. Update User

URL: /users/{id}/

Method: PATCH

Auth Required: ✅ Yes (Admin only)

Request Body (example):

{
  "email": "newmail@example.com"
}


Response:

{
  "id": 3,
  "username": "employee2",
  "email": "newmail@example.com",
  "role": null
}

### 4. Delete User

URL: /users/{id}/

Method: DELETE

Auth Required: ✅ Yes (Admin only)

Response (Success):

{
  "message": "User deleted successfully"
}


Response (Not Found):

{
  "error": "User not found"
}

### 5. Employee List
GET /users/list_employee/

Fetch all users with a role having is_employee flag.

Response (200)

[
  {
    "id": 3,
    "username": "employee1",
    "email": "emp1@example.com",
    "role": null
  },
  {
    "id": 4,
    "username": "employee2",
    "email": "emp2@example.com",
    "role": null
  }
]

### 6. Profile (Current User)

GET /users/profile/

Headers: Authorization: Bearer <access_token>

Response (200)

{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": {
    "id": 1,
    "name": "Admin",
    "permissions": ["list", "create", "delete"]
  }
}


## Role Management APIs
### 1. List Roles

URL: /roles/

Method: GET

Auth Required: ✅ Yes (Admin only)

Response:

[
  {
    "id": 1,
    "name": "Admin",
    "code": "admin"
  },
  {
    "id": 2,
    "name": "Manager",
    "code": "manager"
  }
]

### 2. Create Role

URL: /roles/

Method: POST

Auth Required: ✅ Yes (Admin only)

Request Body:

{
  "name": "Manager Role1",
  "code": "manager_role1",
  "permission_ids": [6],
  "is_employee": true      <!-- true only for managers and employees  -->
}


Response:

{
  "id": 2,
  "name": "Manager",
  "code": "manager"
}

### 3. Update Role

URL: /roles/{id}/

Method: PATCH

Auth Required: ✅ Yes (Admin only)

Request Body:

{
  "name": "Project Manager"
}


Response:

{
  "id": 2,
  "name": "Project Manager",
  "code": "manager"
}

### 4. Delete Role

URL: /roles/{id}/

Method: DELETE

Auth Required: ✅ Yes (Admin only)

Response (Success):

{
  "message": "Role deleted successfully"
}

