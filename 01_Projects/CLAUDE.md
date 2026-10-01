# CLAUDE.md — KULA POS Project Guide (Strict Clean Architecture)

> **Project Name:** KULA POS (`kula-pos`)  
> **Brand Tagline:** *"The Pulse of Bali F&B — Fast, Offline-Proof Cloud POS"*  
> **Target Venue & Testbed:** Sawana Coffee & Eatery, Ubud, Bali  
> **Architecture Pattern:** Strict Clean Architecture (Hexagonal / Ports & Adapters) in Go

---

## 🛠️ Technology Stack & Standards

- **Backend:** Go 1.22+
  - Router: `chi` (`github.com/go-chi/chi/v5`)
  - Database Driver: `pgx` (`github.com/jackc/pgx/v5/pgxpool`)
  - Config: `cleanenv` (`github.com/ilyakaznacheev/cleanenv`)
  - Cache & Stream: `go-redis` (`github.com/redis/go-redis/v9`)
- **Database:** PostgreSQL 16+ (ACID Ledger, UUIDv7, Row-Level Security)
- **Frontend Apps (`/apps`):**
  - `apps/pos`: Vite + React + Tailwind CSS PWA (Offline-first with IndexedDB via `idb`, Web Bluetooth API, Zustand)
  - `apps/backoffice`: Next.js 14+ (App Router) + Tailwind CSS + Shadcn UI + TanStack React Query + Recharts
- **Iconography:** `lucide-react` (stroke width `1.75px`)
- **Theme Palette:** Zinc-950 neutral base (`#09090B`), Emerald-600 action accent (`#059669`), Espresso Amber (`#D97706`). Tabular monospace numbers for all IDR currency.

---

## 🏛️ Strict Clean Architecture Directory Layout

```
kula-pos/
├── cmd/
│   ├── api/main.go                     # Composition Root (Dependency Injection) for HTTP API
│   └── worker/main.go                  # Composition Root for Redis Stream Background Workers
├── internal/
│   ├── core/                           # PURE BUSINESS LOGIC (Zero external framework imports)
│   │   ├── domain/                     # Entities, Value Objects, Domain Errors
│   │   │   ├── order.go
│   │   │   ├── shift.go
│   │   │   ├── catalog.go
│   │   │   ├── inventory.go
│   │   │   └── errors.go               # ErrOrderAlreadyProcessed, ErrShiftClosed, etc.
│   │   ├── ports/                      # Contracts (Inbound & Outbound Interfaces)
│   │   │   ├── inbound.go              # UseCase Interfaces (OrderUseCase, ShiftUseCase)
│   │   │   └── outbound.go             # Repository, EventPublisher, and Printer Ports
│   │   └── usecase/                    # Application Business Rules (Implements Inbound Ports)
│   │       ├── checkout_usecase.go
│   │       ├── shift_usecase.go
│   │       └── inventory_usecase.go
│   └── adapter/                        # INFRASTRUCTURE & DELIVERY (Implements Outbound Ports)
│       ├── inbound/                    # Driving Adapters
│       │   ├── http/                   # Chi REST Handlers, DTO validation, HTTP serializers
│       │   └── worker/                 # Redis Stream Event Consumers
│       └── outbound/                   # Driven Adapters
│           ├── postgres/               # pgx implementation of repository interfaces & TxManager
│           ├── redis/                  # Redis Stream event publisher implementation
│           └── printer/                # ESC/POS TCP & Bluetooth byte streamer
├── migrations/                         # golang-migrate SQL files
├── apps/
│   ├── pos/                            # Cashier PWA (touch-first, offline-first)
│   └── backoffice/                     # Owner & manager web dashboard
├── docker-compose.yml
└── Makefile
```

---

## ⚡ Core Rules & Clean Architecture Invariants

1. **The Dependency Rule (Inward Only):**
   - `core/domain` and `core/usecase` must NEVER import `github.com/jackc/pgx`, `net/http`, `github.com/go-chi/chi`, or `github.com/redis/go-redis`.
   - Business rules must be 100% testable with mock ports without spinning up databases or HTTP servers.
2. **Transaction Management via UnitOfWork / TxManager Port:**
   - Use cases must not execute raw SQL or manage database transactions directly. Use an outbound `TxManager` port:
     ```go
     type TxManager interface {
         WithinTransaction(ctx context.Context, fn func(ctx context.Context) error) error
     }
     ```
3. **Idempotency & Zero Duplication:**
   - Every order has a `client_order_uuid`. If already committed, the usecase returns the existing entity idempotently without raising an error.
4. **Asynchronous Recipe Deduction:**
   - The checkout use case commits the order and publishes an `OrderCompletedEvent` through the `EventPublisher` port.
   - The worker adapter listens to Redis Streams and invokes `InventoryUseCase.DeductBOM(ctx, event)`.
