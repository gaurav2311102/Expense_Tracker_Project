💰 Expense Tracker Backend
This is a simple backend system for an Expense Tracker application built with Django and Django Rest Framework (DRF). The application allows authenticated users to log in, record, view, and analyze their expenses over time.

📌 Features
✅ JWT-based authentication

✅ Secure login and protected endpoints

✅ Expense creation and filtering by date

✅ Expense analytics: totals, category-wise breakdown, and trends

🛠 Tech Stack
Language: Python 3.12.3

Framework: Django, Django REST Framework

Authentication: JWT via djangorestframework-simplejwt

Database: PostgreSQL 


🔐 Authentication

POST /api/login/
Authenticate a user and return a JWT token.

Body:

{
  "email": "user@example.com",
  "password": "your_password"
}

🗃 Models

User

id (auto), 
email (unique, required), 
phone_number (unique, optional), 
country_code (default = "+91"), 
full_name, 
password (hashed), 
date_joined (auto_add), 

Expense

id (auto),
user (foreign key to User),
amount (decimal),
category (string),
date (date),
description (string),

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/gaurav2311102/Expense_Tracker_Project.git
cd EXPENSE_TRACKER

2. Create Virtual Environment

python -m venv venv

On Windows: venv\Scripts\activate
on Linux: source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Setup Database

Edit settings.py to configure your database.

Run migrations:

python manage.py migrate

5. Run Server

python manage.py runserver
