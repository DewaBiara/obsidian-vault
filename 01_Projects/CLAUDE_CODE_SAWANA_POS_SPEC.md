# 🚀 CLAUDE CODE SPECIFICATION: KULA CLOUD POS SYSTEM (KULA POS)

> **Document Type:** Production Engineering Blueprint & Implementation Handover  
> **Brand & Identity:** **KULA POS** (*"The Pulse of Bali F&B — Fast, Offline-Proof Cloud POS"*)  
> **Author:** Thena (Hermes AI) for Dewa Biara  
> **Target Execution Agent:** Claude Code CLI  
> **Project Name:** `kula-pos`  
> **Testbed & Domain:** F&B Cloud POS (Sawana Coffee & Eatery, Ubud, Bali)  
> **Stack:** Go (Backend Modular Monolith), PostgreSQL (ACID Ledger), Redis (Streams & Cache), Next.js / Vite React PWA (Offline-First Cashier UI)
> **Design System:** Zinc Neutral (`#09090B`), Emerald Primary (`#059669`), Espresso Amber (`#D97706`), Lucide Icons (`1.75px` stroke)

---

## 1. Project Overview & Architecture Vision

Sawana POS is an ultra-lightweight, offline-first, high-throughput Point of Sale system designed to replace Moka POS for F&B operations. Unlike legacy cloud POS systems that lag on spotty WiFi and charge steep monthly subscription add-ons for recipes and employee slots, Sawana POS provides:
1. **Zero-Latency Ingestion:** Sub-15ms checkout with idempotent local UUIDv7 transaction deduplication.
2. **True Offline-First:** Cashier PWA runs on local IndexedDB/SQLite, prints directly to ESC/POS thermal printers via Web Bluetooth/TCP Socket port 9100, and kicks the cash drawer solenoid without waiting for cloud roundtrips.
3. **Automated COGS & Recipe Deduction:** Event-driven raw material inventory deduction via Redis Streams using Moving Weighted Average Costing.
4. **Audit-Proof Cash Shift Ledger:** Rigid shift management with blind cash count, mid-shift X-Report, closing Z-Report, and immutable discrepancy tracking.
5. **Native Reputation Loop:** Automatic review prompt for Google Maps 5-star ratings (ULASA integration) on digital receipts.

---

## 2. Recommended Codebase Directory Structure

```
sawana-pos/
├── cmd/
│   ├── api/
│   │   └── main.go                 # HTTP API Server entrypoint
│   └── worker/
│       └── main.go                 # Redis Stream Event Consumer (Inventory & Audit)
├── internal/
│   ├── config/                     # Environment configuration (Viper / cleanenv)
│   ├── database/                   # PostgreSQL connection & migrations
│   │   └── migrations/             # golang-migrate SQL files
│   ├── domain/                     # Pure domain entities & interfaces
│   │   ├── catalog.go
│   │   ├── inventory.go
│   │   ├── order.go
│   │   ├── payment.go
│   │   ├── shift.go
│   │   └── user.go
│   ├── handler/                    # HTTP Handlers (Chi or Echo router)
│   │   ├── catalog_handler.go
│   │   ├── inventory_handler.go
│   │   ├── order_handler.go
│   │   └── shift_handler.go
│   ├── service/                    # Core business logic implementations
│   │   ├── catalog_service.go
│   │   ├── checkout_service.go     # Idempotent checkout & ledger recording
│   │   ├── inventory_service.go    # Recipe BOM & moving average calculator
│   │   ├── printer_service.go      # ESC/POS byte generation & socket spooler
│   │   └── shift_service.go        # Cash reconciliation & X/Z reports
│   ├── repository/                 # PostgreSQL queries (sqlc generated or pure pgx)
│   │   ├── catalog_repo.go
│   │   ├── inventory_repo.go
│   │   ├── order_repo.go
│   │   └── shift_repo.go
│   └── platform/
│       ├── eventbus/               # Redis Stream publisher & consumer wrapper
│       └── printer/                # ESC/POS byte command builder (58mm / 80mm)
├── web/                            # Cashier Frontend (Next.js PWA / Vite React)
│   ├── src/
│   │   ├── components/             # Cashier grid, Cart, Numpad, Modal
│   │   ├── hooks/                  # useOfflineSync, useBluetoothPrinter
│   │   ├── stores/                 # Zustand store (Cart, Shift, Active Table)
│   │   └── lib/                    # IndexedDB outbox queue & ESC/POS generator
├── docker-compose.yml              # Local Postgres, Redis, and API services
├── Makefile                        # Build, migrate, test shortcuts
└── README.md
```

---

## 3. Production-Ready PostgreSQL Database Schema

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. MULTI-TENANCY & OUTLETS
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- SUBSCRIPTIONS & PLANS (FOR B2B SAAS MONETIZATION)
CREATE TYPE subscription_status AS ENUM ('TRIALING', 'ACTIVE', 'PAST_DUE', 'CANCELLED');

CREATE TABLE subscription_plans (
    id VARCHAR(50) PRIMARY KEY, -- 'starter_monthly', 'pro_monthly'
    name VARCHAR(100) NOT NULL,
    price NUMERIC(14,2) NOT NULL,
    max_outlets INT NOT NULL DEFAULT 1,
    max_devices_per_outlet INT NOT NULL DEFAULT 1,
    features JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE business_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID UNIQUE NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    plan_id VARCHAR(50) NOT NULL REFERENCES subscription_plans(id),
    status subscription_status NOT NULL DEFAULT 'TRIALING',
    trial_ends_at TIMESTAMPTZ,
    current_period_start TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    current_period_end TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE outlets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    address TEXT,
    phone VARCHAR(30),
    tax_percentage NUMERIC(5,2) NOT NULL DEFAULT 10.00,        -- PB1 Resto Tax (10%)
    service_charge_percentage NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- REGISTERED HARDWARE TERMINALS (DEVICE PAIRING)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    device_name VARCHAR(100) NOT NULL,
    pairing_code VARCHAR(10),
    pairing_code_expires_at TIMESTAMPTZ,
    device_token_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. USERS, ROLES & PIN ACCESS MATRIX
CREATE TYPE user_role AS ENUM ('OWNER', 'MANAGER', 'CASHIER', 'BARISTA');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255),
    role user_role NOT NULL DEFAULT 'CASHIER',
    pin_hash VARCHAR(255) NOT NULL,                           -- 4 or 6 digit PIN for fast cashier switch
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_permissions (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    can_apply_manual_discount BOOLEAN NOT NULL DEFAULT FALSE,
    can_void_transaction BOOLEAN NOT NULL DEFAULT FALSE,
    can_issue_refund BOOLEAN NOT NULL DEFAULT FALSE,
    can_open_cash_drawer BOOLEAN NOT NULL DEFAULT FALSE,
    can_reprint_receipt BOOLEAN NOT NULL DEFAULT FALSE,
    can_view_shift_history BOOLEAN NOT NULL DEFAULT FALSE
);

-- 3. SHIFTS & CASH RECONCILIATION LEDGER
CREATE TYPE shift_status AS ENUM ('OPEN', 'CLOSED');

CREATE TABLE shifts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ,
    starting_cash NUMERIC(14,2) NOT NULL DEFAULT 0.00,         -- Cash float in drawer
    total_cash_sales NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    total_cash_refunds NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    total_paid_in NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    total_paid_out NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    expected_cash NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    actual_cash NUMERIC(14,2),                                 -- Blind count entered by cashier
    difference_amount NUMERIC(14,2),                           -- actual - expected
    status shift_status NOT NULL DEFAULT 'OPEN',
    notes TEXT
);

CREATE TYPE cash_log_type AS ENUM ('PAID_IN', 'PAID_OUT');

CREATE TABLE shift_cash_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shift_id UUID NOT NULL REFERENCES shifts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    type cash_log_type NOT NULL,
    amount NUMERIC(14,2) NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. MENU CATALOG, VARIANTS & MODIFIERS
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,                                -- e.g., "Hot", "Iced Regular", "Iced Large"
    sku VARCHAR(50),
    base_price NUMERIC(14,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE modifier_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,                                -- e.g., "Dairy Option", "Syrup Flavour"
    min_selection INT NOT NULL DEFAULT 0,
    max_selection INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE modifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL REFERENCES modifier_groups(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,                                -- e.g., "Oat Milk", "Caramel Syrup"
    extra_price NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- 5. RAW MATERIALS, RECIPES (BOM) & INVENTORY LEDGER
CREATE TABLE raw_materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,                                -- e.g., "Arabica Espresso Blend", "Fresh Milk"
    unit VARCHAR(20) NOT NULL,                                 -- 'gram', 'ml', 'pcs'
    current_stock NUMERIC(14,3) NOT NULL DEFAULT 0.000,
    average_cost NUMERIC(14,2) NOT NULL DEFAULT 0.00,          -- Moving weighted average cost per unit
    min_alert_stock NUMERIC(14,3) NOT NULL DEFAULT 0.000,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    raw_material_id UUID NOT NULL REFERENCES raw_materials(id) ON DELETE CASCADE,
    quantity_required NUMERIC(14,3) NOT NULL,                  -- e.g., 18.000 (grams)
    UNIQUE(variant_id, raw_material_id)
);

CREATE TYPE inventory_log_type AS ENUM (
    'SALE_DEDUCTION', 
    'PURCHASE_RECEIPT', 
    'WASTE', 
    'TRANSFER_IN', 
    'TRANSFER_OUT', 
    'ADJUSTMENT'
);

CREATE TABLE inventory_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_material_id UUID NOT NULL REFERENCES raw_materials(id) ON DELETE CASCADE,
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    type inventory_log_type NOT NULL,
    delta_qty NUMERIC(14,3) NOT NULL,                          -- negative for sales/waste, positive for purchase
    balance_qty NUMERIC(14,3) NOT NULL,
    unit_cost NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    reference_id UUID,                                         -- order_id or purchase_order_id
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. ORDERS, PAYMENTS & DOUBLE-ENTRY CHECKOUT
CREATE TYPE order_status AS ENUM ('DRAFT', 'COMPLETED', 'VOID', 'REFUNDED');
CREATE TYPE sales_channel AS ENUM ('DINE_IN', 'TAKEAWAY', 'ONLINE_DELIVERY');

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_order_uuid UUID UNIQUE NOT NULL,                    -- Idempotency key generated at POS Edge
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    shift_id UUID REFERENCES shifts(id) ON DELETE SET NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    invoice_number VARCHAR(60) NOT NULL,                       -- e.g., "SWN/20261001/0001"
    sales_channel sales_channel NOT NULL DEFAULT 'DINE_IN',
    table_number VARCHAR(20),
    subtotal NUMERIC(14,2) NOT NULL,
    discount_amount NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    service_charge_amount NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    tax_amount NUMERIC(14,2) NOT NULL DEFAULT 0.00,            -- PB1 10%
    total_amount NUMERIC(14,2) NOT NULL,
    total_cogs NUMERIC(14,2) NOT NULL DEFAULT 0.00,            -- Cost of goods sold calculated from BOM
    status order_status NOT NULL DEFAULT 'COMPLETED',
    void_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    synced_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES product_variants(id),
    item_name VARCHAR(150) NOT NULL,
    unit_price NUMERIC(14,2) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    subtotal NUMERIC(14,2) NOT NULL,
    cogs_amount NUMERIC(14,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE order_item_modifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_item_id UUID NOT NULL REFERENCES order_items(id) ON DELETE CASCADE,
    modifier_id UUID NOT NULL REFERENCES modifiers(id),
    modifier_name VARCHAR(100) NOT NULL,
    extra_price NUMERIC(14,2) NOT NULL DEFAULT 0.00
);

CREATE TYPE payment_tender AS ENUM ('CASH', 'QRIS', 'EDC_DEBIT', 'EDC_CREDIT', 'SPLIT');

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    tender_type payment_tender NOT NULL,
    amount_tendered NUMERIC(14,2) NOT NULL,
    change_given NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    reference_number VARCHAR(100),                             -- QRIS Transaction ID / EDC Auth Code
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- INDEXES FOR HIGH-THROUGHPUT LOOKUPS
CREATE INDEX idx_orders_outlet_created ON orders (outlet_id, created_at DESC);
CREATE INDEX idx_orders_shift ON orders (shift_id);
CREATE INDEX idx_inventory_logs_raw_mat ON inventory_logs (raw_material_id, created_at DESC);
CREATE INDEX idx_raw_materials_outlet ON raw_materials (outlet_id);
```

---

## 4. Key Business Logic & Algorithms

### A. Idempotent Ingestion Pattern (Clean Architecture UseCase)
```go
package usecase

import (
	"context"
	"kula-pos/internal/core/domain"
	"kula-pos/internal/core/ports"
)

type CheckoutUseCase struct {
	txManager      ports.TxManager
	orderRepo      ports.OrderRepository
	shiftRepo      ports.ShiftRepository
	eventPublisher ports.EventPublisher
}

func NewCheckoutUseCase(
	tx ports.TxManager, 
	order ports.OrderRepository, 
	shift ports.ShiftRepository, 
	pub ports.EventPublisher,
) ports.CheckoutUseCase {
	return &CheckoutUseCase{
		txManager:      tx,
		orderRepo:      order,
		shiftRepo:      shift,
		eventPublisher: pub,
	}
}

func (uc *CheckoutUseCase) ProcessCheckout(ctx context.Context, cmd domain.CheckoutCommand) (*domain.Order, error) {
	// 1. Idempotency Check: if order already processed at edge, return without re-charging
	existing, err := uc.orderRepo.FindByClientUUID(ctx, cmd.ClientOrderUUID)
	if err == nil && existing != nil {
		return existing, nil
	}

	var createdOrder *domain.Order

	// 2. Execute within atomic business transaction managed by outbound port
	err = uc.txManager.WithinTransaction(ctx, func(txCtx context.Context) error {
		order, err := uc.orderRepo.CreateOrder(txCtx, cmd)
		if err != nil {
			return err
		}

		if cmd.PaymentTender == domain.TenderCash {
			if err := uc.shiftRepo.AddCashSales(txCtx, cmd.ShiftID, cmd.TotalAmount); err != nil {
				return err
			}
		}

		createdOrder = order
		return nil
	})

	if err != nil {
		return nil, err
	}

	// 3. Asynchronously emit OrderCompletedEvent to Redis Stream for Recipe BOM deduction
	_ = uc.eventPublisher.Publish(ctx, "orders.completed", domain.OrderCompletedEvent{
		OrderID:   createdOrder.ID,
		OutletID:  createdOrder.OutletID,
		Items:     cmd.Items,
	})

	return createdOrder, nil
}
```

### B. Moving Average Cost (MAC) Formula for Inventory
When purchasing new stock (`PurchaseOrder`):
$$NewAverageCost = \frac{(CurrentStock \times CurrentCost) + (ReceivedQty \times PurchasePrice)}{CurrentStock + ReceivedQty}$$

### C. ESC/POS Hardware Printing Utility (Go)
To print to network thermal printers (Port 9100) or generate byte streams for Web Bluetooth:
```go
package printer

import (
	"bytes"
	"net"
	"time"
)

var (
	CmdInit       = []byte{0x1B, 0x40}             // ESC @ (Initialize printer)
	CmdCut        = []byte{0x1D, 0x56, 0x41, 0x00} // GS V 65 0 (Full Cut)
	CmdDrawerKick = []byte{0x1B, 0x70, 0x00, 0x19, 0xFA} // ESC p 0 25 250 (RJ11 solenoid pulse)
	CmdBoldOn     = []byte{0x1B, 0x45, 0x01}
	CmdBoldOff    = []byte{0x1B, 0x45, 0x00}
	CmdAlignLeft  = []byte{0x1B, 0x61, 0x00}
	CmdAlignCenter= []byte{0x1B, 0x61, 0x01}
)

func KickDrawerAndPrintReceipt(printerIP string, receiptText []byte) error {
	conn, err := net.DialTimeout("tcp", printerIP+":9100", 2*time.Second)
	if err != nil {
		return err
	}
	defer conn.Close()

	var buf bytes.Buffer
	buf.Write(CmdInit)
	buf.Write(CmdDrawerKick) // Kick cash drawer immediately
	buf.Write(receiptText)
	buf.Write([]byte("\n\n\n"))
	buf.Write(CmdCut)

	_, err = conn.Write(buf.Bytes())
	return err
}
```

---

## 5. Phased Execution Prompts for Claude Code

Execute the following prompts step-by-step inside the `sawana-pos` workspace:

### Prompt 1: Project Scaffolding & Database Layer
```bash
claude "Initialize a clean Go 1.22+ backend in this directory. 
1. Use Go Chi for HTTP routing, pgxpool for PostgreSQL connection, and cleanenv for environment variables.
2. Create the migrations directory with the full PostgreSQL schema provided in CLAUDE_CODE_SAWANA_POS_SPEC.md.
3. Write domain models and repository queries for Businesses, Outlets, Users, and Categories using pure SQL / sqlc pattern.
4. Include a docker-compose.yml for local Postgres and Redis."
```

### Prompt 2: Shift & Cash Ledger Engine
```bash
claude "Implement the Shift & Cash Ledger module.
1. Endpoints: POST /api/v1/shifts/open, POST /api/v1/shifts/cash-log (paid-in/paid-out), POST /api/v1/shifts/close.
2. Implement blind cash count logic: cashier submits actual_cash without knowing expected_cash; the service computes difference_amount and updates status to CLOSED.
3. Add handler to generate the Z-Report closing summary."
```

### Prompt 3: Idempotent Checkout & Redis Event Pipeline
```bash
claude "Build the Idempotent Order Checkout service.
1. Endpoint: POST /api/v1/orders/checkout with client_order_uuid idempotency guard.
2. Support CASH and QRIS payments. For CASH payments, increment total_cash_sales on the active shift.
3. Setup a Redis Stream publisher for 'orders.completed'.
4. Create a background worker in cmd/worker/main.go that consumes 'orders.completed', fetches recipe BOM for each item variant, deducts raw_materials stock, and writes to inventory_logs."
```

### Prompt 4: ESC/POS Thermal Printing & Frontend Cashier PWA
```bash
claude "Implement the thermal printer service in internal/platform/printer and setup the web cashier interface:
1. Go ESC/POS command builder for 58mm and 80mm receipts with RJ11 drawer kick command.
2. In /web, create a lightweight Next.js / Tailwind CSS Cashier screen:
   - Product Grid with category tabs
   - Cart with Variant & Modifier selection
   - Quick Cash buttons (Pas, 50k, 100k) & QRIS modal
   - IndexedDB outbox queue that stores orders if offline and pushes to /api/v1/orders/checkout when online."
```
