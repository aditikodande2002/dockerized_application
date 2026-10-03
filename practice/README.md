# FastAPI + MongoDB + Docker Compose Practice Application

A simple FastAPI CRUD application using **MongoEngine** for MongoDB interaction and **Docker Compose** for running FastAPI and MongoDB as separate containers.

---

## 1. Technologies Used

- Python 3.14
- FastAPI
- Uvicorn
- MongoEngine
- PyMongo
- MongoDB 8
- Docker
- Docker Compose
- MongoDB Compass

---

## 2. Project Structure

```text
practice/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 3. Application Architecture

The application has two Docker services:

```text
                 Docker Compose
                      │
          ┌───────────┴───────────┐
          │                       │
          ↓                       ↓
   FastAPI Container       MongoDB Container
   practice_fastapi        practice_mongodb
          │                       │
          │ mongodb://mongodb     │
          └──────────────────────→│
                                  │
                                  ↓
                         mongodb_data volume
```

FastAPI communicates with MongoDB using the Docker Compose service name:

```text
mongodb://mongodb:27017
```

MongoDB is exposed to the Windows host on port `27018`.

FastAPI is exposed on port `8000`.

---

# 4. Important Port Configuration

The application uses:

```text
FastAPI:
localhost:8000

MongoDB Docker container:
localhost:27018
```

Inside Docker, MongoDB still listens on:

```text
27017
```

Therefore:

```text
Windows host       Docker container
-----------------------------------
localhost:27018 →  mongodb:27017
```

Do NOT change the MongoEngine connection to `27018`.

The FastAPI application should use:

```python
connect(
    db="my_database",
    host="mongodb://mongodb:27017"
)
```

---

# 5. Why MongoDB Uses Port 27018

The machine may already have a MongoDB installation running on:

```text
localhost:27017
```

Therefore Docker MongoDB is exposed using:

```yaml
ports:
  - "27018:27017"
```

This means:

```text
27018 = Windows host port
27017 = MongoDB container port
```

MongoDB Compass should connect to the Docker MongoDB using:

```text
mongodb://localhost:27018
```

---

# 6. requirements.txt

The application requires:

```text
fastapi
uvicorn
mongoengine
pymongo
```

Install dependencies manually without Docker using:

```powershell
pip install -r requirements.txt
```

---

# 7. main.py

The MongoDB connection is:

```python
connect(
    db="my_database",
    host="mongodb://mongodb:27017"
)
```

The MongoEngine document:

```python
class users(Document):
    name = StringField(null=True)
    age = IntField(null=True)
```

The application provides three CRUD operations:

```text
GET     /users
POST    /createusers
DELETE  /deleteusers
```

---

# 8. Dockerfile

The Dockerfile:

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile explanation

```dockerfile
FROM python:3.14-slim
```

Uses Python 3.14 slim as the base image.

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory.

```dockerfile
COPY requirements.txt .
```

Copies Python dependencies.

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Installs the dependencies.

```dockerfile
COPY main.py .
```

Copies the application code.

```dockerfile
EXPOSE 8000
```

Documents the application port.

```dockerfile
CMD [...]
```

Starts the FastAPI application using Uvicorn.

---

# 9. docker-compose.yml

Use:

```yaml
services:

  mongodb:
    image: mongo:8
    container_name: practice_mongodb
    ports:
      - "27018:27017"
    volumes:
      - mongodb_data:/data/db

  fastapi:
    build: .
    container_name: practice_fastapi
    ports:
      - "8000:8000"
    depends_on:
      - mongodb

volumes:
  mongodb_data:
```

---

# 10. Understanding docker-compose.yml

## MongoDB service

```yaml
mongodb:
```

`mongodb` is the Compose service name.

Therefore FastAPI can connect using:

```text
mongodb://mongodb:27017
```

---

## MongoDB image

```yaml
image: mongo:8
```

Uses MongoDB version 8.

---

## MongoDB container name

```yaml
container_name: practice_mongodb
```

The actual Docker container is:

```text
practice_mongodb
```

Therefore:

```powershell
docker exec -it practice_mongodb mongosh
```

can be used to enter MongoDB.

---

## MongoDB port

```yaml
ports:
  - "27018:27017"
```

This means:

```text
Windows:   27018
Container: 27017
```

---

## MongoDB volume

```yaml
volumes:
  - mongodb_data:/data/db
```

This stores MongoDB data in a Docker volume.

The actual Docker volume name will normally be:

```text
practice_mongodb_data
```

Do not delete this volume if you want to keep your database data.

---

## FastAPI service

```yaml
fastapi:
```

This is the Compose service name.

Therefore:

```powershell
docker compose logs fastapi
```

works.

---

## FastAPI container

```yaml
container_name: practice_fastapi
```

The actual container is:

```text
practice_fastapi
```

Therefore:

```powershell
docker logs practice_fastapi
```

also works.

---

# 11. Build the Docker Image

From the project directory:

```powershell
cd C:\Users\uk\OneDrive\Desktop\practice
```

Build:

```powershell
docker compose build
```

Or build and start:

```powershell
docker compose up -d --build
```

The image will be created from the Dockerfile.

Check images:

```powershell
docker images
```

You should see:

```text
practice-fastapi
```

---

# 12. Start the Application

Start in detached mode:

```powershell
docker compose up -d
```

If you changed `main.py`, `requirements.txt`, or the Dockerfile:

```powershell
docker compose up -d --build
```

---

# 13. Check Running Services

Run:

```powershell
docker compose ps
```

Expected result:

```text
NAME               IMAGE              SERVICE   STATUS
practice_fastapi   practice-fastapi   fastapi   Up
practice_mongodb   mongo:8            mongodb   Up
```

You should also see:

```text
8000->8000
27018->27017
```

---

# 14. Check Docker Containers

Run:

```powershell
docker ps
```

Expected containers:

```text
practice_fastapi
practice_mongodb
```

---

# 15. View FastAPI Logs

Show logs:

```powershell
docker compose logs fastapi
```

Show the last 10 lines:

```powershell
docker compose logs fastapi --tail 10
```

Follow logs continuously:

```powershell
docker compose logs -f fastapi
```

Follow the last 10 lines:

```powershell
docker compose logs -f fastapi --tail 10
```

Press:

```text
CTRL + C
```

to stop following the logs.

This does NOT stop the container.

---

# 16. View MongoDB Logs

```powershell
docker compose logs mongodb
```

Last 10 lines:

```powershell
docker compose logs mongodb --tail 10
```

Follow logs:

```powershell
docker compose logs -f mongodb
```

---

# 17. View Logs for All Services

```powershell
docker compose logs
```

Follow all logs:

```powershell
docker compose logs -f
```

Last 10 lines:

```powershell
docker compose logs --tail 10
```

---

# 18. Access FastAPI Swagger

Open:

```text
http://localhost:8000/docs
```

FastAPI Swagger UI will display the available endpoints.

---

# 19. FastAPI OpenAPI JSON

Open:

```text
http://localhost:8000/openapi.json
```

---

# 20. Test GET /users

Using PowerShell:

```powershell
curl http://localhost:8000/users
```

If there are no users:

```json
[]
```

If users exist, the response will contain them.

---

# 21. Create a User

Endpoint:

```text
POST /createusers
```

Using PowerShell:

```powershell
curl -Method POST http://localhost:8000/createusers `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"name":"Aditi","age":25}'
```

Example response:

```json
{
  "id": "68...",
  "name": "Aditi",
  "age": 25
}
```

---

# 22. Get All Users

```powershell
curl http://localhost:8000/users
```

Example:

```json
[
  {
    "id": "68...",
    "name": "Aditi",
    "age": 25
  }
]
```

---

# 23. Get One User

Use the user's MongoDB ID:

```powershell
curl "http://localhost:8000/users?userid=YOUR_USER_ID"
```

Example:

```powershell
curl "http://localhost:8000/users?userid=68ac..."
```

---

# 24. Update a User

The same POST endpoint supports updating when `userid` is provided.

```powershell
curl -Method POST "http://localhost:8000/createusers?userid=YOUR_USER_ID" `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"name":"Aditi Updated","age":26}'
```

---

# 25. Delete a User

Use:

```powershell
curl -Method DELETE "http://localhost:8000/deleteusers?userid=YOUR_USER_ID"
```

Example:

```powershell
curl -Method DELETE "http://localhost:8000/deleteusers?userid=68ac..."
```

Response:

```json
{
  "message": "User deleted successfully"
}
```

---

# 26. Access MongoDB Container

Open the MongoDB shell:

```powershell
docker exec -it practice_mongodb mongosh
```

---

# 27. Select the Application Database

Inside `mongosh`:

```javascript
use my_database
```

---

# 28. Show Collections

```javascript
show collections
```

Expected:

```text
users
```

---

# 29. View Users Directly

```javascript
db.users.find()
```

For formatted output:

```javascript
db.users.find().pretty()
```

---

# 30. Count Users

```javascript
db.users.countDocuments()
```

---

# 31. Find a Specific User

```javascript
db.users.find({name: "Aditi"})
```

---

# 32. Exit MongoDB Shell

```javascript
exit
```

---

# 33. MongoDB Compass

To view the MongoDB running inside Docker from MongoDB Compass, connect to:

```text
mongodb://localhost:27018
```

Then navigate to:

```text
my_database
    └── users
```

The data shown here is the data stored by the Docker MongoDB container.

---

# 34. Important MongoDB Connection Difference

Inside Docker:

```python
host="mongodb://mongodb:27017"
```

From Windows/MongoDB Compass:

```text
mongodb://localhost:27018
```

Do not use:

```python
mongodb://localhost:27017
```

inside the FastAPI container.

Inside a container, `localhost` refers to the FastAPI container itself, not the MongoDB container.

---

# 35. Docker Compose Networking

Compose automatically creates a network for the services.

The services can communicate using their service names.

For example:

```text
fastapi → mongodb
```

using:

```text
mongodb://mongodb:27017
```

The service name:

```text
mongodb
```

acts as the hostname inside the Compose network.

---

# 36. Check Compose Service Names

Run:

```powershell
docker compose config --services
```

Expected:

```text
mongodb
fastapi
```

---

# 37. Check Docker Volumes

```powershell
docker volume ls
```

You should see:

```text
practice_mongodb_data
```

Inspect the volume:

```powershell
docker volume inspect practice_mongodb_data
```

---

# 38. Stop the Application

To stop and remove the containers:

```powershell
docker compose down
```

The MongoDB volume remains.

Therefore the database data is preserved.

---

# 39. Start Again

```powershell
docker compose up -d
```

Your MongoDB data should still exist because the volume was not deleted.

---

# 40. WARNING: docker compose down -v

Avoid using this unless you intentionally want to delete the Compose volumes:

```powershell
docker compose down -v
```

This can delete:

```text
practice_mongodb_data
```

and therefore delete the MongoDB data stored in that Docker volume.

For normal stopping, use:

```powershell
docker compose down
```

---

# 41. Rebuild After Code Changes

If you change `main.py`, run:

```powershell
docker compose up -d --build
```

If you only want to rebuild:

```powershell
docker compose build
```

Then start:

```powershell
docker compose up -d
```

---

# 42. Restart a Service

Restart FastAPI:

```powershell
docker compose restart fastapi
```

Restart MongoDB:

```powershell
docker compose restart mongodb
```

Restart everything:

```powershell
docker compose restart
```

---

# 43. Stop One Service

Stop FastAPI:

```powershell
docker compose stop fastapi
```

Stop MongoDB:

```powershell
docker compose stop mongodb
```

Start it again:

```powershell
docker compose start fastapi
```

---

# 44. Execute Commands Inside FastAPI Container

Open a shell:

```powershell
docker exec -it practice_fastapi /bin/bash
```

If Bash is not available:

```powershell
docker exec -it practice_fastapi /bin/sh
```

Exit:

```text
exit
```

---

# 45. Execute Commands Inside MongoDB Container

```powershell
docker exec -it practice_mongodb mongosh
```

---

# 46. View Container Details

FastAPI:

```powershell
docker inspect practice_fastapi
```

MongoDB:

```powershell
docker inspect practice_mongodb
```

---

# 47. View Docker Networks

```powershell
docker network ls
```

View the Compose network:

```powershell
docker compose config
```

---

# 48. Common Docker Commands

List containers:

```powershell
docker ps
```

List all containers:

```powershell
docker ps -a
```

List images:

```powershell
docker images
```

List volumes:

```powershell
docker volume ls
```

List networks:

```powershell
docker network ls
```

Remove stopped containers:

```powershell
docker container prune
```

Remove unused images:

```powershell
docker image prune
```

Remove unused Docker resources:

```powershell
docker system prune
```

Use `docker system prune` carefully because it can remove unused Docker resources.

---

# 49. Docker Compose Commands

Build:

```powershell
docker compose build
```

Build without cache:

```powershell
docker compose build --no-cache
```

Start:

```powershell
docker compose up
```

Start in background:

```powershell
docker compose up -d
```

Build and start:

```powershell
docker compose up -d --build
```

Stop:

```powershell
docker compose down
```

View services:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs
```

Follow logs:

```powershell
docker compose logs -f
```

---

# 50. Complete Development Flow

When starting the project for the first time:

```powershell
cd C:\Users\uk\OneDrive\Desktop\practice
```

Build and start:

```powershell
docker compose up -d --build
```

Check:

```powershell
docker compose ps
```

Check FastAPI logs:

```powershell
docker compose logs fastapi --tail 10
```

Open:

```text
http://localhost:8000/docs
```

Test:

```powershell
curl http://localhost:8000/users
```

Create a user:

```powershell
curl -Method POST http://localhost:8000/createusers `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"name":"Aditi","age":25}'
```

Check users:

```powershell
curl http://localhost:8000/users
```

Check MongoDB:

```powershell
docker exec -it practice_mongodb mongosh
```

Then:

```javascript
use my_database
db.users.find()
```

---

# 51. Development Flow After Changing Code

Whenever `main.py` changes:

```powershell
docker compose up -d --build
```

Then:

```powershell
docker compose ps
```

Then:

```powershell
docker compose logs -f fastapi --tail 10
```

Test:

```text
http://localhost:8000/docs
```

---

# 52. Troubleshooting

## FastAPI container is not running

Check:

```powershell
docker compose ps
```

Then:

```powershell
docker compose logs fastapi
```

---

## MongoDB container is not running

Check:

```powershell
docker compose ps
```

Then:

```powershell
docker compose logs mongodb
```

---

## FastAPI cannot connect to MongoDB

Check `main.py`.

It should contain:

```python
connect(
    db="my_database",
    host="mongodb://mongodb:27017"
)
```

Do not use:

```python
mongodb://localhost:27017
```

---

## Port 8000 is already in use

Check:

```powershell
netstat -ano | findstr :8000
```

You can either stop the process using the port or change the Compose mapping.

For example:

```yaml
ports:
  - "8001:8000"
```

Then access:

```text
http://localhost:8001/docs
```

---

## Port 27018 is already in use

Check:

```powershell
netstat -ano | findstr :27018
```

Change the host port if necessary:

```yaml
ports:
  - "27019:27017"
```

Then MongoDB Compass would use:

```text
mongodb://localhost:27019
```

The FastAPI connection remains:

```python
mongodb://mongodb:27017
```

---

# 53. Docker vs Docker Compose vs Docker Swarm

This project uses **Docker Compose**.

Therefore use:

```powershell
docker compose logs fastapi
```

not:

```powershell
docker service logs fastapi
```

`docker service logs` is primarily for **Docker Swarm services**.

For example, in a Swarm environment:

```bash
docker service logs -f redx_vmauth --tail 10
```

For this project:

```powershell
docker compose logs -f fastapi --tail 10
```

---

# 54. Useful Difference Between Names

There are three important names:

```text
Compose service:
fastapi

Container:
practice_fastapi

Image:
practice-fastapi
```

For example:

```powershell
docker compose logs fastapi
```

uses the **service name**.

```powershell
docker logs practice_fastapi
```

uses the **container name**.

```powershell
docker images
```

shows the **image name**.

Similarly:

```text
Compose service:
mongodb

Container:
practice_mongodb

Image:
mongo:8
```

---

# 55. MongoDB Data Persistence

The Compose file contains:

```yaml
volumes:
  - mongodb_data:/data/db
```

This means MongoDB data is stored in:

```text
practice_mongodb_data
```

If you run:

```powershell
docker compose down
```

the containers are removed but the volume remains.

When you run:

```powershell
docker compose up -d
```

the existing MongoDB data is available again.

---

# 56. Important Existing MongoDB Situation

If MongoDB was already installed directly on Windows, there can be two MongoDB instances:

```text
Windows MongoDB
localhost:27017
```

and:

```text
Docker MongoDB
localhost:27018
```

For this Dockerized project, MongoDB Compass should use:

```text
mongodb://localhost:27018
```

FastAPI should use:

```text
mongodb://mongodb:27017
```

These two connection strings point to the same Docker MongoDB from different locations.

---

# 57. Recommended Daily Commands

### Start project

```powershell
docker compose up -d
```

### Check status

```powershell
docker compose ps
```

### Check logs

```powershell
docker compose logs -f fastapi --tail 10
```

### Open Swagger

```text
http://localhost:8000/docs
```

### Enter MongoDB

```powershell
docker exec -it practice_mongodb mongosh
```

### Check users

```javascript
use my_database
db.users.find()
```

### Stop project

```powershell
docker compose down
```

---

# 58. Full Command Cheat Sheet

```powershell
# Go to project
cd C:\Users\uk\OneDrive\Desktop\practice

# Build
docker compose build

# Start
docker compose up -d

# Build + start
docker compose up -d --build

# Check services
docker compose ps

# Check all containers
docker ps

# FastAPI logs
docker compose logs fastapi

# Follow FastAPI logs
docker compose logs -f fastapi

# Last 10 FastAPI logs
docker compose logs fastapi --tail 10

# Follow last 10 logs
docker compose logs -f fastapi --tail 10

# MongoDB logs
docker compose logs mongodb

# All logs
docker compose logs

# Stop containers
docker compose stop

# Stop and remove containers
docker compose down

# Restart
docker compose restart

# Restart FastAPI
docker compose restart fastapi

# Restart MongoDB
docker compose restart mongodb

# Enter MongoDB
docker exec -it practice_mongodb mongosh

# Enter FastAPI container
docker exec -it practice_fastapi /bin/bash

# If bash doesn't exist
docker exec -it practice_fastapi /bin/sh

# List images
docker images

# List containers
docker ps -a

# List volumes
docker volume ls

# Inspect MongoDB volume
docker volume inspect practice_mongodb_data

# Check Compose services
docker compose config --services

# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Docker cleanup
docker system prune
```

---

# 59. Final Application URLs

FastAPI:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

OpenAPI:

```text
http://localhost:8000/openapi.json
```

MongoDB Compass:

```text
mongodb://localhost:27018
```

Database:

```text
my_database
```

Collection:

```text
users
```

---

# 60. Final Architecture

```text
                         Windows
                            │
              ┌─────────────┴─────────────┐
              │                           │
              │                           │
       localhost:8000              localhost:27018
              │                           │
              ↓                           ↓
     ┌─────────────────┐         ┌─────────────────┐
     │ FastAPI         │         │ MongoDB 8       │
     │                 │         │                 │
     │ practice_fastapi│────────→│practice_mongodb │
     │                 │         │                 │
     └─────────────────┘         └────────┬────────┘
                                          │
                                          ↓
                                 mongodb_data volume
                                          │
                                          ↓
                                     my_database
                                          │
                                          ↓
                                       users
```

The application is now fully Dockerized with **FastAPI + MongoDB + persistent Docker volume + Docker Compose**.