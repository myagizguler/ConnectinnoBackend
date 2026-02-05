# Postman Request Examples

Base URL: `http://localhost:8000`  
Notes istekleri için önce **Register** veya **Login** yapıp yanıttaki **id_token** değerini alın; tüm Notes isteklerinde `Authorization: Bearer <id_token>` kullanın.

---

## 1. POST /register

**Method:** `POST`  
**URL:** `http://localhost:8000/register`

**Headers:**

| Key          | Value             |
|--------------|-------------------|
| Content-Type | application/json  |

**Body:** raw → JSON

```json
{
  "email": "test@example.com",
  "password": "password123",
  "display_name": "Test User"
}
```

`display_name` isteğe bağlı. Şifre en az 6 karakter.

---

## 2. POST /login

**Method:** `POST`  
**URL:** `http://localhost:8000/login`

**Headers:**

| Key          | Value             |
|--------------|-------------------|
| Content-Type | application/json  |

**Body:** raw → JSON

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

---

## 3. GET /notes

**Method:** `GET`  
**URL:** `http://localhost:8000/notes`

**Headers:**

| Key            | Value                    |
|----------------|--------------------------|
| Authorization  | Bearer \<id_token\>      |
| Content-Type   | application/json        |

Body yok.

---

## 4. POST /notes (Create note)

**Method:** `POST`  
**URL:** `http://localhost:8000/notes`

**Headers:**

| Key            | Value                    |
|----------------|--------------------------|
| Authorization  | Bearer \<id_token\>      |
| Content-Type   | application/json        |

**Body:** raw → JSON

```json
{
  "title": "My first note",
  "content": "This is the note content. You can write longer text here.",
  "is_pinned": false
}
```

- `title`: zorunlu, 1–256 karakter  
- `content`: isteğe bağlı, varsayılan `""`, max 50.000 karakter  
- `is_pinned`: isteğe bağlı, varsayılan `false`  

**Minimal örnek (sadece title):**

```json
{
  "title": "Minimal note"
}
```

---

## 5. PUT /notes/{id} (Update note)

**Method:** `PUT`  
**URL:** `http://localhost:8000/notes/{id}`  

Örnek: `http://localhost:8000/notes/abc123xyz`  
`{id}` yerine Create note yanıtındaki `id` değerini yazın.

**Headers:**

| Key            | Value                    |
|----------------|--------------------------|
| Authorization  | Bearer \<id_token\>      |
| Content-Type   | application/json        |

**Body:** raw → JSON (sadece güncellemek istediğiniz alanları gönderin)

```json
{
  "title": "Updated title",
  "content": "Updated content.",
  "is_pinned": true
}
```

**Sadece title güncelleme:**

```json
{
  "title": "New title only"
}
```

**Sadece content güncelleme:**

```json
{
  "content": "New content only"
}
```

---

## 6. DELETE /notes/{id}

**Method:** `DELETE`  
**URL:** `http://localhost:8000/notes/{id}`  

Örnek: `http://localhost:8000/notes/abc123xyz`  
`{id}` yerine silmek istediğiniz notun `id` değerini yazın.

**Headers:**

| Key            | Value                    |
|----------------|--------------------------|
| Authorization  | Bearer \<id_token\>      |

Body yok.

---

## Kullanım sırası (Postman)

1. **POST /register** veya **POST /login** gönderin.
2. Yanıttaki **id_token** değerini kopyalayın.
3. Collection’da (veya environment’ta) **firebase_id_token** değişkenine yapıştırın.
4. **GET /notes**, **POST /notes**, **PUT /notes/{id}**, **DELETE /notes/{id}** isteklerinde `Authorization: Bearer {{firebase_id_token}}` kullanın.
5. **POST /notes** sonrası dönen **id** değerini **note_id** değişkenine yazın; PUT ve DELETE’te `{{note_id}}` kullanın.
