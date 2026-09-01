# Petrol Pump Management

Complete Fuel Station / Petrol Pump Management Application for Frappe 15 & ERPNext 15.

**Developed by Bizaxl Optimisations LLP** | markcom@bizaxl.com | +91 98867 11156

---

## Features

### ⛽ Layer 1 — Admin & Station Configuration
- **Station Configuration** — Single master record for station-level settings, licence info, GST registration
- **Tank Master** — Underground/above-ground fuel tank records with capacity, fuel type, dip chart
- **Nozzle Master** — Individual dispensing outlets linked to tanks and pumps
- **Fuel Price Master** — Daily fuel rate records with effective date and revision history

### 🕒 Layer 2 — Shift, Sales & Stock Operations
- **Shift** — Shift-wise salesman assignment with nozzle allotment, opening cash, settlement
- **Meter Reading** — Opening/closing nozzle readings per shift for computing sale quantity
- **Fuel Sale** — Individual sale transactions with nozzle, quantity, rate, payment mode
- **Stock Purchase & Decantation** — Tanker unloading records with invoiced vs. received quantity
- **Daily Stock Register** — Tank-wise daily ledger with opening, purchase, sale, closing stock

### 🚗 Layer 3 — Vehicle, Credit & ANPR
- **Vehicle Master** — Vehicle-level records linking licence plates to credit customers
- **PP Customer (Credit Account)** — Credit customer profiles with limit, points, risk tracking
- **Credit Limit Ledger** — Running limit-utilisation record for real-time credit validation
- **ANPR Scan Log** — Immutable capture records for number-plate scans at nozzle bay
- **Credit Sale Invoice** — Invoices posted against credit customers from ANPR/manual sales
- **Payment Receipt** — Payments received against credit invoices

### 📊 Layer 4 — Reports & Dashboards
12 comprehensive reports:
1. Daily Sales Summary
2. Shift Settlement Report
3. Stock Variation Report
4. Credit Customer Ageing
5. ANPR Scan & Match Report
6. GST / VAT Summary
7. Employee Attendance & Payroll
8. Fuel Rate Variation Report
9. Density & Dip Variation
10. Profit & Loss Statement
11. Vehicle-wise Consumption Report
12. Swipe / Digital Settlement Report

---

## DocTypes (18)

| # | DocType | Type | Submittable |
|---|---------|------|-------------|
| 1 | Station Configuration | Single | No |
| 2 | Tank Master | Document | No |
| 3 | Tank Dip Chart | Child Table | No |
| 4 | Nozzle Master | Document | No |
| 5 | Fuel Price Master | Document | No |
| 6 | Shift | Document | Yes |
| 7 | Shift Nozzle Allotment | Child Table | No |
| 8 | Meter Reading | Document | No |
| 9 | Fuel Sale | Document | Yes |
| 10 | Stock Purchase Decantation | Document | Yes |
| 11 | Daily Stock Register | Document | No |
| 12 | Vehicle Master | Document | No |
| 13 | PP Customer | Document | No |
| 14 | Credit Limit Ledger | Document | No |
| 15 | ANPR Scan Log | Document | No |
| 16 | Credit Sale Invoice | Document | Yes |
| 17 | Payment Receipt | Document | Yes |
| 18 | Employee Master | Document | No |
| 19 | Payment Receipt Invoice | Child Table | No |

---

## Roles (7)

| Role | Access Level |
|------|-------------|
| System Manager | Full access to all modules |
| Station Manager / Dealer | Full access, approve credit, shift management |
| Salesman / DSM | Own shift and sales records |
| Credit & Accounts Officer | Credit management, invoices, payments |
| Compliance Officer (GST) | Tax filing, GST reports |
| Recovery Officer | Credit recovery, payment collection |
| Auditor / CA | Read-only access for auditing |

---

## External Integrations

1. **ANPR Camera / Number-Plate Recognition** — OCR-based vehicle plate capture
2. **SMS / WhatsApp / Email** — Transaction alerts, credit statements, reminders
3. **Payment Gateway / UPI / Swipe** — Multi-mode payment collection
4. **Tally Export Integration** — Sales, purchase, expense sync to Tally
5. **GST Portal / GSTR Filing** — Auto-aggregated GSTR-1, GSTR-3B reports
6. **Bank Reconciliation** — Daily bank-statement matching
7. **Fuel Dispenser / Pump Controller** — Direct nozzle meter-reading capture
8. **Fleet / GPS Tracking** — Vehicle location for fleet-linked credit customers
9. **Loyalty & Rewards Engine** — Reward-point accrual and redemption

---

## Installation

```bash
# From your bench directory
bench get-app https://github.com/Sudhakar1110/petrol_pump_management.git
bench --site your-site.local install-app petrol_pump_management
bench --site your-site.local migrate
bench build
bench restart
```

## Configuration

1. Go to **Petrol Pump Management > Station Configuration**
2. Set station name, dealer licence, GST number
3. Configure tanks under **Tank Master**
4. Set up nozzles under **Nozzle Master**
5. Set fuel rates under **Fuel Price Master**
6. Create employees under **Employee Master**

---

## License

MIT License - Bizaxl Optimisations LLP
