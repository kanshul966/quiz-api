---

# 🎮 Quiz API

A Flask-based REST API that serves quiz questions from multiple categories (Anime, Games, World Capitals, Python).
It uses **MongoDB Atlas** for data storage and a **key-based access system** with expiration time validation.

---

## 🚀 Features

* 🔑 **API Key authentication** with expiry time.
* 📚 Supports multiple quiz categories:

  * Anime
  * Games
  * WorldCapital
  * Python
* 🎲 Randomized quiz question selection.
* 🛡️ Error handling for invalid/missing parameters.
* 🖼️ Simple landing page with `/` route.

---

## 📦 Requirements

* Python 3.8+
* Flask
* PyMongo

Install dependencies:

```bash
pip install flask pymongo
```

---

## ⚙️ Setup

1. **Clone repository**

   ```bash
   git clone https://github.com/kanshul966/quiz-api.git
   cd quiz-api
   ```

2. **Configure MongoDB**

   * Replace `MONGO URL` with your own MongoDB connection string.
   * Ensure your MongoDB has the following databases/collections:

     * `Quiz.Anime`
     * `Quiz.Games`
     * `Quiz.WorldCapital`
     * `Quiz.Python`
     * `KeysDatabase.KeyDatabase` (for storing API keys)

3. **Run the API**

   ```bash
   python app.py
   ```

   The server will run on `http://0.0.0.0:<random_port>` (between 2000–9000).

---

## 🔑 API Key System

Each client must provide a valid **API key** (`apikey`) stored in `KeysDatabase.KeyDatabase`.

Example document in `KeyDatabase`:

```json
{
  "apikey": "your-api-key",
  "time": "2025-09-10 23:59:59"
}
```

* `apikey`: Unique key for authentication.
* `time`: Expiry timestamp (format: `YYYY-MM-DD HH:MM:SS`).

---

## 📖 API Usage

### Endpoint:

```
GET /api/v1/quiz?apikey=<your_key>&QuizType=<category>
```

### Parameters:

* `apikey` → Your API key.
* `QuizType` → One of: `Anime`, `Games`, `WorldCapital`, `Python`.

### Example Request:

```bash
curl "http://localhost:5000/api/v1/quiz?apikey=test123&QuizType=Anime"
```

### Example Response (200 OK):

```json
{
  "Api:Message": "Request successfully validated.",
  "questions": {
    "question": "Who is the main character of Naruto?",
    "options": ["Naruto", "Sasuke", "Kakashi", "Sakura"],
    "answer": "Naruto"
  },
  "validtill": "2025-09-10 23:59:59",
  "code": 200
}
```

---

## ⚠️ Error Codes

| Code | Message                       |
| ---- | ----------------------------- |
| 400  | Missing/invalid parameters    |
| 403  | Invalid API key / Expired key |
| 404  | No quiz questions available   |
| 500  | Unknown server error          |

---



## 📜 License

MIT License © 2025 \[Your Name]

---

