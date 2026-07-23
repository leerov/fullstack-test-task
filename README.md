# File Sharing App (Refactored)

This project is a refactored version of a file-sharing MVP that allows users to upload files, checks them for suspicious content, and sends alerts.

## 🚀 Key Improvements

### Backend Architecture
- **Modular Services**: Split monolithic `service.py` into `file_service.py` and `alert_service.py`.
- **Storage Abstraction**: Introduced `StorageProvider` interface with a `LocalStorageProvider` implementation, allowing easy switching to S3 or other storage backends.
- **Configuration Management**: Centralized settings using `pydantic-settings` in `config.py`.
- **Database Layer**: Unified database engine and session management in `database.py` and `database_sync.py`.
- **Celery Optimization**: Replaced unsafe `asyncio` hacks in Celery tasks with synchronous `psycopg2` driver for stability.
- **Validation**: Added strict file type and MIME type validation in `validators.py`.
- **Logging**: Integrated structured logging using `loguru`.
- **PDF Optimization**: Replaced manual binary string counting with `pypdf` for accurate page count extraction.

### Frontend Architecture
- **Component-Based Structure**: Decomposed the main page into reusable components: `Header`, `FileTable`, `AlertTable`, and `UploadModal`.
- **Custom Hooks**: Extracted data fetching and state logic into `useFiles`, `useAlerts`, and `useFileUpload` hooks.
- **API Client**: Created a centralized API client with error handling in `lib/api/client.ts`.
- **Auto-Refresh**: Implemented polling in `useFiles` hook to automatically update file statuses every 5 seconds.

### DevOps & Infrastructure
- **Docker Compose**: 
  - Pinned specific versions for PostgreSQL (`16-alpine`) and Redis (`7-alpine`).
  - Added healthchecks for dependent services to ensure correct startup order.
  - Added named volumes for persistent storage of both database and uploaded files.
- **Makefile**: Added convenient commands for managing the project lifecycle (`up`, `down`, `migrate`, `logs`).

## 🛠️ Setup & Running

1. **Start services:**
   ```bash
   make up
   ```

2. **Apply database migrations:**
   ```bash
   make migrate
   ```

3. **Access the application:**
   - **Frontend:** [http://localhost:3000/test](http://localhost:3000/test)
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

4. **View logs:**
   ```bash
   make logs
   ```

5. **Stop services:**
   ```bash
   make down
   ```
