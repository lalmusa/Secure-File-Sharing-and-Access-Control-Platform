# Secure File Sharing and Access Control Platform

## CIS 376 - Software Engineering II

A web-based application designed to securely upload, manage, and share files while enforcing authentication, file ownership, role-based access control, and audit logging.

## Project Overview

The Secure File Sharing and Access Control Platform provides users with a centralized application for managing and sharing files securely.

The system supports:

- User registration and login
- Secure password hashing using bcrypt
- File uploading and downloading
- File deletion
- Controlled file sharing between users
- File ownership tracking
- Role-based access control
- Administrative monitoring
- Audit logging
- Unauthorized access detection

The project was developed as an independent/solo project for CIS 376 - Software Engineering II.

## Features

### User Authentication

- Users can create an account.
- Passwords are stored as bcrypt password hashes.
- Users can log in and log out securely.
- Flask-Login manages authenticated sessions.
- Duplicate usernames are prevented.

### File Management

Authenticated users can:

- Upload files
- Download files they own
- Download files shared with them
- Delete files they own
- View their available files

### File Sharing

File owners can share files with other registered users.

The system prevents:

- Sharing files with nonexistent users
- Sharing a file with yourself
- Duplicate sharing records
- Unauthorized users from downloading files

### Role-Based Access Control

The system currently supports two roles:

- `user`
- `admin`

Regular users have access to normal file-management functionality.

Administrators have additional access to:

- The Admin Dashboard
- User information
- Audit logs
- The regular User Dashboard

Unauthorized users attempting to access the Admin Dashboard are denied access.

### Audit Logging

The application records important system activity, including:

- User registration
- User login
- User logout
- File uploads
- File downloads
- File sharing
- File deletion
- Unauthorized download attempts
- Unauthorized admin access attempts

Administrators can review these records through the Admin Dashboard.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- SQLite
- HTML5
- CSS3
- Jinja2
- Git
- GitHub

## Project Structure

```text
Project/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── audit.py
│   │
│   ├── auth/
│   │   ├── routes.py
│   │   └── decorators.py
│   │
│   ├── files/
│   │   └── routes.py
│   │
│   ├── admin/
│   │   └── routes.py
│   │
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── upload.html
│       └── admin_dashboard.html
│
├── uploads/
│
├── config.py
├── run.py
├── requirements.txt
└── README.md

Installation
1. Clone the Repository

git clone <repository-url>
cd Project

2. Create a Virtual Environment

Windows:

python -m venv venv

Activate it using Git Bash:

source venv/Scripts/activate

Or using Command Prompt:

venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure the Application

Make sure the application configuration contains the required Flask settings, including:

Secret key
SQLite database location
Upload folder
Running the Application

Start the Flask application with:

python run.py

The application should be available at:

http://127.0.0.1:5000/

The root page redirects users to the login/dashboard workflow.

Initial Users

For testing, the project uses accounts such as:

Username	Role
test1	admin
test2	user

These accounts were used to test authentication, file sharing, role-based access control, and unauthorized access.

Testing

Testing included:

Authentication Testing
Successful registration
Duplicate username rejection
Successful login
Invalid password rejection
Logout
File Testing
File upload
File download
File deletion
File sharing
Unauthorized file download
Role-Based Access Testing

The RBAC functionality was tested using two accounts.

test1

Role: admin
Can access the Admin Dashboard
Can access the regular User Dashboard

test2

Role: user
Can access the regular User Dashboard
Cannot access the Admin Dashboard

Unauthorized attempts to access administrative functionality are blocked and recorded in the audit log.

Security

The application includes several security measures:

Password hashing using bcrypt
Flask-Login session management
Login-required route protection
Role-based authorization
File ownership verification
File-sharing permission checks
Unauthorized access rejection
Audit logging
Database relationships using foreign keys
Deployment

The project is currently designed for local deployment using the Flask development server.

Deployment steps:

python run.py

The application then runs locally through:

http://127.0.0.1:5000/