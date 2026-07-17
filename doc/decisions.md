# Design Decisions

## Why Book and BookCopy are separate
A Book models the bibliographic title.
A BookCopy models an individual physical copy with its own lifecycle.

---

## Why composition instead of inheritance
A BookCopy is not a specialized Book.
It is one physical instance of a Book.

---

## Why Library is the entry point
Library coordinates workflows while the domain objects encapsulate business behavior.

---

## Why Member stores BookCopy instead of barcode
The domain collaborates through object references instead of primitive identifiers.
Identifiers are used only at the application boundary.

---

## V2
- Book owns the waiting list.
- BookCopy owns reservation state.
- Reservation expiry is processed at the Book aggregate level.
- Overdue status is derived from borrowed copies instead of being stored.
- Member borrowing eligibility is computed dynamically.