# 🧮 Inventory Management System

A full-featured **Inventory Management System** built with Django, Bootstrap, and SQLite. Designed to help businesses efficiently manage products, stock levels, and users — complete with authentication, admin dashboard, and deployment-ready code.

## 🚀 Features

- ✅ User Authentication (Login, Logout, Google OAuth)
- 📦 Product Management (Add, Edit, Delete, View)
- 🔍 Inventory Search & Filter by Name, Category, Quantity
- ⚠️ Low-Stock Alerts with Red Indicators
- 📊 Dashboard with Live Inventory Stats
- 📥 CSV Import / 📤 PDF Export of Product Data
- 🧾 Booking & Invoice System (optional)
- 🌐 Deployed on [Render](https://render.com/)
- 🔐 Secure with Environment Variables
- 💬 Future Enhancements: Multi-language, Role-based Access, Email Notifications

---

## 🏗️ Tech Stack

| Layer       | Technology                  |
|-------------|------------------------------|
| Backend     | Python, Django               |
| Frontend    | HTML5, CSS3, Bootstrap       |
| Database    | SQLite (dev), PostgreSQL (prod) |
| Auth        | Django Auth, Google OAuth    |
| Hosting     | Render.com                   |
| VCS         | Git + GitHub                 |

---

## 🔧 Setup Instructions

## 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Environment Variables
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

## 5. Run Migrations
python manage.py makemigrations
python manage.py migrate

## 6. Run Locally
python manage.py runserver

## 🌐 Deployment
Hosted On: Render
GitHub is connected to auto-deploy.
Gunicorn + Whitenoise for static files.
Use Render's Environment tab to set environment variables.

## 🙋‍♂️ Author
Ghani
🔗 LinkedIn | 📧 Email

### 1. Clone the Repo

```bash
git clone https://github.com/Ghani55-dev/inventory_web.git
cd inventory_web