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

The project evolves in four phases. Each phase introduces new concepts only after the previous one is stable.

### Phase 1 — Domain Modeling

#### V1 — Core Domain (Completed)

- Book registration
- Member registration
- Multiple physical copies
- Borrow workflow
- Return workflow
- Borrow eligibility
- In-memory implementation
- Unit & integration tests

#### V2 — Circulation Policies (Completed)

- Waiting lists
- Reservations
- Reservation expiry
- Overdue restrictions
- Faculty priority
- Domain invariants
- Rich aggregate behavior

#### V3 — Inventory Evolution

- Damaged copies
- Lost copies
- Remove from circulation
- Inventory consistency
- Tests

#### V4 — Search & Membership Policies

- Search by ISBN
- Search by title
- Search by author
- Membership policies
- Borrowing policy evolution

#### V5 — Engineering Review

- SOLID review
- GRASP review
- Aggregate review
- Responsibility review
- Refactoring
- Test review
- Documentation

---

### Phase 2 — Persistence

- Repository interfaces
- In-memory repositories
- SQLite implementation
- SQLAlchemy mapping
- Transactions

---

### Phase 3 — Application Layer

- FastAPI
- DTOs
- Validation
- Dependency Injection
- Exception handling

---

### Phase 4 — Production Infrastructure

- PostgreSQL
- Redis
- Background scheduler
- Authentication
- Docker
- Logging
- Metrics
- CI/CD

---

The emphasis of this repository is evolving the software through changing business requirements before introducing infrastructure.

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
|
├── repositories/
│   |── __init__.py
│   |── book_repository.py
│   └── member_repository.py
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

- Requirement analysis
- Domain modeling
- Object-oriented design
- Responsibility assignment
- Aggregate design
- State transitions
- Business invariants
- SOLID & GRASP principles
- Test-driven evolution
- Clean architecture
- Incremental software evolution

---

## Status

Current milestone:

**Phase 1 — Complete**

- ✅ V1 Complete
- ✅ V2 Complete
- ✅ V3 Inventory Evolution
- ✅ V4 Search & Inventory Queries
- ✅ V5 Enineering Review

**Phase 2 — In Progress**
- Repository interfaces Complete
- In-memory Repository Complete