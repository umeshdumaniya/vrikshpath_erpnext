app_name = "vrikshpath_erpnext"
app_title = "VrikshPath"
app_publisher = "Prashang Technologies Pvt Ltd"
app_description = "Custom ERP modules for VrikshPath product line — AutoSteer, Field Rover, Kshetra Kendra, Pump Control"
app_email = "umesh@satyanamsoft.com"
app_license = "MIT"
app_version = "0.1.0"

# Module registry — one entry per product line module
# Add new products here as they are developed
required_apps = ["frappe", "erpnext"]

# Custom fields injected into standard ERPNext doctypes
# Format: {"doctype": [field_defs]}
custom_fields = {}

# Document events — hook into standard ERPNext lifecycle
doc_events = {}

# Scheduled tasks
scheduler_events = {}

# Website routes
website_route_rules = []

# Portal menu items (for dealer-technician portal)
portal_menu_items = [
    {
        "title": "My Orders",
        "route": "/vrikshpath/orders",
        "reference_doctype": "Sales Order",
        "role": "VrikshPath Dealer",
    },
    {
        "title": "Installation Requests",
        "route": "/vrikshpath/installations",
        "reference_doctype": "VrikshPath Installation",
        "role": "VrikshPath Dealer",
    },
]

# User roles created by this app
default_roles = [
    {"role": "VrikshPath Dealer", "desk_access": 0},
    {"role": "VrikshPath Assembler", "desk_access": 1},
    {"role": "VrikshPath Manager", "desk_access": 1},
]

# Fixtures — static data committed to repo and loaded on install/migrate
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["VrikshPath Dealer", "VrikshPath Assembler", "VrikshPath Manager"]]]},
    {"dt": "Item Group", "filters": [["name", "in", [
        "GNSS & RTK", "Steering Actuator", "Sensors", "Compute & Control",
        "Display & UI", "Power", "Connectivity", "Connectivity Services",
        "Enclosure & Wiring", "Civil & Mounting", "Finished Goods",
        "Rover Subsystems", "Stambha Subsystems",
    ]]]},
    "Warehouse",
    "VrikshPath Product Line",
    "VrikshPath Installation",
]

# After install hooks
after_install = "vrikshpath_erpnext.setup.after_install"
after_migrate = "vrikshpath_erpnext.setup.after_migrate"
