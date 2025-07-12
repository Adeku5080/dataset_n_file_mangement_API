# Dataset and File Management Service

A FastAPI-based backend service that allows users to manage datasets and their associated files. Each dataset can contain multiple files in various formats, securely stored in AWS S3. The service includes robust authentication (JWT + OpenID) and full-text search capabilities for efficient metadata querying.

---

## Features

-  User authentication via **JWT** and **OpenID Connect**
-  Create, read, update, and delete **datasets**
-  Upload and manage **files stored in AWS S3**
-  **Full-text search** on dataset metadata and file attributes
-  Secure API endpoints with access control
-  Clean, modular FastAPI architecture

---

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Authentication**: JWT + OpenID Connect
- **Database**: PostgreSQL with Full-Text Search
- **ORM**: SQLAlchemy
- **Object Storage**: AWS S3
- **Testing**: Pytest (optional – add if used)
- **Others**: Alembic for migrations, Uvicorn for ASGI server

---

##  Setup & Installation

> Ensure you have Python 3.10+, PostgreSQL, and AWS credentials configured.

```bash
# 1. Clone the repository
git clone https://github.com/adeku5080/dataset_n_file_mangement_API
cd dataset-file-management-service

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
alembic upgrade head

# 5. Start the development server
uvicorn app.main:app --reload
