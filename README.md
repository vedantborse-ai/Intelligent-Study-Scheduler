# 🧠 SmartSchedule — Intelligent Study Scheduler SaaS

## 📌 Overview

SmartSchedule is a full-stack SaaS platform that automatically generates optimized study schedules based on user-defined tasks, deadlines, and priorities.

Unlike traditional task managers, SmartSchedule uses a deterministic scheduling engine to intelligently allocate time slots, resolve conflicts, and sync optimized schedules directly to Google Calendar.

The system is built with a production-ready architecture, containerized using Docker, and deployed via a CI/CD pipeline.

---

## 🚀 Key Features

### 🔐 Authentication & Google Calendar Integration
- OAuth-based Google authentication
- User session persistence and auto-refresh credentials
- Two-way schedule visibility with primary calendar email display
- Automatic creation of calendar events
- Prevent duplicate calendar entries on rescheduling

### 📝 Task Management
- Create tasks with duration, deadline, and priority (1-5 scale)
- Complete and delete tasks (automatically removes linked calendar events)
- View pending and scheduled tasks

### ⚙️ Deterministic Scheduling Engine
- Sorts tasks using AI priority-queue boosters (e.g. deadline proximity, habits)
- Allocates time slots sequentially starting from current time
- Highlights schedule conflicts in the UI if a task's end time overflows its deadline

### 📊 Dashboard & Analytics
- Glassmorphic Cyberpunk HUD dashboard UI
- Real-time weekly streak count (active day tracker)
- Task completion rates and system load progress bars

---

## 🏗️ System Architecture

The system follows a modular full-stack architecture:

- **Frontend (React + Vite + JS)**: Cyberpunk HUD dashboard UI.
- **Backend (FastAPI + Python)**: API layer, scheduling engine, and Google API integrations.
- **Database (SQLite + SQLAlchemy)**: Persistent storage for tasks and OAuth credentials.
- **CI/CD Pipeline (GitHub Actions)**: Automated code lint, test, build verification, and Docker validation.

---

## 📂 Project Structure

```bash
📁 Intelligent-Study-Scheduler/
│
├── 📁 frontend/                         # React client
│   ├── 📁 src/
│   │   ├── App.css                      # Cyberpunk styles
│   │   └── App.jsx                      # Main UI components
│   ├── Dockerfile                       # Multi-stage production build (Node + Nginx)
│   └── package.json
│
├── 📁 app/                              # FastAPI backend
│   ├── database.py                      # SQLAlchemy database session setup
│   ├── models.py                        # DB schema (Task, OAuthCredential)
│   ├── scheduler.py                     # Deterministic scheduling slot builder
│   ├── ai_engine.py                     # Urgency and priority booster
│   ├── calendar_sync.py                 # Google Calendar integration & credential management
│   ├── routes.py                        # REST API routing
│   └── main.py                          # FastAPI application launcher
│
├── .github/
│   └── workflows/
│       └── ci.yml                       # CI/CD pipeline (GitHub Actions)
│
├── Dockerfile                           # Backend Python slim Dockerfile
├── docker-compose.yml                   # Local multi-container compose orchestrator
├── .env                                 # Configuration and OAuth secret keys
└── README.md                            # Project documentation
```

---

## 🧠 Scheduling Algorithm Overview

The scheduling engine:
1. **Urgency boosting**: Dynamically raises priorities of tasks with upcoming deadlines (<24h and <72h) or overdue status.
2. **Habit adaptation**: Dynamically scales task duration if historically similar priority levels were delayed.
3. **Sequential assignment**: Builds slot durations starting from the current time.
4. **Conflict detection**: Evaluates `end_time > deadline` and marks tasks as conflicting.

---

## ▶️ Local Development Setup

### 1. Clone the repository & Configure credentials
Create a `.env` file in the root of the project with your Google API OAuth credentials:

```env
DATABASE_URL=sqlite:///./tasks.db
JWT_SECRET=your_jwt_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/callback
```

### 2. Launching via Docker Compose
To build and launch both services locally:
```bash
docker-compose up --build
```
- **Frontend App**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **FastAPI OpenAPI docs**: http://localhost:8000/docs

---

## 🌍 Cloud Deployment (Render)

### Deploy Backend (Free Web Service)
1. Link your repository in Render and create a **Web Service**.
2. Set Runtime to **Docker** (Render uses the root `Dockerfile` to launch the API container).
3. Set your env variables matching `.env`.

### Deploy Frontend (Free Static Site)
1. Create a **Static Site** on Render linking the same repository.
2. Set **Root Directory** to `frontend`.
3. Set **Build Command** to `npm run build`.
4. Set **Publish Directory** to `dist`.
5. Add Env Variable `VITE_API_URL` pointing to your deployed backend URL.

---

## 🧑‍💻 Author

Developed as a modern full-stack SaaS system illustrating Docker containerization, Google OAuth, and algorithmic scheduling.
