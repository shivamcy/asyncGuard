# asyncGuard
## Asynchronous API Security & Misconfiguration Scanner

### Description
asyncGuard is a comprehensive, full-stack security platform designed to audit, monitor, and evaluate API configuration hygiene. It combines a robust FastAPI backend with an immersive, Cyberpunk-themed Next.js frontend to provide real-time visibility into security risks.

It helps teams detect misconfigurations, insecure API practices, and operational risks early—before they turn into incidents—all presented through a "hacker-style" system monitor dashboard.

### What Problem Does asyncGuard Solve?
Misconfigurations are a leading cause of security breaches. asyncGuard provides an automated, scalable way to:
- **Register & Track** APIs across an organization.
- **Audit Continuously** using asynchronous background workers.
- **Visualize Risk** via a centralized, interactive dashboard.
- **Enforce Access Control** with strict Role-Based Access Control (RBAC).

---

### Key Features

#### Immersive Dashboard (Frontend)
- **Cyberpunk Aesthetic:** CRT scanlines, vignettes, and terminal-style typography.
- **Real-Time Stats:** Live monitoring of registered APIs and audit performance.

#### Organization & User Management
- **Role-Based Access:** - **Admins:** Manage APIs, view all users, remove users, and destroy organizations.
    - **Viewers/Auditors:** Read-only access to reports and organization info.
- **Strict Hierarchy:** Users belong to exactly one organization. The creator becomes the Admin.
- **User Auditing:** Admins can inspect the personnel database directly from the dashboard.

#### API Management
- **Registry:** Centralized list of all API endpoints under an organization.
- **Validation:** Prevents duplicate names/URLs and enforces valid endpoint formatting.

#### Asynchronous Auditing (Backend)
- **Scalable Workers:** Audits are offloaded to Celery workers to prevent API blocking.
- **Scheduled Scans:** Automated checks run via Celery Beat (every 55 minutes).
- **Resilience:** Fault-tolerant execution with auto-retries and Dead Letter Queue (DLQ) for failed tasks.

---

### Architecture Overview

The system is containerized using **Docker** for consistent deployment.

* **Frontend:** Next.js 16 (React) + Tailwind CSS
* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL (Async + Sync drivers)
* **Task Queue:** Celery + Redis
* **Migrations:** Alembic
* **Auth:** JWT (HTTP-only Cookies)

---

### Configuration

Before running the system, you must set up the environment variables.

#### 1. Frontend Configuration (`frontend/.env.local`)
Create a file named `.env.local` inside the `frontend/` directory:

```env
# Point this to your backend (Internal Docker Alias or Localhost)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 
```

#### 2. Backend Configuration (`backend/.env`)
Create a file named `.env` inside the `backend/` directory:

```env
# App Settings
APP_NAME=asyncGuard
ENV=development
DEBUG=true

# Security (CHANGE THESE IN PRODUCTION)
JWT_SECRET_KEY=change_this_to_a_long_random_string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Cookies
COOKIE_NAME=access_token
COOKIE_SECURE=false      # Set to 'true' in production (HTTPS)
COOKIE_HTTPONLY=true
COOKIE_SAMESITE=lax

# Database Connection
# Format: postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME
DATABASE_URL=postgresql+asyncpg://user:password@your-db-host:5432/postgres
ALEMBIC_DATABASE_URL=postgresql+psycopg2://user:password@your-db-host:5432/postgres

# Redis / Celery
REDIS_HOST=redis
REDIS_PORT=6379

# Celery Configuration (Use 'redis' hostname for Docker, 'localhost' for local dev)
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Audit Settings
AUDIT_TIMEOUT_SECONDS=10
MAX_AUDIT_RETRIES=5

```

### Installation & Setup

asyncGuard is designed to run via **Docker Compose** for immediate deployment.

#### Prerequisites
- Docker Desktop installed and running.
- Git.

#### Quick Start
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shivamcy/asyncGuard.git
    cd asyncGuard
    ```

2. **Setup Environment:**
    
- Copy the configuration above into `frontend/.env.local` and `backend/.env`.


2.  **Build and Start the System:**
    ```bash
    docker compose build
    docker compose up
    ```

3.  **Access the System:**
    - **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
    - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

4.  **Stop the System:**
    Press `Ctrl+C` in the terminal or run:
    ```bash
    docker compose down
    ```

---

### Contributors

- **Shivam Chaudhary** - Backend Architecture, Database Design, API Development, Celery Task Orchestration.  
  [Gmail](mailto:thakurelashivam@gmail.com) • [GitHub](https://github.com/shivamcy) • [LinkedIn](https://www.linkedin.com/in/shivam-chaudhary-0bb343175/)

- **Kanishka Bhardwaj** - Security Architecture, Authentication & Authorization Logic, API Development, Frontend Development.  
  [Gmail](mailto:imkanishkabhardwaj@gmail.com) • [GitHub](https://github.com/kanishkabhardwaj12) • [LinkedIn](https://www.linkedin.com/in/kanishka-bhardwaj-7926a3276/)
