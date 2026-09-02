# Petrol Pump Management

**Complete Petrol Pump / Fuel Station Management Application**
Built on Frappe 15 / ERPNext 15

**Publisher:** Bizaxl Optimisations LLP
**Contact:** markcom@bizaxl.com | +91 98867 11156 | bizaxl.com

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

## Module Overview

| Layer | Description | DocTypes |
|-------|-------------|----------|
| **Layer 1** — Admin & Configuration | Station setup, tank & nozzle config, fuel pricing | Station Configuration, Tank Master, Nozzle Master, Fuel Price Master, Employee Master, Commission Rule, PP Supplier Master, Notification Settings |
| **Layer 2** — Shift, Sales & Stock | Shift-wise nozzle allotment, meter readings, daily stock register | Shift, Shift Nozzle Allotment, Fuel Sale, Meter Reading, Daily Stock Register, Stock Purchase Decantation, Trip Voucher, Lube Stock, Evaporation Loss, Tanker Expense, Bank Statement Import, Station Inspection, Day Settlement |
| **Layer 3** — Vehicle, Credit & ANPR | Vehicle-linked customer profiles, credit limit & points, ANPR billing | Vehicle Master, PP Customer, Credit Sale Invoice, Credit Statement, Credit Recovery Entry, Credit Limit Ledger, Payment Receipt, ANPR Scan Log |
| **Layer 4** — Accounts, Compliance & Reporting | GST/Tally sync, payroll, financial statements | Expense Entry, Income Entry, Attendance Register, Leave Application, Overtime Log, Advance Amount, Salary Slip Entry, Commission Payment, Bank Deposit, Cheque Print Queue, Reward Points Ledger, Swipe Settlement, Petro Card Transaction, GSTR-1 Filing, GSTR-3B Filing, GSTR-2A Reconciliation, TCS Statement, TDS Statement, Bank Reconciliation Entry, Tally Export Log, SMS Log, Email Log |

---

## Operational Workflows

### Workflow A — Vehicle-based Credit Billing (ANPR)

```
Vehicle Arrival → ANPR Camera captures plate → OCR reads plate
    → Vehicle Master match (confidence check)
    → Credit Limit Ledger validation (available balance check)
    → Manager override if over limit
    → Fuel Sale created → Auto Credit Sale Invoice generated
    → SMS/WhatsApp receipt sent → Credit Points awarded
    → Credit Limit Ledger updated in real time
```

**DocTypes involved:** ANPR Scan Log → Vehicle Master → Credit Limit Ledger → Fuel Sale → Credit Sale Invoice → SMS Log → Reward Points Ledger

### Workflow B — Shift & Fuel Sales Operations

```
Shift Start → Manager allots nozzles + opening cash to salesman
    → Opening meter readings recorded per nozzle
    → Sales during shift (Cash / Credit / Card / UPI / Petro-card)
    → Closing meter readings taken
    → Tank dip check → Compared against calculated stock movement
    → Shift settlement: Cash collected vs expected, shortages flagged
    → Closing cash handed over → Settlement approved and locked
```

**DocTypes involved:** Shift → Shift Nozzle Allotment → Meter Reading → Fuel Sale → Day Settlement → Swipe Settlement

### Workflow C — Stock & Tank Management

```
Purchase order placed → Tanker (TT) arrival logged → Trip Voucher created
    → Pre-unload dip & density recorded
    → Fuel decanted into designated tank
    → Tank-wise stock updated → Variance flagged
    → Daily stock register auto-computed: opening + purchase - sale = closing
    → Low-stock alerts triggered → Reorder notifications sent
```

**DocTypes involved:** Trip Voucher → Stock Purchase Decantation → Tank Master → Daily Stock Register → Evaporation Loss → Lube Stock

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

**DocTypes involved:** Credit Statement → Credit Recovery Entry → Payment Receipt → Bank Statement Import → GSTR-1 Filing → GSTR-3B Filing → TCS Statement → TDS Statement → Tally Export Log

### Workflow E — Employee & Payroll

```
Shift-wise attendance marked → Salary type set (Paid/Unpaid)
    → Leave applications processed → Overtime hours logged
    → Monthly salary slips auto-generated
    → Advances deducted from salary
    → Commission calculated based on fuel sold
    → Payroll summary report generated
```

**DocTypes involved:** Attendance Register → Leave Application → Overtime Log → Advance Amount → Salary Slip Entry → Commission Payment

### Workflow F — Digital Payments & Settlement

```
Card/UPI/E-Wallet transactions at POS
    → Swipe Settlement records per machine
    → Petro Card transactions tracked
    → Machine-wise settlement reconciliation
    → Difference flagged if mismatch
```

**DocTypes involved:** Swipe Settlement → Petro Card Transaction → Machine Wise Transaction Report

---

## Implemented Features (56 DocTypes, 33 Reports)

### Configuration
- Station Configuration (station name, licence, GST, currency, contact)
- Tank Master (fuel type, capacity, dip chart, stock level, safe level)
- Tank Dip Chart (dip cm to volume mapping)
- Nozzle Master (linked to tank, pump, meter reading, status: Open/Stop/Reset)
- Fuel Price Master (effective date, rate per litre, revision history)
- Employee Master (role, salary type, mobile, joining date)
- Commission Rule (per fuel type/qty thresholds)
- PP Supplier Master

### Operations
- Shift (salesman assignment, opening cash, settlement status)
- Shift Nozzle Allotment (child table for nozzle assignments)
- Fuel Sale (nozzle, quantity, rate, payment mode, vehicle/customer link)
- Meter Reading (opening/closing, testing qty, sale qty)
- Daily Stock Register (opening, purchase, sale, closing, variation)
- Stock Purchase Decantation (invoiced vs received, density, variation)
- Trip Voucher (tanker trip tracking)
- Lube Stock (lube inventory with expiry & reorder alerts)
- Evaporation Loss (fuel loss tracking with threshold alerts)
- Tanker Expense (tanker trip P&L with cost breakdown)
- Bank Statement Import (CSV upload + auto-matching)
- Station Inspection (dip, density, temperature, nozzle readings)
- Day Settlement (end-of-day reconciliation)

### Credit & Sales
- PP Customer (type, GST, address, credit limit, points, risk category, block status)
- Vehicle Master (plate number, type, customer link, ANPR status)
- Credit Sale Invoice (customer, vehicle, amount, due date, interest, status)
- Credit Statement (period-wise billing with invoice details)
- Credit Recovery Entry (discount/waiver, grace days, balance calculation)
- Credit Limit Ledger (limit, used, available, auto-block)
- Payment Receipt (customer, mode, amount, reference)
- ANPR Scan Log (plate, camera, confidence, action taken)

### Finance & HR
- Expense Entry (date, type, amount, payment method)
- Income Entry (type, source, amount, recurring)
- Attendance Register (shift-wise, salary type)
- Leave Application (employee, dates, status)
- Overtime Log (hours, pay calculation)
- Advance Amount (employee, amount, recovery)
- Salary Slip Entry (basic, OT, commission, deductions, net pay)
- Commission Payment (auto-calculated from rules)
- Bank Deposit (amount, date, bank reference)
- Cheque Print Queue (payee, amount, words, status)
- Reward Points Ledger (earn/redeem/expire tracking)

### Digital Payments
- Swipe Settlement (machine, payment mode, collected vs sale)
- Petro Card Transaction (card number, amount, type)

### Compliance & GST
- GSTR-1 Filing (B2B invoices, XML generation, HSN summary)
- GSTR-3B Filing (auto-calculation, XML generation)
- GSTR-2A Reconciliation (purchase matching)
- TCS Statement (auto-calculation)
- TDS Statement (auto-calculation)
- Bank Reconciliation Entry
- Tally Export Log (export tracking)

### Notifications
- SMS Log (Twilio/MSG91/custom gateway)
- Email Log (Frappe email system)
- PP Notification Settings (gateway config + message templates)

---

## Implemented Reports (33 Reports)

| Report | Description |
|--------|-------------|
| Daily Sales Summary | Shift-wise, nozzle-wise, payment-mode-wise sales |
| Shift Settlement Report | Cash collected vs expected, shortages |
| Stock Variation Report | Tank-wise dip vs meter-sale variance |
| Credit Customer Ageing | Outstanding dues by age bucket |
| ANPR Scan Report | Scan stats, auto-matched vs manual |
| GST VAT Summary | GST summary with CGST/SGST |
| Employee Attendance Payroll | Attendance, salary, commission summary |
| Fuel Rate Variation Report | Historical rate changes |
| Density Dip Variation | Tank-wise density vs stock |
| Profit Loss Statement | Trading account, expenses, margin |
| Vehicle Wise Consumption | Fuel consumption per vehicle |
| Swipe Digital Settlement | Card/UPI/e-wallet reconciliation |
| Expense Summary | Expense breakdown |
| Bank Deposit Report | Deposit history |
| Bank Reconciliation Report | Reconciliation status |
| GSTR-1 Summary | B2B credit sales for GST filing |
| GSTR-3B Summary | Monthly GST return |
| GSTR-2A Reconciliation Report | Purchase matching |
| HSN Wise Summary | HSN code-wise product summary |
| TCS TDS Report | Combined TCS/TDS statement |
| Employee Commission Report | Employee-wise sales & commission |
| Cash Flow Report | Daily cash inflows/outflows |
| PP Day Book | All transactions for a date |
| Payroll Summary | Employee-wise salary details |
| Tally Export Report | Export history |
| Report Export | CSV/Excel export |
| Nozzle Wise Sale | Per-nozzle sales with payment split |
| Meter Dip Variation | Meter sale vs dip reading |
| Employee Shortage Report | Per-employee cash shortage |
| Monthly Shortage Report | Monthly aggregated shortage |
| Machine Wise Transaction | POS machine-wise breakdown |
| Tank Valuation Report | Stock value & utilization |
| Sales Officer Inspection | Inspection records |

---

## Missing Features — Why They Can't Be Implemented

### Mobile Apps (Cannot Implement)

| Feature | Reason |
|---------|--------|
| Dealer / Owner mobile app | Requires separate React Native/Flutter development — not part of Frappe web framework |
| Manager-level mobile app | Same — needs native mobile app codebase |
| Salesman / DSM mobile app | Same — needs native mobile app codebase |
| Credit-customer self-service app | Credit Portal page exists but full mobile app needs separate development |

**Why:** Mobile apps require platform-specific development (iOS/Android), app store deployment, push notification setup, and ongoing maintenance. Frappe is a web framework — it provides web pages but not native mobile apps.

### External Integrations (Cannot Implement)

| Feature | Reason |
|---------|--------|
| ANPR Camera / OCR integration | Requires physical camera hardware at nozzle bay + third-party OCR API (OpenALPR, Plate Recognizer) |
| Fuel Dispenser / Pump Controller | Requires hardware integration with specific dispenser brands (Gilbarco, Tokheim) — needs physical device |
| Fleet / GPS Tracking | Requires GPS hardware installed in vehicles + third-party tracking API |
| WhatsApp integration | Requires WhatsApp Business API account + Meta verification and approval |
| Payment Gateway (Razorpay/PhonePe) | Requires payment provider merchant account + API keys + KYC |
| Bank auto-import (real API) | Banks don't offer open APIs — CSV/manual upload already works |
| GST portal auto-submit | Requires Digital Signature Certificate (DSC) + GSTN portal registration |
| Tally real-time sync | Requires Tally Gateway (ODBC connection) + Tally installed on same network |

**Why:** These features all require physical hardware, third-party paid API accounts, or government-issued certificates that cannot be created or tested without real-world setup.

### Minor Missing Features

| Feature | Reason |
|---------|--------|
| Graphical dashboard (charts/gauges) | Frappe Number Cards and Charts exist but need manual UI configuration in the Desk — cannot be auto-generated via code |
| Cheque printing layout | Requires specific printer hardware + bank-specific cheque book format — varies by bank |
| Full accounting vouchers (journal/contra) | Requires ERPNext accounting module deep integration — would need GL Entry automation across all transaction types |
| Birthday DOB field | Code checks `date_of_birth` but field not yet added to PP Customer DocType |
| Cash denomination breakdown | Document mentions cash denomination in shift settlement — not implemented as separate child table |
| Handover voucher | Document mentions closing cash handover — covered by Day Settlement but not a separate DocType |
| Vehicle-wise credit sale report | Data exists in Credit Sale Invoice but no dedicated grouped report |
| Multi-outlet/multi-station | Single station setup only — would need significant architecture changes |

---

## Roles & Permissions

| Role | Access |
|------|--------|
| System Manager | Full access to all DocTypes |
| Station Manager | Full access to operations, read compliance |
| Salesman DSM | Own shift records, create fuel sales |
| Credit Accounts Officer | Full credit management, read operations |
| Compliance Officer | Full GST/compliance, read operations |
| Recovery Officer | Credit recovery management |
| Petrol Pump Auditor | Read-only across all DocTypes |

---

## Scheduler Tasks

| Schedule | Task | Description |
|----------|------|-------------|
| Daily | Daily Stock Reconciliation | Auto-compute daily stock register per tank |
| Daily | Send Credit Reminders | SMS for overdue invoices |
| Daily | Check Stock Levels | Alert for low stock |
| Daily | Auto-block Credit Customers | Block on limit breach + SMS |
| Daily | Send Expiry Alerts | Lube expiry notifications |
| Daily | Expire Reward Points | Points older than 1 year |
| Daily | Auto-calculate Evaporation | Tank-wise evaporation loss |
| Daily | Send Daily Business Summary | SMS to manager |
| Daily | Send Birthday/Anniversary SMS | Birthday greetings |
| Weekly | Generate Credit Statements | Auto-generate weekly statements |
| Weekly | Send Weekly Credit Email | Email statements to customers |
| Monthly | Generate Monthly Reports | Business reports |
| Monthly | Calculate Late Interest | Interest on overdue invoices |
| Monthly | Auto-generate Payroll | Salary slips for all employees |
| Monthly | Auto-generate Commission | Commission for salesmen |

---

## DocType Count

| Category | Count |
|----------|-------|
| Configuration DocTypes | 8 |
| Operations DocTypes | 13 |
| Credit & Sales DocTypes | 9 |
| Finance & HR DocTypes | 11 |
| Digital Payment DocTypes | 2 |
| Compliance DocTypes | 8 |
| Notification DocTypes | 3 |
| Child Table DocTypes | 2 |
| **Total DocTypes** | **56** |
| **Total Reports** | **33** |
