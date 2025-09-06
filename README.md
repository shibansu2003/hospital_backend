# Hospital Backend Secure System

A secure hospital management backend built with Django REST Framework and PostgreSQL, providing APIs for patients, doctors, and their mappings. Authentication is handled via JWT tokens for secure communication.

## ✨ Features

- 🔐 JWT Authentication (Access & Refresh tokens)
- 👤 User Registration & Login
- 🩺 Manage Patients & Doctors
- 🔗 Map Patients to Doctors
- 🗄️ PostgreSQL Database Integration
- 🧪 Tested with Thunder Client / Postman

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Auth**: JWT (SimpleJWT)
- **Testing**: Thunder Client / Postman

## ⚙️ Installation

1️⃣ **Clone the repository**

```bash
git clone https://github.com/your-username/hospital-backend.git
cd hospital-backend
```

2️⃣ **Create virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

4️⃣ **Setup PostgreSQL**

```sql
CREATE DATABASE hospital_db;
CREATE USER hospital_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
```

Update `settings.py`:

```python
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
```

5️⃣ **Run migrations**

```bash
python manage.py migrate
```

6️⃣ **Create a superuser**

```bash
python manage.py createsuperuser
```

7️⃣ **Start the server**

```bash
python manage.py runserver
```

Server runs at 👉 http://127.0.0.1:8000

## 🔐 Authentication (JWT)

- **Register/Login** → Get access & refresh tokens
- **Use Access Token** → Add to headers:

```
Authorization: Bearer <access_token>
```

- **Refresh Token** → Get a new access token:

```
POST /api/auth/refresh/
{
  "refresh": "<your_refresh_token>"
}
```

## 📌 API Endpoints

### 🔑 Auth

| Method | Endpoint                | Description             |
|--------|-------------------------|-------------------------|
| POST   | /api/auth/register/     | Register new user       |
| POST   | /api/auth/login/        | Login & get tokens      |
| POST   | /api/auth/refresh/      | Refresh access token    |

### 🧑 Patients

| Method | Endpoint                | Description             |
|--------|-------------------------|-------------------------|
| GET    | /api/patients/          | List patients           |
| POST   | /api/patients/          | Add patient             |
| GET    | /api/patients/{id}/     | Get patient             |
| PUT    | /api/patients/{id}/     | Update patient          |
| DELETE | /api/patients/{id}/     | Delete patient          |

### 👨‍⚕️ Doctors

| Method | Endpoint                | Description             |
|--------|-------------------------|-------------------------|
| GET    | /api/doctors/           | List doctors            |
| POST   | /api/doctors/           | Add doctor              |
| GET    | /api/doctors/{id}/      | Get doctor              |
| PUT    | /api/doctors/{id}/      | Update doctor           |
| DELETE | /api/doctors/{id}/      | Delete doctor           |

### 🔗 Mappings

| Method | Endpoint                      | Description                  |
|--------|-------------------------------|------------------------------|
| GET    | /api/mappings/                | List mappings                |
| POST   | /api/mappings/                | Map patient ↔ doctor         |
| GET    | /api/mappings/{id}/           | Get mapping                  |
| GET    | /api/mappings/{patient_id}/   | Get mapping by patient       |

## 🧪 Testing with Thunder Client / Postman

1. **Register** → Get tokens
2. **Copy access token**
3. **Add header**:

```
Authorization: Bearer <access_token>
```

4. Call protected endpoints
5. Use refresh token when access token expires

## ⚡ Environment Variables

Create a `.env` file in the project root with the following structure:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=your_db_name
DB_USER=Your_db_user_name
DB_PASSWORD=Your_db_Password
DB_HOST=127.0.0.1
DB_PORT=5432

ACCESS_TOKEN_LIFETIME_MIN=30
REFRESH_TOKEN_LIFETIME_DAYS=1
```

## 🚀 Future Scope

- Role-based access (Admin, Doctor, Patient)
- Appointment scheduling
- Medical report uploads
- Logging & monitoring
