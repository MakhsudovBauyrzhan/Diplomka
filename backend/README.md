# Tour Booking Platform API

A Django REST Framework backend for a tour booking platform where users can create, discover, and book tours.

## Features

- User registration and authentication with JWT
- Email verification
- Tour creation and management
- Tour discovery with filtering and search
- Tour participation management
- Payment processing and refunds
- Payouts to tour creators

## Technology Stack

- Python 3.9+
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Pillow for image processing

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database:
```sql
CREATE DATABASE tourdb;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tourdb TO postgres;
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `POST /api/users/register/` - Register a new user
- `POST /api/users/verify-email/` - Verify email with token
- `POST /api/users/resend-verification/` - Resend verification email
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/update/` - Update user profile
- `PUT /api/users/change-password/` - Change password

### Tours
- `GET /api/tours/` - List all tours
- `POST /api/tours/` - Create a new tour
- `GET /api/tours/{id}/` - Get tour details
- `PUT /api/tours/{id}/` - Update a tour
- `DELETE /api/tours/{id}/` - Delete a tour
- `POST /api/tours/{id}/join/` - Join a tour
- `POST /api/tours/{id}/leave/` - Leave a tour
- `GET /api/tours/my_tours/` - List user's created tours
- `GET /api/tours/participating/` - List tours user is participating in
- `GET /api/tours/{tour_id}/participants/` - List participants of a tour

### Payments
- `GET /api/payments/payments/` - List user's payments
- `POST /api/payments/payments/` - Create a new payment
- `GET /api/payments/payments/{id}/` - Get payment details
- `POST /api/payments/payments/{id}/refund/` - Refund a payment
- `GET /api/payments/payouts/` - List user's payout requests
- `POST /api/payments/payouts/` - Create a new payout request
- `GET /api/payments/payouts/{id}/` - Get payout request details
- `POST /api/payments/payouts/{id}/process/` - Process a payout request
- `GET /api/payments/transactions/` - List user's transactions

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@localhost:5432/tourdb
FRONTEND_URL=http://localhost:3000
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
``` 