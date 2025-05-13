# 🕑 Remind Me Later

A Django application to schedule and send **reminders** via **email** and **SMS**. It uses **Celery** and **Redis** to handle background tasks, with secure **user authentication** and integration with **Twilio** for SMS and **SMTP** for email.

---
![Screenshot 2025-05-13 201559](https://github.com/user-attachments/assets/83e6a445-4836-4d98-a27e-9bc66f91f2a0)
![Screenshot 2025-05-13 201611](https://github.com/user-attachments/assets/be203253-8914-4f2d-9e5c-dd1e3fc47af2)
![Screenshot 2025-05-13 201637](https://github.com/user-attachments/assets/5e50ba2e-b42c-43cb-9c36-912552bef22b)


## 📌 Table of Contents

- [🔧 Features](#-features)
- [⚙️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🔄 Application Flow](#-application-flow)
- [🚀 Setup Instructions](#-setup-instructions)
- [🧠 Usage Guide](#-usage-guide)
- [🧪 Testing](#-testing)
- [📬 Reminder Task Example](#-reminder-task-example)
- [📎 License](#-license)

---

## 🔧 Features

- ✅ User registration, login, and logout (Django auth)
- 📝 Users can create reminders with:
  - Message content
  - Date and time to send
  - Delivery method: Email, SMS, or both
- 🔄 Background job processing with Celery and Redis
- 📧 Email reminders using SMTP (Gmail, etc.)
- 📱 SMS reminders using Twilio
- 🔐 Secure configuration with environment variables

---

## ⚙️ Tech Stack

| Component       | Technology           |
|----------------|----------------------|
| Backend         | Django               |
| Task Queue      | Celery               |
| Broker          | Redis                |
| SMS Service     | Twilio               |
| Email Service   | SMTP (Gmail/Yahoo)   |
| Authentication  | Django User Model    |
| Scheduler       | Celery Beat (optional) |
| Database        | SQLite / PostgreSQL  |

---

## 📂 Project Structure

remind_me_later/
├── manage.py
├── .env # Secret keys and configs
├── requirements.txt
├── remind_me/ # Django project
│ ├── init.py # Initializes Celery
│ ├── settings.py
│ ├── urls.py
│ ├── celery.py # Celery config
├── reminders/ # App for reminders
│ ├── models.py # Reminder model
│ ├── views.py # Create/view/delete reminders
│ ├── tasks.py # Celery task logic
│ ├── forms.py
│ ├── templates/reminders/
│ ├── urls.py

markdown
Copy
Edit

---

## 🔄 Application Flow

1. **User signs up / logs in**
   - Auth handled by Django
2. **User creates a reminder**
   - Inputs message, date/time, and delivery method
3. **Reminder saved to DB**
4. **Celery task scheduled**
   - Based on the `send_time`, Celery will run `send_reminder`
5. **Redis** as the **message broker** queues the task
6. **At scheduled time:**
   - If `via_email`, sends email
   - If `via_sms`, sends SMS using Twilio

---

## 🚀 Setup Instructions

### 1. Clone and Setup Environment

```bash
git clone https://github.com/yourusername/remind-me-later.git
cd remind-me-later
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
