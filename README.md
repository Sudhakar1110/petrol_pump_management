# ⛽ Petrol Pump Management — Standard Operating Procedure (SOP)
### Unified Functional Guide for Fuel Station Operations

---

> **Document Version:** 1.0  
> **Application:** Petrol Pump Management ERPNext v15  
> **Audience:** Station Manager, Salesman/DSM, Credit Accounts Officer, Compliance Officer, Recovery Officer, Auditor  
> **Support:** markcom@bizaxl.com | +91 98867 11156 | bizaxl.com

---

## 📋 Table of Contents

1. [Getting Started & Administrative Setup](#1-getting-started--administrative-setup)
   - 1.1 [Access the System](#11-access-the-system)
   - 1.2 [Initial Setup (One-Time — Admin Only)](#12-initial-setup-one-time--admin-only)
   - 1.3 [Assign User Roles](#13-assign-user-roles)
2. [Module 1 — Station Configuration & Master Data](#2-module-1--station-configuration--master-data)
   - 2.1 [SOP — Configuring Station Settings](#21-sop--configuring-station-settings)
   - 2.2 [SOP — Adding a New Tank](#22-sop--adding-a-new-tank)
   - 2.3 [SOP — Adding a New Nozzle](#23-sop--adding-a-new-nozzle)
   - 2.4 [SOP — Setting Daily Fuel Prices](#24-sop--setting-daily-fuel-prices)
   - 2.5 [SOP — Adding Employees](#25-sop--adding-employees)
3. [Module 2 — Shift & Fuel Sales Operations](#3-module-2--shift--fuel-sales-operations)
   - 3.1 [SOP — Starting a Shift](#31-sop--starting-a-shift)
   - 3.2 [SOP — Recording Fuel Sales](#32-sop--recording-fuel-sales)
   - 3.3 [SOP — Recording Meter Readings](#33-sop--recording-meter-readings)
   - 3.4 [SOP — Shift Settlement](#34-sop--shift-settlement)
   - 3.5 [SOP — Day Settlement](#35-sop--day-settlement)
4. [Module 3 — Stock & Tank Management](#4-module-3--stock--tank-management)
   - 4.1 [SOP — Receiving Fuel Delivery](#41-sop--receiving-fuel-delivery)
   - 4.2 [SOP — Recording Dip Readings](#42-sop--recording-dip-readings)
   - 4.3 [SOP — Daily Stock Register](#43-sop--daily-stock-register)
5. [Module 4 — Credit Customer Management](#5-module-4--credit-customer-management)
   - 5.1 [SOP — Onboarding a Credit Customer](#51-sop--onboarding-a-credit-customer)
   - 5.2 [SOP — Processing Credit Sales](#52-sop--processing-credit-sales)
   - 5.3 [SOP — Receiving Credit Payments](#53-sop--receiving-credit-payments)
   - 5.4 [SOP — Credit Recovery](#54-sop--credit-recovery)
6. [Module 5 — Employee & Payroll](#6-module-5--employee--payroll)
   - 6.1 [SOP — Marking Attendance](#61-sop--marking-attendance)
   - 6.2 [SOP — Processing Salary Slips](#62-sop--processing-salary-slips)
   - 6.3 [SOP — Managing Advances & Loans](#63-sop--managing-advances--loans)
7. [Module 6 — GST & Tax Compliance](#7-module-6--gst--tax-compliance)
   - 7.1 [SOP — Generating GSTR-1](#71-sop--generating-gstr-1)
   - 7.2 [SOP — Generating GSTR-3B](#72-sop--generating-gstr-3b)
   - 7.3 [SOP — TCS/TDS Statements](#73-sop--tcstds-statements)
8. [Module 7 — Digital Payments & Settlement](#8-module-7--digital-payments--settlement)
   - 8.1 [SOP — Swipe/Card Settlement](#81-sop--swipecard-settlement)
   - 8.2 [SOP — Petro-Card Transactions](#82-sop--petro-card-transactions)
9. [Module 8 — Notifications & SMS](#9-module-8--notifications--sms)
   - 9.1 [SOP — Configuring SMS Gateway](#91-sop--configuring-sms-gateway)
10. [Module 9 — Reports & Analytics](#10-module-9--reports--analytics)
11. [Combined Operating Checklists (Daily, Weekly, Monthly)](#11-combined-operating-checklists-daily-weekly-monthly)
12. [User Roles & Permissions Matrix](#12-user-roles--permissions-matrix)
13. [Missing Features & Why They Cannot Be Implemented](#13-missing-features--why-they-cannot-be-implemented)
14. [Frequently Asked Questions (FAQ)](#14-frequently-asked-questions-faq)
15. [Support & Escalation Contact Details](#15-support--escalation-contact-details)

---

## 1. Getting Started & Administrative Setup

### 1.1 Access the System

1. Open your browser and navigate to your ERP URL:  
   `https://your-domain.com`
2. Login with your secure credentials provided by the IT department.
3. On the left sidebar, click on the **PP Management** workspace.
4. You will see the **Petrol Pump Management Dashboard** with quick-access cards:
   - ⛽ Today's Fuel Sales & Revenue
   - 📊 Tank Stock Levels & Variations
   - 💰 Credit Customer Outstanding
   - ⚠️ Low Stock Alerts & Expiry Notifications
   - 👤 Employee Attendance & Shift Status

---

### 1.2 Initial Setup (One-Time — Admin Only)

> **Who does this:** System Administrator or Station Manager  
> **Purpose:** Seed the foundational master data to make the platform operational.

| Step | Action | Where |
|---|---|---|
| 1 | Configure Station Settings | PP Management → Configuration → Station Configuration |
| 2 | Setup Tanks | PP Management → Configuration → Tank Master |
| 3 | Setup Nozzles | PP Management → Configuration → Nozzle Master |
| 4 | Set Fuel Prices | PP Management → Configuration → Fuel Price Master |
| 5 | Add Employees | PP Management → Configuration → Employee Master |
| 6 | Configure SMS Gateway | PP Management → Configuration → PP Notification Settings |
| 7 | Seed Demo Data | `bench --site your-site execute petrol_pump_management.setup.after_install` |

---

### 1.3 Assign User Roles

> **Who does this:** Administrator or HR Manager

Go to **ERPNext → Users**, select the employee, and assign the appropriate roles:

| Role | Responsibilities |
|---|---|
| **Station Manager** | Full access to all operations, approve settlements, manage staff |
| **Salesman DSM** | Create fuel sales, record meter readings, manage own shift |
| **Credit Accounts Officer** | Manage credit customers, invoices, payments, recovery |
| **Compliance Officer** | GST filing, TCS/TDS statements, regulatory reports |
| **Recovery Officer** | Credit recovery tracking, follow-ups, escalation |
| **Petrol Pump Auditor** | Read-only access to all records for audit purposes |
| **System Manager** | Full system access, user management, configuration |

---

## 2. Module 1 — Station Configuration & Master Data

> **Purpose:** Set up the foundational configuration — station details, tanks, nozzles, fuel pricing, and employee records.

---

### 2.1 SOP — Configuring Station Settings

**Who:** Station Manager / Admin  
**When:** First-time setup or when station details change

1. Navigate to **PP Management → Configuration → Station Configuration**.
2. Click **+ New** (or edit the existing "Main Station" record).
3. Fill in the required fields:
   - **Station Name:** Legal/trade name of the fuel station
   - **Dealer Licence No:** Oil-company dealership licence number
   - **GST Number:** GSTIN registered for the station
   - **Default Fuel Unit:** Select `Litre`
   - **Financial Year Start:** Select `April` (Indian FY)
   - **Default Currency:** `INR`
   - **Contact Email:** Email for statements and regulatory correspondence
4. Click **Save**.

✅ **Expected Result:** Station profile is configured. All reports and GST filings will use these details.

---

### 2.2 SOP — Adding a New Tank

**Who:** Station Manager  
**When:** When a new underground/above-ground tank is installed

1. Navigate to **PP Management → Configuration → Tank Master**.
2. Click **+ New**.
3. Enter the **Tank Number** (e.g., `T1`, `T2`).
4. Select the **Fuel Type** (`Petrol`, `Diesel`, or `Premium`).
5. Enter the **Capacity (Litres)** (e.g., `10000`).
6. Set the **Current Stock (Litres)** — enter the current dip reading.
7. Set the **Safe Stock Level** (minimum before reorder alert fires, e.g., `2000`).
8. Tick **Is Active**.
9. Click **Save**.

✅ **Expected Result:** Tank is registered. Daily stock register and evaporation tracking will begin.

---

### 2.3 SOP — Adding a New Nozzle

**Who:** Station Manager  
**When:** When a new dispensing nozzle is installed or reassigned

1. Navigate to **PP Management → Configuration → Nozzle Master**.
2. Click **+ New**.
3. Enter the **Nozzle Number** (e.g., `P1-T1-1` = Pump 1 / Tank 1 / Nozzle 1).
4. Select the **Source Tank** (link to Tank Master).
5. Enter the **Pump Number** (physical dispenser unit).
6. Enter the **Current Meter Reading** (initial reading).
7. Select the **Fuel Price** (link to Fuel Price Master).
8. Set **Nozzle Status** to `Open`.
9. Tick **Is Active**.
10. Click **Save**.

✅ **Expected Result:** Nozzle is ready for shift allotment and fuel sales.

---

### 2.4 SOP — Setting Daily Fuel Prices

**Who:** Station Manager  
**When:** Daily, when oil companies announce price revisions

1. Navigate to **PP Management → Configuration → Fuel Price Master**.
2. Click **+ New**.
3. Select the **Fuel Type** (`Petrol`, `Diesel`, or `Premium`).
4. Set **Effective From** to the date/time the new rate takes effect.
5. Enter the **Rate Per Litre** (inclusive of taxes).
6. The **Previous Rate** auto-fills from the last active record.
7. Tick **Is Active** (only one active rate per fuel type at a time).
8. Click **Save**.

> [!TIP]
> The system maintains a complete revision history. Old rates are automatically deactivated when a new rate is activated.

---

### 2.5 SOP — Adding Employees

**Who:** Station Manager / HR  
**When:** When a new employee joins the station

1. Navigate to **PP Management → Configuration → Employee Master**.
2. Click **+ New**.
3. Enter the **Employee Name**.
4. Select the **Role** (`Salesman`, `DSM`, `Manager`, `Accountant`, or `Security`).
5. Enter the **Mobile Number**.
6. Select the **Salary Type** (`Fixed`, `Duty-based`, or `Commission`).
7. Enter the **Joining Date**.
8. Tick **Is Active**.
9. Click **Save**.

✅ **Expected Result:** Employee can be assigned to shifts and included in payroll.

---

## 3. Module 2 — Shift & Fuel Sales Operations

> **Purpose:** Manage the daily operational loop — shift allotment, fuel dispensing, meter readings, and settlement.

---

### 3.1 SOP — Starting a Shift

**Who:** Station Manager  
**When:** At the beginning of each shift (morning/afternoon/night)

1. Navigate to **PP Management → Operations → Shift**.
2. Click **+ New**.
3. Set the **Shift Date**.
4. Select the **Salesman** (Employee Master).
5. In the **Nozzles Allotted** child table, add the nozzles assigned to this salesman.
6. Enter the **Opening Cash** handed to the salesman.
7. Set **Status** to `Open`.
8. Click **Save** and **Submit**.

✅ **Expected Result:** Shift is active. Salesman can now record fuel sales against this shift.

---

### 3.2 SOP — Recording Fuel Sales

**Who:** Salesman / DSM  
**When:** Throughout the shift, for each fuel dispensing transaction

1. Navigate to **PP Management → Operations → Fuel Sale**.
2. Click **+ New**.
3. Select the **Shift** (current active shift).
4. Select the **Nozzle** used for dispensing.
5. The **Sale Date**, **Rate**, and **Amount** auto-calculate.
6. Enter the **Quantity (Litres)** dispensed.
7. The **Amount** auto-calculates: `Quantity × Rate`.
8. Select the **Payment Mode** (`Cash`, `Credit`, `Card`, `UPI`, or `Petro-card`).
9. If credit sale, select the **Customer** (PP Customer).
10. Click **Save** and **Submit**.

> [!IMPORTANT]
> For credit sales, the system auto-creates a Credit Sale Invoice and checks the customer's credit limit. If the limit is exceeded, the sale is blocked.

✅ **Expected Result:** Sale is recorded. SMS receipt sent to customer (if configured). Reward points awarded (1 point per ₹100).

---

### 3.3 SOP — Recording Meter Readings

**Who:** Salesman / DSM  
**When:** At the start and end of each shift

1. Navigate to **PP Management → Operations → Meter Reading**.
2. Click **+ New**.
3. Select the **Nozzle**.
4. Select the **Shift**.
5. Enter the **Opening Reading** (carried forward from previous shift's closing).
6. Enter the **Closing Reading** (current meter value).
7. Enter **Testing Qty** (litres drawn for calibration, if any).
8. The **Sale Qty** auto-calculates: `Closing - Opening - Testing Qty`.
9. Click **Save**.

✅ **Expected Result:** Meter reading recorded. Sale quantity is verified against meter readings.

---

### 3.4 SOP — Shift Settlement

**Who:** Station Manager  
**When:** At the end of each shift

1. Open the active **Shift** record.
2. Review the collected cash, card/UPI settlements, and credit sales.
3. Enter the **Closing Cash** counted.
4. The system calculates: `Expected = Opening Cash + Total Sale Amount`.
5. Any **Shortage** or **Excess** is flagged.
6. Change **Status** to `Settled`.
7. Click **Submit**.

> [!CAUTION]
> Shortages must be investigated. The Employee Shortage Report tracks shortages per employee across date ranges.

✅ **Expected Result:** Shift is closed and locked. Cash is handed over to next shift or manager.

---

### 3.5 SOP — Day Settlement

**Who:** Station Manager  
**When:** At the end of each business day

1. Navigate to **PP Management → Operations → Day Settlement**.
2. Click **+ New**.
3. Enter the **Settlement Date**.
4. The system pulls in all shift data for the day.
5. Review **Total Sales**, **Cash Collected**, **Card/UPI Amount**, **Credit Amount**.
6. Verify **Bank Deposits** logged for the day.
7. Check that all totals reconcile.
8. Change **Status** to `Closed`.
9. Click **Submit**.

✅ **Expected Result:** Business day is closed. PP Day Book report is updated.

---

## 4. Module 3 — Stock & Tank Management

> **Purpose:** Track tank-wise fuel stock from delivery through daily sales to closing stock with variation analysis.

---

### 4.1 SOP — Receiving Fuel Delivery

**Who:** Station Manager / Store Keeper  
**When:** When a tanker (TT) arrives with fuel

1. Navigate to **PP Management → Operations → Stock Purchase Decantation**.
2. Click **+ New**.
3. Enter the **Tanker Number** (registration number).
4. Select the **Tank** (destination tank).
5. Enter the **Invoiced Quantity** (per supplier invoice).
6. Enter the **Received Quantity** (dip-verified quantity actually received).
7. Enter the **Density** recorded at time of unloading.
8. The **Variation %** auto-calculates: `(Invoiced - Received) / Invoiced × 100`.
9. Set the **Decantation DateTime**.
10. Click **Save** and **Submit**.

> [!TIP]
> If variation exceeds threshold, the system flags it for investigation. Use the Stock Variation Report for detailed analysis.

---

### 4.2 SOP — Recording Dip Readings

**Who:** Salesman / Station Manager  
**When:** Daily, at the start and end of business

1. Navigate to **PP Management → Configuration → Tank Dip Chart**.
2. Record the **Dip Reading (cm)** for each tank.
3. The **Stock Volume (Litres)** auto-maps from the dip chart.
4. Compare with the calculated stock in the Daily Stock Register.

---

### 4.3 SOP — Daily Stock Register

**Who:** System (auto-generated) / Station Manager (manual)  
**When:** Daily

1. Navigate to **PP Management → Operations → Daily Stock Register**.
2. The system auto-generates entries for each active tank:
   - **Opening Stock** (previous day's closing)
   - **Purchase Qty** (from Stock Purchase Decantation)
   - **Sale Qty** (from Fuel Sales linked to tank's nozzles)
   - **Closing Stock** = Opening + Purchase - Sale
   - **Variation** = Expected Closing - Actual Dip Reading
3. Review and verify the entries.
4. Click **Save**.

> [!CAUTION]
> Variations above 0.5% are flagged as "Above Threshold" and above 2% as "Critical". Investigate immediately.

---

## 5. Module 4 — Credit Customer Management

> **Purpose:** Manage credit customers — onboarding, credit sales, payments, limit tracking, and recovery.

---

### 5.1 SOP — Onboarding a Credit Customer

**Who:** Credit Accounts Officer  
**When:** When a new customer requests a credit account

1. Navigate to **PP Management → Credit & Sales → PP Customer**.
2. Click **+ New**.
3. Select the **Customer Type** (`Individual`, `Proprietary`, `Fleet`, or `Corporate`).
4. Enter the **Full Name**.
5. Enter the **Mobile Number** (used for SMS notifications).
6. Enter the **Credit Limit** (maximum outstanding permitted).
7. Select the **Risk Category** (`Low`, `Medium`, or `High`).
8. Enter **GST Number** and **Address** (if GST-compliant billing needed).
9. Click **Save**.

✅ **Expected Result:** Customer is registered. Credit limit is set. SMS notifications will be sent for sales and payments.

---

### 5.2 SOP — Processing Credit Sales

**Who:** Salesman / DSM  
**When:** When a credit customer purchases fuel

1. Record a **Fuel Sale** as normal (see Section 3.2).
2. Select **Payment Mode** = `Credit`.
3. Select the **Customer** (PP Customer).
4. The system auto-checks: `Available Credit = Limit - Outstanding`.
5. If **Available Credit > Sale Amount** → Sale proceeds.
6. If **Available Credit < Sale Amount** → Sale is **BLOCKED**.
7. A **Credit Sale Invoice** is auto-generated with `Due Date` = Sale Date + 30 days.
8. SMS receipt is sent to the customer.

> [!IMPORTANT]
> Customers exceeding their credit limit are auto-blocked. Only the Station Manager can override with manager approval.

---

### 5.3 SOP — Receiving Credit Payments

**Who:** Credit Accounts Officer  
**When:** When a customer makes a payment against outstanding dues

1. Navigate to **PP Management → Credit & Sales → Payment Receipt**.
2. Click **+ New**.
3. Select the **Customer**.
4. The **Outstanding Amount** auto-fills.
5. Enter the **Amount Received**.
6. Select the **Mode** (`Cash`, `Bank Transfer`, `Swipe`, `UPI`, or `Cheque`).
7. Enter the **Reference Number** (bank UTR / cheque number).
8. Click **Save** and **Submit**.

✅ **Expected Result:** Payment is recorded. Credit Limit Ledger is updated. SMS confirmation sent to customer. If outstanding clears, customer is unblocked.

---

### 5.4 SOP — Credit Recovery

**Who:** Recovery Officer  
**When:** When follow-up is needed for overdue payments

1. Navigate to **PP Management → Credit & Sales → Credit Recovery Entry**.
2. Click **+ New**.
3. Select the **Customer**.
4. The **Outstanding Amount** auto-fills.
5. Select the **Recovery Type** (`Call`, `Visit`, `SMS`, `Letter`, or `Legal Notice`).
6. Enter the **Amount Collected** (if any).
7. Enter any **Discount / Waiver** applied.
8. Select the **Collection Mode**.
9. Set **Next Follow-up Date** if needed.
10. Click **Save** and **Submit**.

> [!TIP]
> The system auto-calculates `Balance After = Outstanding - Collected - Discount`. Discounts are applied to the oldest unpaid invoices first.

---

## 6. Module 5 — Employee & Payroll

> **Purpose:** Track attendance, process salary slips, manage advances, and calculate commissions.

---

### 6.1 SOP — Marking Attendance

**Who:** Station Manager  
**When:** Daily, at the start of each shift

1. Navigate to **PP Management → Finance & HR → Attendance Register**.
2. Click **+ New**.
3. Set the **Date** and **Shift**.
4. For each employee, set the **Attendance Status** (`Present`, `Absent`, `Half Day`, or `Leave`).
5. Set the **Salary Type** (`Paid` or `Unpaid`).
6. Click **Save** and **Submit**.

---

### 6.2 SOP — Processing Salary Slips

**Who:** System (auto-generated monthly) / Station Manager  
**When:** Monthly

1. Navigate to **PP Management → Finance & HR → Salary Slip Entry**.
2. The system auto-generates salary slips for all active employees.
3. Review each slip:
   - **Basic Salary** (from Employee Master)
   - **Overtime Pay** (auto-calculated from Overtime Log)
   - **Commission Earned** (from Commission Payment)
   - **Deductions** (Advance, Loan, PF, ESI, Professional Tax)
   - **Net Salary** = Total Earnings - Total Deductions
4. Click **Submit** to approve.

---

### 6.3 SOP — Managing Advances & Loans

**Who:** Station Manager  
**When:** When an employee requests a salary advance

1. Navigate to **PP Management → Finance & HR → Advance Amount**.
2. Click **+ New**.
3. Select the **Employee**.
4. Enter the **Advance Amount**.
5. Enter the **Date** of disbursement.
6. Select the **Mode** (`Cash` or `Bank`).
7. Click **Save**.

> [!TIP]
> Advances are auto-deducted from the employee's next salary slip. The system tracks pending advances in the Salary Slip Entry.

---

## 7. Module 6 — GST & Tax Compliance

> **Purpose:** Generate GST filing-ready reports and manage TCS/TDS compliance.

---

### 7.1 SOP — Generating GSTR-1

**Who:** Compliance Officer  
**When:** Monthly, before the 10th of the next month

1. Navigate to **PP Management → Compliance & GST → GSTR-1 Filing**.
2. Click **+ New**.
3. Enter the **Filing Period** (e.g., `08-2026` for August 2026).
4. Set the **Filing Date**.
5. The system auto-aggregates all credit sales for the period.
6. Review the **B2B Invoices** child table.
7. Click **Submit** to generate the **GSTR-1 XML**.
8. Download the XML for upload to the GST portal.

---

### 7.2 SOP — Generating GSTR-3B

**Who:** Compliance Officer  
**When:** Monthly, before the 20th of the next month

1. Navigate to **PP Management → Compliance & GST → GSTR-3B Filing**.
2. Click **+ New**.
3. Enter the **Filing Period**.
4. The system auto-calculates:
   - **Total Outward Supplies** (quantity)
   - **Total Taxable Value**
   - **CGST** (6%) and **SGST** (6%)
   - **Net Tax Payable** = Tax - ITC
5. Click **Submit** to generate the **GSTR-3B XML**.

---

### 7.3 SOP — TCS/TDS Statements

**Who:** Compliance Officer  
**When:** Monthly

1. Navigate to **PP Management → Compliance & GST → TCS Statement** or **TDS Statement**.
2. Click **+ New**.
3. Enter the party details, gross amount, and tax rate.
4. The **Tax Amount** and **Net Amount** auto-calculate.
5. Click **Save** and **Submit**.

---

## 8. Module 7 — Digital Payments & Settlement

> **Purpose:** Track card/UPI/e-wallet transactions and reconcile POS machine settlements.

---

### 8.1 SOP — Swipe/Card Settlement

**Who:** Station Manager  
**When:** Daily, at the end of business

1. Navigate to **PP Management → Digital Payments → Swipe Settlement**.
2. Click **+ New**.
3. Enter the **POS Machine ID**.
4. Select the **Payment Mode** (`Card`, `UPI`, `E-Wallet`, or `Petro-card`).
5. Enter the **Total Sale Amount** (expected from machine).
6. Enter the **Total Collected** (actual amount received).
7. The **Difference** auto-calculates.
8. Set **Status** (`Pending`, `Settled`, or `Disputed`).
9. Click **Save** and **Submit**.

---

### 8.2 SOP — Petro-Card Transactions

**Who:** Salesman / DSM  
**When:** When a petro-card payment is received

1. Navigate to **PP Management → Digital Payments → Petro Card Transaction**.
2. Click **+ New**.
3. Enter the **Card Number** and **Card Holder Name**.
4. Enter the **Amount** and select the **Transaction Type** (`Fuel Purchase` or `Balance Top-up`).
5. Click **Save**.

---

## 9. Module 8 — Notifications & SMS

> **Purpose:** Configure SMS/Email gateways and manage notification templates.

---

### 9.1 SOP — Configuring SMS Gateway

**Who:** System Manager  
**When:** First-time setup

1. Navigate to **PP Management → Configuration → PP Notification Settings**.
2. Tick **Enable SMS**.
3. Select the **SMS Gateway** (`Twilio`, `MSG91`, or `Custom HTTP API`).
4. Enter the gateway credentials (API key, account SID, etc.).
5. Review the **Message Templates**:
   - **SMS: Credit Sale** — sent on credit fuel purchase
   - **SMS: Payment Receipt** — sent on payment received
   - **SMS: Limit Breach** — sent when credit limit exceeded
   - **SMS: Advance Reminder** — sent for advance deductions
6. Click **Save**.

> [!TIP]
> Use `{customer}`, `{amount}`, `{station}` as placeholders in templates. They auto-fill from the transaction data.

---

## 10. Module 9 — Reports & Analytics

A complete set of 33 reports covering all operational areas:

| Report | Module | Focus Metrics | Primary Filters |
|---|---|---|---|
| **Daily Sales Summary** | Sales | Shift-wise, nozzle-wise, payment-mode-wise sales | Date Range |
| **Shift Settlement Report** | Operations | Cash collected vs expected, shortages | Date, Employee |
| **Stock Variation Report** | Stock | Tank-wise dip vs meter-sale variance | Date Range, Tank |
| **Credit Customer Ageing** | Credit | Outstanding dues by age bucket | Customer, Date |
| **Nozzle Wise Sale** | Sales | Per-nozzle sales with payment split | Date Range, Nozzle |
| **Meter Dip Variation** | Stock | Meter sale vs dip reading comparison | Date Range, Tank |
| **Employee Shortage Report** | HR | Per-employee cash shortage | Date Range, Employee |
| **Monthly Shortage Report** | HR | Monthly aggregated shortage | Month, Employee |
| **Tank Valuation Report** | Stock | Stock value & utilization % | Tank |
| **Machine Wise Transaction** | Digital | POS machine-wise breakdown | Date Range |
| **GST VAT Summary** | Compliance | GST summary with CGST/SGST | Date Range |
| **GSTR-1 Summary** | Compliance | B2B credit sales for GST filing | Period |
| **GSTR-3B Summary** | Compliance | Monthly GST return summary | Period |
| **TCS TDS Report** | Compliance | Combined TCS/TDS statement | Date Range |
| **HSN Wise Summary** | Compliance | HSN code-wise product summary | Date Range |
| **Employee Commission Report** | HR | Employee-wise sales & commission | Period |
| **Payroll Summary** | HR | Employee-wise salary details | Period |
| **Cash Flow Report** | Finance | Daily cash inflows/outflows | Date |
| **PP Day Book** | Finance | All transactions for a date | Date |
| **Profit Loss Statement** | Finance | Trading account, expenses, margin | Date Range |
| **Expense Summary** | Finance | Expense breakdown | Date Range |
| **Bank Deposit Report** | Finance | Deposit history | Date Range |
| **Bank Reconciliation Report** | Finance | Reconciliation status | Date Range |
| **Credit Customer Ageing** | Credit | Outstanding dues by age | Customer |
| **Vehicle Wise Consumption** | Credit | Fuel consumption per vehicle | Vehicle, Date |
| **Employee Attendance Payroll** | HR | Attendance, salary, commission | Month |
| **Fuel Rate Variation Report** | Config | Historical rate changes | Date Range |
| **Density Dip Variation** | Stock | Tank-wise density vs stock | Date Range |
| **ANPR Scan Report** | ANPR | Scan stats, auto-matched vs manual | Date Range |
| **Swipe Digital Settlement** | Digital | Card/UPI/e-wallet reconciliation | Date Range |
| **Sales Officer Inspection** | Operations | Inspection records | Date Range |
| **Tally Export Report** | Compliance | Export history | Date Range |
| **Report Export** | System | CSV/Excel export | Report Type |

---

## 11. Combined Operating Checklists (Daily, Weekly, Monthly)

### 11.1 Daily Checklist (Morning Dispatch)

| Task | Category | Responsible |
|---|---|---|
| ☐ Set today's fuel prices | Configuration | Station Manager |
| ☐ Start shift and allot nozzles | Operations | Station Manager |
| ☐ Record opening meter readings | Operations | Salesman |
| ☐ Verify tank stock levels (dip check) | Stock | Salesman |
| ☐ Process fuel sales throughout the shift | Sales | Salesman |
| ☐ Record closing meter readings | Operations | Salesman |
| ☐ Perform shift settlement | Operations | Station Manager |
| ☐ Log bank deposits for the day | Finance | Station Manager |
| ☐ Perform day settlement | Operations | Station Manager |
| ☐ Run swipe/card machine settlement | Digital | Station Manager |

### 11.2 Weekly Operational Review

| Task | Category | Responsible |
|---|---|---|
| ☐ Review credit customer outstanding balances | Credit | Credit Accounts Officer |
| ☐ Send credit reminders for overdue invoices | Credit | System (auto) |
| ☐ Generate credit statements for all customers | Credit | System (auto) |
| ☐ Review employee shortage trends | HR | Station Manager |
| ☐ Check stock variations and evaporation losses | Stock | Station Manager |
| ☐ Review ANPR scan logs and match rates | ANPR | Station Manager |

### 11.3 Monthly Regulatory & Compliance Audit

| Task | Category | Responsible |
|---|---|---|
| ☐ Generate and file GSTR-1 | Compliance | Compliance Officer |
| ☐ Generate and file GSTR-3B | Compliance | Compliance Officer |
| ☐ Process TCS/TDS statements | Compliance | Compliance Officer |
| ☐ Generate salary slips for all employees | HR | System (auto) |
| ☐ Calculate and pay commissions | HR | System (auto) |
| ☐ Review profit & loss statement | Finance | Station Manager |
| ☐ Reconcile bank statements | Finance | Credit Accounts Officer |
| ☐ Review all safety & inspection reports | Safety | Station Manager |

---

## 12. User Roles & Permissions Matrix

| Feature / DocType | Station Manager | Salesman DSM | Credit Accounts Officer | Compliance Officer | Recovery Officer | Auditor |
|---|---|---|---|---|---|---|
| **Station Configuration** | ✅ | 👁 | ❌ | ❌ | ❌ | 👁 |
| **Tank Master** | ✅ | 👁 | ❌ | ❌ | ❌ | 👁 |
| **Nozzle Master** | ✅ | 👁 | ❌ | ❌ | ❌ | 👁 |
| **Fuel Price Master** | ✅ | 👁 | ❌ | ❌ | ❌ | 👁 |
| **Employee Master** | ✅ | ❌ | ❌ | ❌ | ❌ | 👁 |
| **Shift** | ✅ | ✅ (own) | ❌ | ❌ | ❌ | 👁 |
| **Fuel Sale** | ✅ | ✅ (create) | ❌ | ❌ | ❌ | 👁 |
| **Meter Reading** | ✅ | ✅ | ❌ | ❌ | ❌ | 👁 |
| **Daily Stock Register** | ✅ | 👁 | ❌ | ❌ | ❌ | 👁 |
| **PP Customer** | ✅ | 👁 | ✅ | ❌ | 👁 | 👁 |
| **Credit Sale Invoice** | ✅ | ❌ | ✅ | ❌ | 👁 | 👁 |
| **Payment Receipt** | ✅ | ❌ | ✅ | ❌ | 👁 | 👁 |
| **Credit Recovery Entry** | 👁 | ❌ | 👁 | ❌ | ✅ | 👁 |
| **Expense Entry** | ✅ | ❌ | ✅ | ❌ | ❌ | 👁 |
| **Salary Slip Entry** | ✅ | ❌ | ❌ | ❌ | ❌ | 👁 |
| **GSTR-1 Filing** | 👁 | ❌ | ❌ | ✅ | ❌ | 👁 |
| **GSTR-3B Filing** | 👁 | ❌ | ❌ | ✅ | ❌ | 👁 |
| **Swipe Settlement** | ✅ | ❌ | 👁 | ❌ | ❌ | 👁 |
| **SMS Log** | 👁 | ❌ | 👁 | ❌ | ❌ | 👁 |

*Legend: ✅ Full Write/Submit | 👁 Read-Only | ❌ No Access*

---

## 13. Missing Features & Why They Cannot Be Implemented

### Mobile Apps

| Feature | Reason |
|---|---|
| Dealer / Owner mobile app | Requires React Native/Flutter development — not part of Frappe web framework |
| Manager-level mobile app | Needs native mobile app codebase, app store deployment |
| Salesman / DSM mobile app | Needs native mobile app with offline support |
| Credit-customer self-service app | Full mobile app needs separate development |

### External Integrations

| Feature | Reason |
|---|---|
| ANPR Camera / OCR | Requires physical camera hardware at nozzle bay + third-party OCR API |
| Fuel Dispenser / Pump Controller | Requires hardware integration with dispenser brands (Gilbarco, Tokheim) |
| Fleet / GPS Tracking | Requires GPS hardware installed in vehicles + third-party API |
| WhatsApp integration | Requires WhatsApp Business API account + Meta verification |
| Payment Gateway (Razorpay/PhonePe) | Requires payment provider merchant account + API keys |
| Bank auto-import (real API) | Banks don't offer open APIs — CSV upload already works |
| GST portal auto-submit | Requires Digital Signature Certificate (DSC) + GSTN registration |
| Tally real-time sync | Requires Tally Gateway (ODBC) + Tally installed on same network |

### Minor Missing

| Feature | Reason |
|---|---|
| Graphical dashboard | Frappe Number Cards/Charts exist but need manual UI configuration |
| Cheque printing layout | Requires bank-specific cheque format + printer hardware |
| Full accounting vouchers | Needs deep ERPNext accounting module integration |
| Multi-outlet support | Single station only — needs architecture changes |

---

## 14. Frequently Asked Questions (FAQ)

#### Q1: How does the system prevent credit sales beyond the limit?
**A:** When a Fuel Sale is submitted with Payment Mode = `Credit`, the system checks `Available Credit = Credit Limit - Outstanding`. If the sale amount exceeds available credit, the submission fails with a validation error. The customer is also auto-blocked for future sales.

#### Q2: How are fuel prices updated across all nozzles?
**A:** When a new Fuel Price Master record is created and marked `Is Active`, all nozzles linked to that fuel type automatically use the new rate for subsequent sales. Old rates are deactivated.

#### Q3: What happens when stock variation exceeds threshold?
**A:** The Evaporation Loss DocType flags variations above 0.5% as "Above Threshold" and above 2% as "Critical". Daily tasks send SMS alerts to the station manager for investigation.

#### Q4: How is GST filing data generated?
**A:** The GSTR-1 Filing DocType auto-aggregates all credit sales for the period, calculates CGST/SGST at 6% each, and generates a GSTN-compatible XML file for upload to the GST portal.

#### Q5: How are reward points earned and redeemed?
**A:** Points are earned at 1 point per ₹100 spent (auto-credited on Fuel Sale submit). Points can be redeemed during a sale by entering `Redeem Points` on the Fuel Sale form. Points expire after 1 year (daily task).

#### Q6: Can I override a blocked credit customer?
**A:** Only the Station Manager can unblock a customer by toggling the `Is Blocked` flag on the PP Customer record. This requires manager approval.

---

## 15. Support & Escalation Contact Details

For technical issues, login resets, or system bugs:

📧 **Email:** markcom@bizaxl.com  
📞 **Phone:** +91 98867 11156  
🌐 **Website:** bizaxl.com  
💬 **Support:** Contact your Station Manager or System Administrator

---
*End of Petrol Pump Management — Standard Operating Procedure (SOP)*
