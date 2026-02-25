# 🧠 SmartSchedule — Intelligent Study Scheduler SaaS

## 📌 Overview

SmartSchedule is a full-stack SaaS platform that automatically generates optimized study schedules based on user-defined tasks, deadlines, and priorities.

Unlike traditional task managers, SmartSchedule uses a deterministic scheduling engine to intelligently allocate time slots, resolve conflicts, and sync optimized schedules directly to Google Calendar.

The system is built with a production-ready architecture, containerized using Docker, and deployed via a CI/CD pipeline.

---

## 🎯 Problem Statement

Students and professionals often:

- Underestimate task durations  
- Overload certain days  
- Manually schedule inefficiently  
- Miss deadlines due to poor time allocation  

Most task management tools are passive — they store tasks but do not optimize time.

SmartSchedule solves this by:

- Automatically generating optimized schedules  
- Balancing workload across available time slots  
- Prioritizing tasks based on urgency and importance  
- Syncing structured schedules to Google Calendar  
- Providing analytics on workload distribution  

---

## 🚀 Key Features

### 🔐 Authentication

- Secure JWT-based authentication  
- User registration & login  
- Session management  

---

### 📝 Task Management

Users can:

- Create tasks with duration, deadline, and priority  
- Edit and delete tasks  
- View pending and scheduled tasks  

---

### ⚙️ Scheduling Engine

The system automatically:

- Sorts tasks using priority queues  
- Allocates time slots before deadlines  
- Prevents schedule conflicts  
- Optimizes workload distribution  

Scheduling decisions are deterministic and reproducible.

---

### 📅 Google Calendar Integration

- OAuth-based Google authentication  
- Automatic creation of calendar events  
- Update/delete synced events  
- Two-way schedule visibility  

---

### 📊 Dashboard & Analytics

- Weekly calendar visualization  
- Task distribution charts  
- Workload heatmap  
- Schedule summary  

---

## 🏗️ System Architecture

The system follows a modular SaaS architecture:

Frontend (React + TypeScript)  
→ User interaction & dashboard UI  

Backend (Node.js + Express)  
→ API layer + scheduling engine  

Database (PostgreSQL)  
→ Persistent storage for users, tasks, and schedules  

Google Calendar API  
→ External calendar synchronization  

CI/CD Pipeline (GitHub Actions)  
→ Automated build, test, and deployment  

Dockerized Environment  
→ Containerized frontend and backend services  

---

## 🧱 Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS

### Backend
- Node.js
- Express
- JWT Authentication

### Database
- PostgreSQL

### DevOps
- Docker
- Docker Compose
- GitHub Actions (CI/CD)
- Cloud Deployment (Render / Railway / AWS)

---

## 📂 Project Structure

```bash
📁 smartschedule/
│
├── 📁 frontend/                         # React + TypeScript client
│   ├── 📁 src/
│   ├── 📁 public/
│   └── Dockerfile
│
├── 📁 backend/                          # Node.js + Express API
│   ├── 📁 src/
│   │   ├── 📁 controllers/              # Request handlers
│   │   ├── 📁 routes/                   # API route definitions
│   │   ├── 📁 services/                 # Business logic (scheduler, calendar)
│   │   ├── 📁 middleware/               # Auth & validation middleware
│   │   ├── 📁 utils/                    # Helper functions
│   │   └── server.ts                    # Entry point
│   └── Dockerfile
│
├── docker-compose.yml                   # Local multi-container setup
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── ci.yml                       # CI/CD pipeline (GitHub Actions)
│
└── README.md                            # Project documentation
```

---

## 🧠 Scheduling Algorithm Overview

The scheduling engine:

1. Sorts tasks by:
   - Priority level  
   - Deadline proximity  

2. Uses a greedy time allocation strategy:
   - Finds available time slots  
   - Allocates duration blocks  
   - Ensures deadline compliance  

3. Detects conflicts and rebalances automatically.

Time complexity depends primarily on:
- Number of tasks
- Number of available time slots

---

## 🐳 DevOps & Deployment

SmartSchedule is production-ready.

### Docker
- Multi-container architecture  
- Separate containers for frontend & backend  
- Environment-based configuration  

### CI/CD Pipeline

GitHub Actions pipeline:

- Runs tests  
- Builds Docker images  
- Pushes to registry  
- Deploys to cloud environment  

---

# 📦 API Documentation

All endpoints are prefixed with:

---

## 🔐 Authentication

Handles user registration and login.

| Method | Endpoint              | Description            | Auth Required |
|--------|----------------------|------------------------|--------------|
| POST   | `/auth/register`     | Register new user      | ❌ No        |
| POST   | `/auth/login`        | Authenticate user      | ❌ No        |

---

## 📝 Task Management

CRUD operations for managing user tasks.

| Method | Endpoint         | Description              | Auth Required |
|--------|-----------------|--------------------------|--------------|
| GET    | `/tasks`        | Get all user tasks       | ✅ Yes       |
| POST   | `/tasks`        | Create a new task        | ✅ Yes       |
| PUT    | `/tasks/:id`    | Update an existing task  | ✅ Yes       |
| DELETE | `/tasks/:id`    | Delete a task            | ✅ Yes       |

---

## ⚙️ Scheduling

Endpoints related to schedule generation and retrieval.

| Method | Endpoint                  | Description                     | Auth Required |
|--------|---------------------------|---------------------------------|--------------|
| POST   | `/schedule/generate`      | Generate optimized schedule     | ✅ Yes       |
| GET    | `/schedule`               | Retrieve current schedule       | ✅ Yes       |

---

## 📅 Calendar Integration

Google Calendar synchronization endpoints.

| Method | Endpoint              | Description                           | Auth Required |
|--------|-----------------------|---------------------------------------|--------------|
| POST   | `/calendar/sync`      | Sync schedule with Google Calendar    | ✅ Yes       |

---

## 📌 Example Request

### Create Task

```json
POST /api/tasks
{
  "title": "Complete DSA practice",
  "duration": 120,
  "deadline": "2026-02-28",
  "priority": "HIGH"
}
```

---

## 🔐 Environment Variables

Backend requires:
DATABASE_URL=
JWT_SECRET=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

---

## ▶️ Local Development Setup

1. Clone the repository  
2. Configure environment variables  
3. Run:
   docker-compose up --build


Frontend: http://localhost:3000  
Backend: http://localhost:5000  

---

## 🌍 Deployment

The application is deployed using:

- Docker containers  
- GitHub Actions CI/CD  
- Cloud platform hosting  

Live Demo: (Add deployment link here)

---

## 📈 Future Improvements

- Adaptive learning from user habits  
- AI-based duration prediction  
- Smart break insertion  
- Mobile responsiveness  
- Real-time notifications  

---

## 🧑‍💻 Author

Developed as a full-stack SaaS system demonstrating:

- System design
- Algorithmic scheduling
- API integration
- DevOps & CI/CD
- Production deployment
