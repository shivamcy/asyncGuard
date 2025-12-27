
# asyncGuard
## Asynchronous API Security & Misconfiguration Scanner
### Description

asyncGuard is a backend system designed to audit, monitor, and evaluate API security and configuration hygiene. It helps teams detect misconfigurations, insecure API practices, and operational risks early—before they turn into incidents.

The project is built with FastAPI, PostgreSQL, Celery, and Redis, and is designed to scale from API-level auditing to cloud-level security scanning.


### What Problem Does asyncGuard Solve?
Misconfigurations are one of the leading causes of security breaches.
asyncGuard provides an automated way to:

- Register APIs belonging to an organization
- Periodically audit those APIs
- Detect insecure configurations and bad practices
- Store and report audit results
- Run checks asynchronously at scale

### Key Features

- Organization Management
    - Users can belong to only one organization
    - A Viewer can create an organization
    - The creator becomes the Admin
    - Only Admins can delete organizations
    - Deleting an organization resets all users to Viewer with no org and also deletes all the associated APIs

- API Management
    - Admins can register APIs under an organization
    - Prevent duplicate API names or URLs
    - Activate / deactivate APIs
    - List APIs per organization
    - Protected by authentication and role checks

- Asynchronous Auditing
    - APIs are audited using background workers
    - Scheduled audits using Celery Beat
    - Fault-tolerant task execution with retries
    - Dead Letter Queue support for failed tasks


### Architecture Overview

- FastAPI – REST API backend
- PostgreSQL – Persistent storage
- SQLAlchemy (Async) – ORM
- Alembic – Database migrations
- Celery – Asynchronous task execution
- Redis – Message broker for Celery
- JWT (Cookies) – Authentication & authorization


### Conclusion
asyncGuard provides a scalable and extensible backend system for auditing and monitoring API security and reliability.  
Designed with modular checks, asynchronous execution, and strict access control, it serves as a strong foundation for evolving into broader infrastructure and cloud security auditing use cases.
The architecture prioritizes clarity, security, and maintainability, making it suitable for both research and production deployments.

#### Contributors
- Shivam Chaudhary - Backend Architecture, Database Design, API Development, Celery Task Orchestration. [Gmail](thakurelashivam@gmail.com) • [GitHub](https://github.com/shivamcy) • [LinkedIn](https://www.linkedin.com/in/shivam-chaudhary-0bb343175/)


- Kanishka Bhardwaj - Security Architecture, Authentication & Authorization Logic, API Development. [Gmail](imkanishkabhardwaj@gmail.com) • [GitHub](https://github.com/kanishkabhardwaj12) • [LinkedIn](www.linkedin.com/in/kanishka-bhardwaj-7926a3276/)