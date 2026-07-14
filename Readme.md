# Library Management System

A learning project focused on building intuition for Object-Oriented Design (OOD), Low-Level Design (LLD), and backend engineering by incrementally evolving a Library Management System from a pure in-memory domain model into a production-style backend service.

## Objectives

This project is intended to develop engineering intuition rather than build a CRUD application.

The primary goals are:

- Object-Oriented Design
- Domain Modeling
- Responsibility Assignment
- SOLID Principles
- Backend Architecture
- Software Evolution

The project is intentionally developed in multiple iterations, introducing technologies only when the domain model naturally requires them.

---

## Roadmap

### V1 — Domain Model (Completed)

Pure object-oriented implementation.

Features:

- Book registration
- Multiple physical copies per title
- Member registration
- Borrow workflow
- Return workflow
- Borrow eligibility
- In-memory storage
- Unit tests

No frameworks or databases are used.

---

### V2 — Domain Features

- Reservations
- Waiting list
- Faculty priority
- Reservation expiry
- Overdue restrictions

---

### V3 — REST API

Expose the existing domain model using FastAPI.

---

### V4 — Persistence

Replace in-memory storage with PostgreSQL through repository abstractions.

---

### V5 — Infrastructure

Introduce:

- Redis
- Authentication
- Caching

---

### V6 — Production Engineering

- Docker
- CI/CD
- Logging
- Monitoring
- Deployment

---

## Current Project Structure

```
library-management-system/

├── Inventory/
│   ├── Book.py
│   └── BookCopy.py
│
├── Library/
│   └── Library.py
│
├── Members/
│   └── Member.py
│
├── tests.py
├── enums.py
└── main.py
```

---

## Domain Model

```
Library
│
├── Books
│      │
│      ├── Book (Title)
│      │       │
│      │       └── BookCopy
│      │
│      └── ISBN → Book
│
└── Members
        │
        └── Member ID → Member
```

---

## Current Business Workflows

- Register books
- Register members
- Borrow a book
- Return a book

---

## Learning Notes

This repository prioritizes:

- Correct responsibility assignment
- Encapsulation
- Composition over inheritance
- Rich domain models
- Incremental software evolution

Infrastructure concerns are intentionally postponed until the domain model is stable.

---

## Status

Current milestone:

**V1 — Complete**