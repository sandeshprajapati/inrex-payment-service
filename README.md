# Payment Wallet Service

A complete FastAPI-based REST API service for managing user wallets and fund transactions with PostgreSQL backend.

## 🚀 Features

- **Add funds** to user wallets with transaction recording
- **Withdraw funds** from wallets with balance validation
- **Check wallet balance** for any user
- **View complete transaction history** with filtering
- **PostgreSQL persistence** with SQLAlchemy ORM
- **Comprehensive error handling** and validation
- **Interactive API documentation** with Swagger UI
- **Modular architecture** with separation of concerns
- **Database transaction safety** with rollback on errors
- **Detailed logging** for all operations

## 📁 Project Structure

```
inrex-payment-service/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── wallet.py              # Wallet API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration settings
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                # Import all models
│   │   ├── base_class.py          # SQLAlchemy Base class
│   │   ├── init_db.py             # Database initialization
│   │   └── session.py             # Database session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py               # Transaction enums (CREDIT/DEBIT, SUCCESS/FAILED)
│   │   ├── user.py                # User model
│   │   ├── wallet.py              # Wallet model
│   │   └── transaction.py         # Transaction model
│   └── schemas/
│       ├── __init__.py
│       └── schemas.py             # Pydantic schemas for validation
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
├── README.md                      # This documentation
├── test_api.py                   # Comprehensive API tests
├── simple_test.py                # Basic connectivity test
└── API_EXAMPLES.md               # Additional API usage examples
```

## 🛠 Installation & Setup

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

- Ensure PostgreSQL is running
- Create database named 'payment':

```sql
CREATE DATABASE payment;
```

- Update connection string in `app/core/config.py` if needed:

```python
DATABASE_URL: str = "postgresql://username:password@localhost:5432/payment"
```

### 4. Initialize Database Tables

```bash
set PYTHONPATH=. && python -m app.db.init_db
```

### 5. Start the Server

```bash
set PYTHONPATH=. && uvicorn main:app --reload
```

Or directly:

```bash
set PYTHONPATH=. && python main.py
```

### 6. Verify Installation

- Health check: http://localhost:8000/health
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## 🔗 API Endpoints

### Core Wallet Operations

| Method | Endpoint                         | Description             | Request Body                                                  |
| ------ | -------------------------------- | ----------------------- | ------------------------------------------------------------- |
| `POST` | `/wallet/user`                   | Create new user         | `{"name": "John Doe"}`                                        |
| `POST` | `/wallet/addFunds`               | Add funds to wallet     | `{"user_id": 1, "amount": 100.0, "description": "Deposit"}`   |
| `POST` | `/wallet/withdrawFunds`          | Withdraw funds          | `{"user_id": 1, "amount": 25.0, "description": "Withdrawal"}` |
| `GET`  | `/wallet/balance/{user_id}`      | Get wallet balance      | -                                                             |
| `GET`  | `/wallet/transactions/{user_id}` | Get transaction history | Optional: `?limit=10`                                         |

### System Endpoints

| Method | Endpoint  | Description                     |
| ------ | --------- | ------------------------------- |
| `GET`  | `/`       | Root endpoint with service info |
| `GET`  | `/health` | Detailed health check           |

## 📝 API Usage Examples

### 1. Create a User

```bash
curl -X POST "http://localhost:8000/wallet/user" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe"
}
```

### 2. Add Funds to Wallet

```bash
curl -X POST "http://localhost:8000/wallet/addFunds" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "amount": 100.50,
    "description": "Initial deposit"
  }'
```

**Response:**

```json
{
  "id": 1,
  "user_id": 1,
  "type": "CREDIT",
  "amount": 100.5,
  "timestamp": "2025-08-22T11:45:00.123456",
  "status": "SUCCESS",
  "description": "Initial deposit"
}
```

### 3. Withdraw Funds

```bash
curl -X POST "http://localhost:8000/wallet/withdrawFunds" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "amount": 25.00,
    "description": "ATM withdrawal"
  }'
```

### 4. Check Balance

```bash
curl -X GET "http://localhost:8000/wallet/balance/1"
```

**Response:**

```json
{
  "wallet_id": 1,
  "balance": 75.5
}
```

### 5. Get Transaction History

```bash
curl -X GET "http://localhost:8000/wallet/transactions/1"
```

**Response:**

```json
{
  "user_id": 1,
  "transactions": [
    {
      "id": 2,
      "user_id": 1,
      "type": "DEBIT",
      "amount": 25.0,
      "timestamp": "2025-08-22T11:46:00.123456",
      "status": "SUCCESS",
      "description": "ATM withdrawal"
    },
    {
      "id": 1,
      "user_id": 1,
      "type": "CREDIT",
      "amount": 100.5,
      "timestamp": "2025-08-22T11:45:00.123456",
      "status": "SUCCESS",
      "description": "Initial deposit"
    }
  ]
}
```

### 6. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## 🗃️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

### Wallets Table

```sql
CREATE TABLE wallets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    balance FLOAT DEFAULT 0.0 NOT NULL
);
```

### Transactions Table

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    type VARCHAR(6) NOT NULL CHECK (type IN ('CREDIT', 'DEBIT')),
    amount FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(7) NOT NULL CHECK (status IN ('SUCCESS', 'FAILED')),
    description VARCHAR(255)
);
```

## ✅ Features Implemented

### Core Requirements

- ✅ **POST** `/wallet/addFunds` → Add funds to user account
- ✅ **POST** `/wallet/withdrawFunds` → Withdraw funds from user account
- ✅ **GET** `/wallet/balance/{userId}` → Fetch current wallet balance
- ✅ **GET** `/wallet/transactions/{userId}` → Fetch transaction history

### Database & Models

- ✅ PostgreSQL integration with SQLAlchemy
- ✅ Users table (id, name)
- ✅ Wallets table (id, user_id, balance)
- ✅ Transactions table (id, user_id, type, amount, timestamp, status, description)
- ✅ CREDIT/DEBIT transaction types
- ✅ SUCCESS/FAILED transaction statuses

### Validation & Error Handling

- ✅ Pydantic models for request/response validation
- ✅ **Balance validation** (cannot withdraw more than available)
- ✅ Proper HTTP status codes (200, 201, 400, 404, 500)
- ✅ Comprehensive error messages
- ✅ Database transaction rollback on errors

### Additional Features

- ✅ Modular architecture (separate routes, models, database)
- ✅ Comprehensive logging with timestamps
- ✅ **Swagger/OpenAPI documentation** at `/docs`
- ✅ **ReDoc documentation** at `/redoc`
- ✅ Health check endpoints
- ✅ CORS support
- ✅ Database session management
- ✅ CASCADE delete for related records

## 🧪 Testing

### Automated Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

### Basic Connectivity Test

```bash
python simple_test.py
```

### Manual Testing

Use the interactive Swagger UI at: http://localhost:8000/docs

## 📊 Error Handling

The API returns appropriate HTTP status codes and error messages:

### Common Error Responses

**User Not Found (404):**

```json
{
  "detail": "User not found"
}
```

**Insufficient Funds (400):**

```json
{
  "detail": "Insufficient balance. Available: $75.5, Requested: $200.0"
}
```

**Wallet Not Found (404):**

```json
{
  "detail": "Wallet not found"
}
```

**Server Error (500):**

```json
{
  "detail": "Error processing transaction"
}
```

## 📈 Performance Features

- **Database Connection Pooling** with SQLAlchemy
- **Transaction Safety** with automatic rollback
- **Efficient Queries** with proper indexing
- **Session Management** with automatic cleanup
- **Request Validation** with Pydantic models

## 🔒 Security Features

- **Input Validation** with Pydantic schemas
- **SQL Injection Protection** with SQLAlchemy ORM
- **Transaction Atomicity** ensuring data consistency
- **Error Handling** without sensitive data exposure
- **CORS Support** for cross-origin requests

## 📚 Dependencies

```
fastapi==0.104.1       # Modern web framework
uvicorn==0.24.0        # ASGI server
sqlalchemy==2.0.23     # ORM for database operations
psycopg2-binary==2.9.9 # PostgreSQL adapter
pydantic==2.5.0        # Data validation
pydantic-settings==2.1.0 # Settings management
python-multipart==0.0.6  # Form data support
requests==2.31.0       # HTTP client (for testing)
```

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment Variables** for sensitive configuration
2. **Rate Limiting** to prevent abuse
3. **Authentication/Authorization** for user access control
4. **Database Connection Pooling** optimization
5. **Monitoring and Logging** integration
6. **SSL/TLS Termination** for secure connections
7. **Load Balancing** for scalability
8. **Database Backups** and disaster recovery

## 📧 API Documentation

- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🛠 Development

### Adding New Features

1. Create models in `app/models/`
2. Add schemas in `app/schemas/`
3. Implement routes in `app/api/`
4. Update database initialization in `app/db/`
5. Add tests in test files

### Database Migrations

For schema changes, use SQLAlchemy migrations:

```bash
# Install alembic for migrations
pip install alembic

# Initialize migrations
alembic init migrations

# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with FastAPI, SQLAlchemy, and PostgreSQL** 🚀
