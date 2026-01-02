# Development Guide - Heirs-PrivPark

## Project Structure

```
Heirs-PrivPark/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # API Routes
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database
│   │   └── schemas/        # Pydantic templates
│   ├── secrets/            # Firebase keys
│   ├── .env               # Environment variables
│   └── requirements.txt   # Python dependencies
├── mobile/                # Flutter app (to be created)
├── docs/                  # Documentation
├── test/                  # Automated testing
└── README.md
```

## Environment configuration

### 1. Backend (FastAPI)

```bash
# Virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Outbuildings
pip install -r backend/requirements.txt
```

### 2. PostgreSQL database

```sql
-- Create the database
CREATE DATABASE privpark;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE privpark TO postgres;
```

### 3. Firebase configuration

1. Create a Firebase project
2. Enable Authentication (Email/Telephone/Google)
3. Download the Admin SDK service key
4. Place in `backend/secrets/firebase_service_account.json`

### 4. Environment variables

Create `backend/.env` :

```env
ENV=dev
PROJECT_NAME=HeirsPrivPark
API_PREFIX=/api
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/privpark
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=backend/secrets/firebase_service_account.json
CORS_ORIGINS=*
```

## Starting the server

```bash
# Start the development server
python run_server.py

# Or directly with uvicorn
uvicorn app.main:app --app-dir backend --reload --port 8000
```

The server will be available on http://127.0.0.1:8000

## Tests

### Authentication tests

```bash
# Basic tests
python backend/app/test/test_auth.py

# Tests with Firebase token
python backend/app/test/test_auth.py YOUR_FIREBASE_TOKEN
```

### Manual tests with cURL

```bash
# Health check
curl http://127.0.0.1:8000/health

# Test with token
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://127.0.0.1:8000/api/users/me
```

## Development

### Adding new endpoints

1. Create the route in `backend/app/api/routes_*.py`
2. Add the diagrams to `backend/app/schemas/`
3. Add DB templates if necessary
4. Test with the test script

### Road structure

```python
from fastapi import APIRouter, Depends
from app.api.deps import verify_bearer_token_and_get_user

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/items")
def get_items(current_user = Depends(verify_bearer_token_and_get_user)):
    return {"items": []}
```

### Database models

```python
# backend/app/db/models/example.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
```

### Pydantic diagrams

```python
# backend/app/schemas/example.py
from pydantic import BaseModel

class ExampleBase(BaseModel):
    name: str

class ExampleOut(ExampleBase):
    id: int
    class Config:
        from_attributes = True
```

## Debugging

### Logs

The logs are displayed in the server console.

### Database

```bash
# Connecting to PostgreSQL
psql -h localhost -U postgres -d privpark

# See the tables
\dt

# View users
SELECT * FROM users;
```

### Firebase

Check the Firebase logs in the Firebase console.

## Deployment

### Production with Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build et run
docker build -t heirsprivpark-api .
docker run -p 8000:8000 heirsprivpark-api
```

## Best practices

### Code

- Using strict Python types
- Documenting functions with docstrings
- Follow PEP 8
- Test before committing

### Safety

- Never commit API keys
- Using environment variables
- Validate all user entries
- Implementing rate limiting in production

### Database

- Using Alembic migrations
- Create indexes on frequently used columns
- Make regular backups

## Troubleshooting

### Common errors

1. **PostgreSQL connection error**

   - Check that PostgreSQL is running
   - Check credentials in `.env`

2. **Firebase error**

   - Check that the key file exists
   - Check the PROJECT_ID

3. **CORS error**
   - Check the CORS_ORIGINS configuration
   - Add frontend origin

### Support

- View server logs
- Check the API documentation
- Create a GitHub issue if necessary

