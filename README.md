# Online Food Ordering Microservice

A microservice-based food ordering system built as a university project. The system is composed of multiple independent services, each responsible for a specific domain, communicating through an API gateway and a message broker.

---

## Services

### Catalog Service — Rust + Axum + PostgreSQL
Manages restaurants and their menu items. Built in Rust for performance and type safety. Uses `sqlx` for compile-time verified SQL queries and `axum` as the web framework.

**Endpoints:**
- `GET /api/restaurants` — list all restaurants
- `POST /api/restaurants` — create a restaurant
- `GET /api/restaurants/{id}` — get a restaurant
- `PATCH /api/restaurants/{id}` — update a restaurant
- `DELETE /api/restaurants/{id}` — delete a restaurant
- `GET /api/restaurants/{id}/items` — list menu items
- `POST /api/restaurants/{id}/items` — create a menu item
- `GET /api/restaurants/{id}/items/{item_id}` — get a menu item
- `PATCH /api/restaurants/{id}/items/{item_id}` — update a menu item
- `DELETE /api/restaurants/{id}/items/{item_id}` — delete a menu item

---

### Customer Service — Python + FastAPI + PostgreSQL
Handles customer registration, authentication, and profile management. Issues JWT tokens on login used to protect customer endpoints.

**Endpoints:**
- `POST /api/customers/register` — register a new customer
- `POST /api/customers/login` — login and receive a JWT token
- `GET /api/customers` — list all customers (auth required)
- `GET /api/customers/{id}` — get a customer (auth required)
- `PATCH /api/customers/{id}` — update a customer (auth required, own account only)
- `DELETE /api/customers/{id}` — delete a customer (auth required, own account only)

---

### Order Cart Service — Python + FastAPI + Redis
Manages customer shopping carts. Uses Redis for fast ephemeral storage with automatic TTL expiry. Carts are stored as JSON blobs keyed by user ID.

**Endpoints:**
- `GET /api/cart/{user_id}` — get a cart
- `POST /api/cart/{user_id}/items` — add an item to the cart
- `PATCH /api/cart/{user_id}/items/{item_id}` — update item quantity
- `DELETE /api/cart/{user_id}/items/{item_id}` — remove an item
- `DELETE /api/cart/{user_id}/items` — clear the cart
- `DELETE /api/cart/{user_id}` — delete the cart

---

### Order Service — TypeScript + Fastify + PostgreSQL
Handles order creation and status tracking. Built with Fastify for performance and Drizzle ORM for type-safe SQL. Orders snapshot item data at the time of purchase.

**Endpoints:**
- `GET /api/orders` — list all orders
- `POST /api/orders` — create an order
- `GET /api/orders/{orderId}` — get an order
- `GET /api/users/{userId}/orders` — get orders by user
- `PATCH /api/orders/{orderId}/status` — update order status

---

### Queue Service — Python + FastAPI + RabbitMQ
Demonstrates asynchronous messaging using RabbitMQ. Publishes a message to a queue, consumes it, and echoes it back. Serves as the foundation for future event-driven features like email notifications.

**Endpoints:**
- `POST /api/send` — publish and echo a message

---

### API Gateway — Traefik
All traffic flows through Traefik on port 80. Routes requests to the appropriate service based on path prefix, stripping the `/api` prefix before forwarding.

| Path | Service | Port |
|---|---|---|
| `/api/restaurants` | Catalog Service | 8001 |
| `/api/cart` | Order Cart Service | 8002 |
| `/api/customers` | Customer Service | 8003 |
| `/api/orders` | Order Service | 8004 |
| `/api/send` | Queue Service | 8005 |

Traefik dashboard available at `http://localhost:8080`.

---

## Technology Choices

| Technology | Used In | Why |
|---|---|---|
| **Rust + Axum** | Catalog Service | Performance, memory safety, compile-time SQL verification with sqlx |
| **Python + FastAPI** | Customer, Cart, Queue Services | Fast development, automatic OpenAPI docs, async support |
| **TypeScript + Fastify** | Order Service | Type safety, modern Node.js ecosystem, Fastify's performance |
| **PostgreSQL** | Catalog, Customer, Order | Relational data with ACID guarantees, each service owns its own database |
| **Redis** | Order Cart | Ephemeral session-like data needing fast reads/writes and automatic TTL expiry |
| **RabbitMQ** | Queue Service | Async message passing, decouples services, foundation for event-driven features |
| **Traefik** | API Gateway | Docker-native, automatic service discovery via labels, built-in dashboard |
| **SQLAlchemy** | Customer Service | Async ORM for Python with Postgres |
| **Drizzle ORM** | Order Service | Lightweight TypeScript-first ORM, type-safe queries |
| **sqlx** | Catalog Service | Compile-time SQL verification, zero-cost abstractions |
| **bcrypt** | Customer Service | Industry standard password hashing |
| **JWT** | Customer Service | Stateless authentication tokens |
| **Docker Compose** | Infrastructure | Orchestrates all services and infrastructure locally |

---

## Architecture

```
Client
  ↓
Traefik (port 80) — API Gateway
  ├── /api/restaurants → Catalog Service → PostgreSQL
  ├── /api/customers   → Customer Service → PostgreSQL
  ├── /api/cart        → Cart Service → Redis
  ├── /api/orders      → Order Service → PostgreSQL
  └── /api/send        → Queue Service → RabbitMQ
```

Each service:
- Owns its own database (no shared databases between services)
- Is independently deployable
- Communicates through the API gateway
- Has its own Docker container

---

## Running the Project

**Requirements:** Docker and Docker Compose

Create a `.env` file at the repo root:
```
DB_PASSWORD=your_password
JWT_SECRET=your_jwt_secret
RABBITMQ_USER=your_rabbitmq_user
RABBITMQ_PASS=your_rabbitmq_pass
```

Start all services:
```bash
docker compose up --build
```

**Service URLs:**
- API Gateway: `http://localhost`
- Traefik Dashboard: `http://localhost:8080`
- RabbitMQ Dashboard: `http://localhost:15672`
- Customer Service Docs: `http://localhost:8003/docs`
- Cart Service Docs: `http://localhost:8002/docs`
- Queue Service Docs: `http://localhost:8005/docs`
- Order Service Docs: `http://localhost:8004/docs`

---

## Design Patterns Used

**Repository Pattern** — all database operations are abstracted behind repository interfaces. Handlers depend on the interface, not the implementation. Swapping databases requires only a new repository implementation.

**DTO Pattern** — separate data transfer objects for incoming requests and outgoing responses. Prevents internal domain fields from leaking into the API and enforces validation at the boundary.

**Dependency Injection** — repositories are injected into handlers at startup rather than being instantiated inside them. Enables loose coupling between layers.

**Database per Service** — each service owns its own database. No service can directly query another service's database. Data is shared through API calls only.
