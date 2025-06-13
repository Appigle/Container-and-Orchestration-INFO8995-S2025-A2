# Container-and-Orchestration-INFO8995-S2025-A2

## Overview

This project demonstrates a web application using Docker Compose. It consists of:

- A Python Flask API server for user data (create/fetch)
- A MySQL 8.0 database for data persistence
- Nginx as a load balancer for scaling multiple web app containers

## Project Structure

```
├── app/
│   ├── main.py               # Flask API
│   ├── requirements.txt      # Python dependencies
│   └── logs/                 # Log files (created at runtime)
├── db/
│   └── init.sql              # SQL to create user table
├── docker-compose.yml        # Multi-container orchestration
├── nginx.conf                # Nginx load balancer config
├── .env                      # (Optional) Environment variables
└── README.md                 # This file
```

## Prerequisites

- Docker & Docker Compose installed
- Python 3.8+ for local development (Optional)

## Quick Start

1. **Clone the repository and navigate to the project root.**

2. **Build and start the stack with scaling:**

   ```sh
   docker-compose up --build --scale web=3
   ```

   - This starts 3 Flask app containers, 1 MySQL database, and 1 Nginx load balancer (on port 5000).

3. **Access the API:**
   - Base URL: [http://localhost:5000/](http://localhost:5000/)

## API Usage Examples

### Create a User

```sh
curl -X POST http://localhost:5000/user \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Alice", "last_name": "Smith"}'
```

### Fetch a User by ID

```sh
curl http://localhost:5000/user/1
```

## Logs

- All API requests and responses are logged to `app/logs/app.log` inside the container.
- To view logs from the host:
  ```sh
  cat app/logs/app.log
  ```

## Data Persistence

- MySQL data is stored in a Docker volume (`db_data`) and persists across container restarts.
- To test persistence:
  1. Create a user.
  2. Run `docker-compose down` then `docker-compose up --scale web=3`.
  3. Fetch the user again to confirm data is retained.

## Scaling & Load Balancing

- Nginx load balances requests across all running `web` containers.
- To change the number of web app replicas:
  ```sh
  docker-compose up --build --scale web=N
  ```
  (Replace `N` with the desired number of replicas.)
- The `nginx.conf` upstream block should list all expected web containers (e.g., `web`, `web_1`, `web_2`, ...).

## Security Best Practices

- Flask app runs as a non-root user in a minimal image.
- MySQL uses a dedicated user and strong passwords.
- Only required ports are exposed; internal networking is used for inter-container communication.

---
