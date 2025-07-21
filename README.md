# 🌆 Urban Share - Urban Resource Sharing Platform

Urban Share is a Django-based web application that enables users in urban areas to share, lend, rent, or borrow resources such as tools, appliances, spaces, and services. The platform encourages sustainability and builds community connections through responsible sharing.

---

## 🚀 Features

- 🔐 User registration, login, and session/JWT authentication
- 🛠️ List and manage shareable resources
- 🔍 Search and filter resources by location, category, availability
- 📆 Booking and availability management
- ⭐ Rating and feedback on each resource
- 💬 Messaging or contact system between users
- 📊 Admin dashboard for platform management
- 📧 Email confirmation and Notification for Booking request, approval and rejection

---

## 🏗️ Tech Stack

- **Backend:** Django, Django REST Framework, Django Channels
- **Frontend:** Django Templates (or integrate React/Vue)
- **Database:** PostgreSQL
- **Auth:** Django session auth and JWT (via `djangorestframework-simplejwt`)
- **Env Management:** `python-decouple` or `django-environ`
- **Asynchronous Tasks:** Celery, Redis

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Nadeerpk/urban-share.git
cd urban-share
```

### 2. Setup virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
