# Auth – Register & Login (bu API üzerinden)

Notes API 401 veriyorsa önce **bu backend API** ile kayıt olup **id_token** alın; sonra Notes isteklerinde `Authorization: Bearer <id_token>` kullanın.

---

## 1. Register (Yeni hesap)

**Method:** `POST`  
**URL:** `http://localhost:8000/register` (veya `{{base_url}}/register`)

**Headers:**

| Key           | Value             |
|---------------|-------------------|
| Content-Type  | application/json  |

**Body (raw JSON):**

```json
{
  "email": "test@example.com",
  "password": "password123",
  "display_name": "Test User"
}
```

- `email`: Geçerli e-posta (zorunlu).
- `password`: En az 6 karakter (zorunlu).
- `display_name`: İsteğe bağlı.

**Başarılı yanıt (201):**

```json
{
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "refresh_token": "AOEOulZ...",
  "uid": "abc123...",
  "email": "test@example.com",
  "expires_in": 3600
}
```

- **id_token** → Notes API’de kullanın: `Authorization: Bearer <id_token>`

---

## 2. Login (Mevcut hesap)

**Method:** `POST`  
**URL:** `http://localhost:8000/login` (veya `{{base_url}}/login`)

**Headers:**

| Key           | Value             |
|---------------|-------------------|
| Content-Type  | application/json  |

**Body (raw JSON):**

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Yanıtta yine `id_token` döner; onu Notes API’de kullanın.

---

## 3. Notes API’de kullanım

1. **POST /register** veya **POST /login** isteğini atın.
2. Yanıttaki **id_token** değerini kopyalayın.
3. Notes isteklerinde header: `Authorization: Bearer <id_token>`

Postman’de `firebase_id_token` değişkenine bu değeri yapıştırırsanız tüm Notes istekleri bu token’ı kullanır.

---

## Backend ayarı

Register/Login’in id_token döndürmesi için backend’de **FIREBASE_WEB_API_KEY** tanımlı olmalı:

- Firebase Console → Project settings → General → Your apps → **Web API Key**
- `.env` içine: `FIREBASE_WEB_API_KEY=AIza...`

---

## Hata yanıtları

| HTTP | Anlamı |
|------|--------|
| 409  | Email already registered → /login kullanın. |
| 401  | Invalid email or password. |
| 503  | Auth not configured (FIREBASE_WEB_API_KEY). |
