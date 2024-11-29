# ABAN Tether Exchange API

This project is an implementation task for ABAN Tether. The goal is to design an API for registering purchase orders from an exchange or cryptocurrency exchange under specific conditions.

## Features

- **User Management**: Create and authenticate users.
- **Currency Management**: List available currencies.
- **Order Management**: Pay order and done settlement.
- **Batch job**: Settlement not settled orders in period time
- **REDIS**: Store not settled orders in redis for settlement batching mode 

## Technology Stack

- **Python**: The main programming language.
- **SQLAlchemy**: An ORM for interacting with the database.
- **FASTAPI**: web framework for building APIs with Python based on standard Python type hints
- **REDIS**: Redis is an in-memory database that persists on disk. The data model is key-value, but many different kind of values are supported: Strings, Lists, Sets, Sorted Sets, Hashes, Streams, HyperLogLogs, Bitmaps.
- **Docker**: For containerization.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose

### Local Development Setup

2. **Build the Docker Image**:
   ```sh
   docker build -t abantether:v1 .

3. **Start the Services**:
   ```sh
   docker-compose up -d

4. **Access the Application**:

   The application will be running at http://localhost:8000/docs#