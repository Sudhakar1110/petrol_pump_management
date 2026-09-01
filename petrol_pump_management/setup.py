import frappe


def after_install():
    """Create roles and default station configuration after app installation."""
    create_custom_roles()
    create_default_permissions()
    frappe.db.commit()


def create_custom_roles():
    """Create custom roles for petrol pump management."""
    roles = [
        {
            "role_name": "Station Manager",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Station Manager / Dealer - Full access to all modules",
        },
        {
            "role_name": "Salesman DSM",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Salesman / Direct Sales Man - Access to shift and sales operations",
        },
        {
            "role_name": "Credit Accounts Officer",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Credit & Accounts Officer - Credit management and accounting",
        },
        {
            "role_name": "Compliance Officer",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Compliance Officer (GST) - Tax filing and regulatory compliance",
        },
        {
            "role_name": "Recovery Officer",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Recovery Officer - Credit recovery and dues collection",
        },
        {
            "role_name": "Petrol Pump Auditor",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Auditor / CA - Read-only access for auditing purposes",
        },
    ]

    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)


def create_default_permissions():
    """Create default role permissions for DocTypes."""
    permissions = [
        # Station Configuration
        {"role": "System Manager", "doctype": "Station Configuration", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Station Manager", "doctype": "Station Configuration", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Petrol Pump Auditor", "doctype": "Station Configuration", "permlevel": 0,
         "read": 1},

        # Tank Master
        {"role": "System Manager", "doctype": "Tank Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Station Manager", "doctype": "Tank Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Salesman DSM", "doctype": "Tank Master", "permlevel": 0,
         "read": 1},
        {"role": "Credit Accounts Officer", "doctype": "Tank Master", "permlevel": 0,
         "read": 1},

        # Nozzle Master
        {"role": "System Manager", "doctype": "Nozzle Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Station Manager", "doctype": "Nozzle Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Fuel Price Master
        {"role": "System Manager", "doctype": "Fuel Price Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Station Manager", "doctype": "Fuel Price Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Shift
        {"role": "Station Manager", "doctype": "Shift", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
        {"role": "Salesman DSM", "doctype": "Shift", "permlevel": 0,
         "read": 1, "write": 1, "create": 1},

        # Meter Reading
        {"role": "Salesman DSM", "doctype": "Meter Reading", "permlevel": 0,
         "read": 1, "write": 1, "create": 1},
        {"role": "Station Manager", "doctype": "Meter Reading", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Fuel Sale
        {"role": "Salesman DSM", "doctype": "Fuel Sale", "permlevel": 0,
         "read": 1, "write": 1, "create": 1},
        {"role": "Station Manager", "doctype": "Fuel Sale", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Credit Accounts Officer", "doctype": "Fuel Sale", "permlevel": 0,
         "read": 1},

        # Stock Purchase & Decantation
        {"role": "Station Manager", "doctype": "Stock Purchase & Decantation", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Daily Stock Register
        {"role": "Station Manager", "doctype": "Daily Stock Register", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "System Manager", "doctype": "Daily Stock Register", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Vehicle Master
        {"role": "Station Manager", "doctype": "Vehicle Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Credit Accounts Officer", "doctype": "Vehicle Master", "permlevel": 0,
         "read": 1},

        # Customer (Credit Account)
        {"role": "Credit Accounts Officer", "doctype": "PP Customer", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Recovery Officer", "doctype": "PP Customer", "permlevel": 0,
         "read": 1, "write": 1},
        {"role": "Station Manager", "doctype": "PP Customer", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Credit Limit Ledger
        {"role": "Credit Accounts Officer", "doctype": "Credit Limit Ledger", "permlevel": 0,
         "read": 1, "write": 1, "create": 1},
        {"role": "Recovery Officer", "doctype": "Credit Limit Ledger", "permlevel": 0,
         "read": 1, "write": 1},

        # ANPR Scan Log
        {"role": "System Manager", "doctype": "ANPR Scan Log", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Station Manager", "doctype": "ANPR Scan Log", "permlevel": 0,
         "read": 1},
        {"role": "Credit Accounts Officer", "doctype": "ANPR Scan Log", "permlevel": 0,
         "read": 1},

        # Credit Sale Invoice
        {"role": "Credit Accounts Officer", "doctype": "Credit Sale Invoice", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1},
        {"role": "Station Manager", "doctype": "Credit Sale Invoice", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1},
        {"role": "Recovery Officer", "doctype": "Credit Sale Invoice", "permlevel": 0,
         "read": 1, "write": 1},

        # Payment Receipt
        {"role": "Credit Accounts Officer", "doctype": "Payment Receipt", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "submit": 1},
        {"role": "Recovery Officer", "doctype": "Payment Receipt", "permlevel": 0,
         "read": 1, "write": 1, "create": 1},

        # Employee Master
        {"role": "Station Manager", "doctype": "Employee Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Salesman DSM", "doctype": "Employee Master", "permlevel": 0,
         "read": 1},

        # Expense Entry (Layer 4)
        {"role": "Station Manager", "doctype": "Expense Entry", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
        {"role": "System Manager", "doctype": "Expense Entry", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
        {"role": "Petrol Pump Auditor", "doctype": "Expense Entry", "permlevel": 0,
         "read": 1},

        # Attendance Register (Layer 4)
        {"role": "Station Manager", "doctype": "Attendance Register", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "Salesman DSM", "doctype": "Attendance Register", "permlevel": 0,
         "read": 1},

        # Advance Amount
        {"role": "Station Manager", "doctype": "Advance Amount", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "System Manager", "doctype": "Advance Amount", "permlevel": 0,
         "read": 1, "write": 1, "create": 1},

        # Bank Deposit
        {"role": "Station Manager", "doctype": "Bank Deposit", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1},
        {"role": "System Manager", "doctype": "Bank Deposit", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "submit": 1},

        # Day Settlement
        {"role": "Station Manager", "doctype": "Day Settlement", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1},
        {"role": "System Manager", "doctype": "Day Settlement", "permlevel": 0,
         "read": 1, "write": 1, "submit": 1},

        # PP Supplier Master
        {"role": "Station Manager", "doctype": "PP Supplier Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},
        {"role": "System Manager", "doctype": "PP Supplier Master", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1},

        # Trip Voucher
        {"role": "Station Manager", "doctype": "Trip Voucher", "permlevel": 0,
         "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
    ]

    for perm in permissions:
        if not frappe.db.exists("Custom DocPerm", {
            "role": perm["role"],
            "parent": perm["doctype"],
            "permlevel": perm["permlevel"],
        }):
            pass  # Permissions handled via DocType JSON
