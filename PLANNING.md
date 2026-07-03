# PesaTrack - Planning Document

## Functional Requirements
1. A user can create an account and log in securely.
2. A user can create custom categories (e.g., "Groceries," "Transport," "Rent") - categories are private to each user, not shared globally.
3. A user can record a transaction: an amount, a category, a date, a type (income or expense), and an optional note.
4. A user can set a monthly budget limit per category.
5. A user can view a dashboard summarizing total income, total expenses, and spending per category for the current month, with a visual indicator when a category exceeds its budget.
6. A user can only ever view, edit, or delete their own transactions, categories, and budgets - never another user's .
7. Staff users can view aggregate, anonymized platform statistics (e.g., "total number of transactions logged platform-wide this month") but cannot view any individual user's specific transaction data (a deliberate, realistic privacy boundary for a financial application).
8. The system sends each user a monthly summary email of their spending.
9. All core resources (transactions, categories, budgets) are available via a REST API, authenticated via tokens, for future mobile/frontend clients.

## Entity-Relationship Diagram

```
┌─────────────────────┐
│        User           │
├────────────────────┤
│ id (PK)               │
│ username               │
│ email                  │
│ password (hashed)      │
│ is_staff                │
│ date_joined              │
└──────────┬───────────┘
           │ 1
           │
           │ owns
           │ N
┌──────────▼───────────┐         ┌─────────────────────┐
│      Category          │         │       Budget           │
├─────────────────────┤         ├─────────────────────┤
│ id (PK)                │◄────────│ id (PK)               │
│ user (FK → User)        │  1    N │ category (FK)         │
│ name                    │         │ user (FK → User)      │
│ created_at              │         │ monthly_limit (Decimal)│
└──────────┬───────────┘         │ created_at             │
           │ 1                     └─────────────────────┘
           │
           │ has many
           │ N
┌──────────▼───────────┐
│      Transaction        │
├─────────────────────┤
│ id (PK)                │
│ user (FK → User)        │
│ category (FK → Category)│
│ amount (Decimal)         │
│ transaction_type         │  (income / expense)
│ date                      │
│ note                      │
│ created_at                │
└─────────────────────────┘
```



## Architectural Decisions
- Custom User model, configured before first migration
- Apps: accounts, finance, dashboard
- API: full ModelViewSets per resource, token-authenticated, object-level IsOwner permission
- Background tasks: Celery + Redis for monthly summary emails
- Deployment: Docker Compose from the start