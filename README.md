# Petrol Pump Management

Complete Petrol Pump / Fuel Station Management Application built on **Frappe 15 / ERPNext 15**.

**Publisher:** Bizaxl Optimisations LLP | markcom@bizaxl.com | +91 98867 11156 | bizaxl.com

---

## Install

```bash
bench get-app https://github.com/Sudhakar1110/petrol_pump_management.git
bench --site your-site install-app petrol_pump_management
bench --site your-site migrate
bench --site your-site fix-workspace
bench build
bench restart
```

---

## App Stats

| Category | Count |
|----------|-------|
| DocTypes | 56 |
| Reports | 33 |
| Roles | 7 |
| Scheduler Tasks | 15 |

---

## Module Layers

| Layer | Description | Key DocTypes |
|-------|-------------|-------------|
| **Layer 1** — Configuration | Station setup, tank & nozzle config, fuel pricing | Station Configuration, Tank Master, Nozzle Master, Fuel Price Master, Employee Master |
| **Layer 2** — Operations | Shift-wise sales, meter readings, daily stock | Shift, Fuel Sale, Meter Reading, Daily Stock Register, Stock Purchase Decantation |
| **Layer 3** — Credit & ANPR | Vehicle credit billing, limit tracking | Vehicle Master, PP Customer, Credit Sale Invoice, Credit Limit Ledger, ANPR Scan Log |
| **Layer 4** — Compliance | GST, payroll, financial reports | GSTR-1/3B Filing, Salary Slip Entry, Expense Entry, Tally Export Log |

---

## Operational Workflows

### Workflow A — Vehicle-based Credit Billing (ANPR)

```
Vehicle Arrival
  → ANPR Camera captures plate → OCR reads plate number
  → Vehicle Master match (confidence check)
  → Credit Limit Ledger validation (available balance)
  → Manager override if over limit
  → Fuel Sale created
  → Auto Credit Sale Invoice generated
  → SMS receipt sent → Credit Points awarded
  → Credit Limit Ledger updated in real time
```

### Workflow B — Shift & Fuel Sales Operations

```
Shift Start
  → Manager allots nozzles + opening cash to salesman
  → Opening meter readings recorded per nozzle
  → Sales during shift (Cash / Credit / Card / UPI / Petro-card)
  → Closing meter readings taken
  → Tank dip check → Compared against calculated stock
  → Shift settlement: Cash collected vs expected, shortages flagged
  → Closing cash handed over → Settlement approved
```

### Workflow C — Stock & Tank Management

```
Purchase order placed
  → Tanker (TT) arrival logged → Trip Voucher created
  → Pre-unload dip & density recorded
  → Fuel decanted into designated tank
  → Tank-wise stock updated → Variance flagged
  → Daily stock register auto-computed: opening + purchase - sale = closing
  → Low-stock alerts triggered → Reorder notifications sent
```

### Workflow D — Credit Recovery & Compliance

```
Period-wise statements auto-generated per credit customer
  → Overdue balances trigger SMS/email reminders
  → Interest charged on late payments (configurable grace days)
  → Payments recorded (cash/bank/swipe) against outstanding invoices
  → Bank reconciliation via CSV import + auto-matching
  → GST reports generated: GSTR-1, GSTR-3B, TCS, TDS
  → Tally export for accounting sync
```

### Workflow E — Employee & Payroll

```
Shift-wise attendance marked → Salary type set (Paid/Unpaid)
  → Leave applications processed → Overtime hours logged
  → Monthly salary slips auto-generated
  → Advances deducted from salary
  → Commission calculated based on fuel sold
  → Payroll summary report generated
```

### Workflow F — Digital Payments & Settlement

```
Card/UPI/E-Wallet transactions at POS
  → Swipe Settlement records per machine
  → Petro Card transactions tracked
  → Machine-wise settlement reconciliation
  → Difference flagged if mismatch
```

---

## Implemented Features

### DocTypes (56)

**Configuration (8):** Station Configuration, Tank Master, Tank Dip Chart, Nozzle Master, Fuel Price Master, Employee Master, Commission Rule, PP Supplier Master

**Operations (13):** Shift, Shift Nozzle Allotment, Fuel Sale, Meter Reading, Daily Stock Register, Stock Purchase Decantation, Trip Voucher, Lube Stock, Evaporation Loss, Tanker Expense, Bank Statement Import, Station Inspection, Day Settlement

**Credit & Sales (9):** PP Customer, Vehicle Master, Credit Sale Invoice, Credit Statement, Credit Recovery Entry, Credit Limit Ledger, Payment Receipt, Payment Receipt Invoice, ANPR Scan Log

**Finance & HR (11):** Expense Entry, Income Entry, Attendance Register, Leave Application, Overtime Log, Advance Amount, Salary Slip Entry, Commission Payment, Bank Deposit, Cheque Print Queue, Reward Points Ledger

**Digital Payments (2):** Swipe Settlement, Petro Card Transaction

**Compliance & GST (8):** GSTR-1 Filing, GSTR-1 Filing Invoice, GSTR-3B Filing, GSTR-2A Reconciliation, TCS Statement, TDS Statement, Bank Reconciliation Entry, Tally Export Log

**Notifications (3):** SMS Log, Email Log, PP Notification Settings

**Child Tables (2):** Bank Statement Transaction, Inspection Nozzle Reading

### Reports (33)

Daily Sales Summary, Shift Settlement Report, Stock Variation Report, Credit Customer Ageing, ANPR Scan Report, GST VAT Summary, Employee Attendance Payroll, Fuel Rate Variation Report, Density Dip Variation, Profit Loss Statement, Vehicle Wise Consumption, Swipe Digital Settlement, Expense Summary, Bank Deposit Report, Bank Reconciliation Report, GSTR-1 Summary, GSTR-3B Summary, GSTR-2A Reconciliation Report, HSN Wise Summary, TCS TDS Report, Employee Commission Report, Cash Flow Report, PP Day Book, Payroll Summary, Tally Export Report, Report Export, Nozzle Wise Sale, Meter Dip Variation, Employee Shortage Report, Monthly Shortage Report, Machine Wise Transaction, Tank Valuation Report, Sales Officer Inspection

---

## Missing Features & Why They Cannot Be Implemented

### Mobile Apps
| Feature | Reason |
|---------|--------|
| Dealer/Manager/DSM/Credit User mobile apps | Requires React Native/Flutter development — not part of Frappe web framework |

### External Integrations
| Feature | Reason |
|---------|--------|
| ANPR Camera / OCR | Requires physical camera hardware + third-party OCR API |
| Fuel Dispenser / Pump Controller | Requires hardware integration with dispenser brands |
| Fleet / GPS Tracking | Requires GPS hardware + third-party API |
| WhatsApp integration | Requires WhatsApp Business API + Meta approval |
| Payment Gateway (Razorpay/PhonePe) | Requires merchant account + API keys |
| Bank auto-import (real API) | Banks don't offer open APIs — CSV upload works |
| GST portal auto-submit | Requires Digital Signature Certificate (DSC) + GSTN registration |
| Tally real-time sync | Requires Tally Gateway (ODBC) + Tally installed on same network |

### Minor Missing
| Feature | Reason |
|---------|--------|
| Graphical dashboard | Frappe Number Cards/Charts exist but need manual UI configuration |
| Cheque printing layout | Requires bank-specific cheque format + printer |
| Full accounting vouchers | Needs deep ERPNext accounting module integration |
| Multi-outlet support | Single station only — needs architecture changes |

---

## Roles

| Role | Access |
|------|--------|
| System Manager | Full access to all DocTypes |
| Station Manager | Full operations, read compliance |
| Salesman DSM | Own shift records, create fuel sales |
| Credit Accounts Officer | Full credit management |
| Compliance Officer | Full GST/compliance |
| Recovery Officer | Credit recovery management |
| Petrol Pump Auditor | Read-only across all DocTypes |

---

## Scheduler Tasks

| Schedule | Task | Description |
|----------|------|-------------|
| Daily | Stock Reconciliation | Auto-compute daily stock register per tank |
| Daily | Credit Reminders | SMS for overdue invoices |
| Daily | Stock Level Check | Alert for low stock |
| Daily | Auto-block Customers | Block on limit breach + SMS |
| Daily | Expiry Alerts | Lube expiry notifications |
| Daily | Expire Reward Points | Points older than 1 year |
| Daily | Evaporation Calc | Tank-wise evaporation loss |
| Daily | Business Summary SMS | Daily summary to manager |
| Daily | Birthday SMS | Birthday greetings |
| Weekly | Credit Statements | Auto-generate weekly statements |
| Weekly | Credit Email | Email statements to customers |
| Monthly | Monthly Reports | Business reports |
| Monthly | Late Interest | Interest on overdue invoices |
| Monthly | Auto Payroll | Salary slips for all employees |
| Monthly | Auto Commission | Commission for salesmen |
