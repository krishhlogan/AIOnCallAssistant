# 🤖 AI On-Call Assistant

An intelligent, production-ready assistant to triage customer emails using LLMs (like Gemini), YAML-based playbooks, and modular tools like shell command execution and Slack/email notifications.

## 🚀 Features

* 🧠 LLM-powered issue inference from email subject/body
* 📅 FastAPI endpoint to receive email data
* 📟 YAML playbooks to define fix actions
* 🛠️ Shell/HTTP command execution
* 🧵 Background processing with Celery & Redis
* 🔌 Modular agent architecture using MCP protocol
* 🐳 Docker Compose for easy local development

---

## 💠 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-org/ai-oncall-assistant.git
cd ai-oncall-assistant
```

### 2. Configure Environment Variables

Create a `.env` file at the root level:

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=gemini
```

Make sure `.env` is in `.gitignore` (already handled).

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

This will start:

* `api`: FastAPI server (port 8000)
* `worker`: Celery background worker
* `redis`: Queue backend

---

## 📩 API Usage

### `POST /submit-email`

Ingests an email with subject/body and triggers background processing based on inferred issue type.

#### Query Params

* `llm_provider`: `gemini` or `openai`

#### Request Body (JSON)

```json
{
  "subject": "Ref ID: 258516012723 -- Ticket No: 933691",
  "sender": "jane.doe@example.com",
  "body": "Hi,\n\nI am Jane Doe. My mobile number is 9876543210 and policy number is PL-78654321. Today coins got deducted twice from my wallet.\n\nRegards,\nJane"
}
```

---

## 🦚 Test the Email Submission Endpoint

You can test the assistant locally using these `curl` commands:

### 🔀 Double Deduction Example

```bash
curl -X POST "http://localhost:8000/submit-email?llm_provider=gemini" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Ref ID: 258516012723 -- Ticket No: 933691",
    "sender": "jane.doe@example.com",
    "body": "Hi,\n\nI am Jane Doe. My mobile number is 9876543210 and policy number is PL-78654321. Today coins got deducted twice from my wallet.\n\nRegards,\nJane"
  }'
```

### 🔄 Sync Issue Example

```bash
curl -X POST "http://localhost:8000/submit-email?llm_provider=gemini" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Ref ID: 258516012723 -- Ticket No: 933691",
    "sender": "jane.doe@example.com",
    "body": "Hi,\n\nI am Jane Doe. My mobile number is 9876543210 and policy number is PL-78654321. Today syncing is not happening from my wallet.\n\nRegards,\nJane"
  }'
```

---

## 📁 Project Structure

```
.
├── api/                   # FastAPI app
├── worker/                # Celery background processor
├── playbooks/             # YAML files defining fix logic
├── .env                   # Local environment config
├── docker-compose.yml     # Dev orchestration
└── README.md
```

---

## 📜 License

MIT © YourOrg
