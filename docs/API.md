# Documentation API - Heirs-PrivPark

## Base URL

```
http://127.0.0.1:8000  # Développement
https://api.heirsprivpark.com  # Production
```

## Authentification

All protected endpoints require an authorisation header. :

```
Authorization: Bearer <FIREBASE_ID_TOKEN>
```

## Endpoints

### Service health

#### GET /health

Check the status of the API.

**Response:**

```json
{
  "status": "ok"
}
```

---

### Authentification

#### POST /api/auth/verify-token

Verify a Firebase token and return user information.

**Headers:**

- `Authorization: Bearer <FIREBASE_ID_TOKEN>`

**Response:**

```json
{
  "user_id": 1,
  "firebase_uid": "abc123...",
  "email": "user@example.com",
  "message": "Token valide"
}
```

#### POST /api/auth/login

User login (alias for verify-token).

**Headers:**

- `Authorization: Bearer <FIREBASE_ID_TOKEN>`

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "photo_url": "https://...",
  "role": "user",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### POST /api/auth/logout

Disconnection (symbolic, the actual disconnection occurs on the client side).

**Response:**

```json
{
  "message": "Logout réussi",
  "note": "Veuillez vous déconnecter depuis l'application mobile"
}
```

#### GET /api/auth/me

Retrieve information about the logged-in user.

**Headers:**

- `Authorization: Bearer <FIREBASE_ID_TOKEN>`

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "photo_url": "https://...",
  "role": "user"
}
```

---

### Users

#### GET /api/users/me

Retrieve the detailed profile of the logged-in user.

**Headers:**

- `Authorization: Bearer <FIREBASE_ID_TOKEN>`

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Doe",
  "photo_url": "https://...",
  "role": "user"
}
```

#### PUT /api/users/me

Edit the profile of the logged-in user.

**Headers:**

- `Authorization: Bearer <FIREBASE_ID_TOKEN>`

**Body:**

```json
{
  "display_name": "John Smith",
  "photo_url": "https://new-photo.com/avatar.jpg"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "display_name": "John Smith",
  "photo_url": "https://new-photo.com/avatar.jpg",
  "role": "user"
}
```

---

## Error codes

| Code | Description                                |
| ---- | ------------------------------------------ |
| 200  | Success                                     |
| 401  | Not authorised (invalid/missing token)      |
| 403  | Access denied (insufficient permissions) |
| 422  | Validation error                      |
| 500  | Server error                             |

## Examples of use

### JavaScript/Fetch

```javascript
const token = "YOUR_FIREBASE_ID_TOKEN";

// Retrieve user profile
const response = await fetch("http://127.0.0.1:8000/api/users/me", {
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
});

const user = await response.json();
console.log(user);
```

### Python/Requests

```python
import requests

token = "YOUR_FIREBASE_ID_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Check the token
response = requests.post(
    "http://127.0.0.1:8000/api/auth/verify-token",
    headers=headers
)
print(response.json())
```

### cURL

```bash
# Health check
curl http://127.0.0.1:8000/health

# Retrieve profile
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://127.0.0.1:8000/api/users/me
```

## Swagger/OpenAPI

Interactive documentation is available at :

- **Development**: http://127.0.0.1:8000/docs
- **Production**: https://api.heirsprivpark.com/docs

