app_name = "vrikshpath_erpnext"
app_title = "VrikshPath"
app_publisher = "Prashang Technologies Pvt Ltd"
app_description = "Custom ERP modules for VrikshPath product line — AutoSteer, Field Rover, Kshetra Kendra, Pump Control"
app_email = "umesh@satyanamsoft.com"
app_license = "MIT"
app_version = "0.2.0"

required_apps = ["frappe", "erpnext"]

# ── Item custom fields ────────────────────────────────────────────────────────
# Injected into the standard ERPNext Item doctype.
# These capture the electrical/hardware interface spec for every component.
custom_fields = {
    "Item": [
        {
            "fieldname": "section_hardware_spec",
            "fieldtype": "Section Break",
            "label": "Hardware Interface Spec",
            "insert_after": "description",
            "collapsible": 1,
        },
        {
            "fieldname": "voltage_rail",
            "fieldtype": "Select",
            "label": "Voltage Rail",
            "options": "\n3.3V\n5V\n12V\n24V\nDual\nVariable",
            "insert_after": "section_hardware_spec",
        },
        {
            "fieldname": "logic_level",
            "fieldtype": "Select",
            "label": "Logic Level",
            "options": "\n3.3V\n5V\nBoth (level-shifted)",
            "insert_after": "voltage_rail",
        },
        {
            "fieldname": "communication_protocol",
            "fieldtype": "Data",
            "label": "Communication Protocol(s)",
            "insert_after": "logic_level",
            "description": "e.g. I2C, SPI, UART, USB, CAN, PWM",
        },
        {
            "fieldname": "col_break_hw1",
            "fieldtype": "Column Break",
            "insert_after": "communication_protocol",
        },
        {
            "fieldname": "default_i2c_address",
            "fieldtype": "Data",
            "label": "Default I2C Address",
            "insert_after": "col_break_hw1",
            "description": "e.g. 0x4A",
        },
        {
            "fieldname": "alt_i2c_address",
            "fieldtype": "Data",
            "label": "Alternate I2C Address",
            "insert_after": "default_i2c_address",
            "description": "e.g. 0x4B when ADDR pin pulled HIGH",
        },
        {
            "fieldname": "absolute_max_voltage",
            "fieldtype": "Float",
            "label": "Absolute Max Voltage (V)",
            "insert_after": "alt_i2c_address",
            "description": "Exceeding this destroys the component",
            "precision": "2",
        },
        {
            "fieldname": "max_current_ma",
            "fieldtype": "Float",
            "label": "Max Current Draw (mA)",
            "insert_after": "absolute_max_voltage",
        },
        {
            "fieldname": "esd_sensitive",
            "fieldtype": "Check",
            "label": "ESD Sensitive",
            "insert_after": "max_current_ma",
            "description": "Handle with anti-static strap",
            "default": "0",
        },
        {
            "fieldname": "heatsink_required",
            "fieldtype": "Check",
            "label": "Heatsink Required",
            "insert_after": "esd_sensitive",
            "default": "0",
        },
        {
            "fieldname": "datasheet_url",
            "fieldtype": "Data",
            "label": "Datasheet URL",
            "insert_after": "heatsink_required",
        },
        {
            "fieldname": "pinout_image_url",
            "fieldtype": "Data",
            "label": "Pinout Image URL",
            "insert_after": "datasheet_url",
        },
        {
            "fieldname": "wiring_notes",
            "fieldtype": "Small Text",
            "label": "Critical Wiring Warning",
            "insert_after": "pinout_image_url",
            "description": "e.g. NOT 5V tolerant — destroys chip. Always check before wiring.",
        },
    ],
    # ── Work Order rework / scrap tracking ────────────────────────────────────
    # When a component burns during assembly (wrong polarity, ESD), record it so
    # inventory + COGS stay correct instead of silently grabbing another part.
    "Work Order": [
        {
            "fieldname": "section_vp_rework",
            "fieldtype": "Section Break",
            "label": "VrikshPath Rework / Scrap",
            "insert_after": "qty",
            "collapsible": 1,
        },
        {
            "fieldname": "rework_occurred",
            "fieldtype": "Check",
            "label": "Rework / Scrap Occurred",
            "insert_after": "section_vp_rework",
            "default": "0",
        },
        {
            "fieldname": "rework_component",
            "fieldtype": "Link",
            "label": "Scrapped Component",
            "options": "Item",
            "insert_after": "rework_occurred",
            "depends_on": "rework_occurred",
        },
        {
            "fieldname": "rework_qty",
            "fieldtype": "Float",
            "label": "Scrapped Qty",
            "insert_after": "rework_component",
            "depends_on": "rework_occurred",
        },
        {
            "fieldname": "rework_reason",
            "fieldtype": "Small Text",
            "label": "Rework Reason",
            "insert_after": "rework_qty",
            "depends_on": "rework_occurred",
            "description": "e.g. XL6019 burned — reverse polarity on bench",
        },
    ],
}

# ── Document lifecycle hooks ──────────────────────────────────────────────────
doc_events = {
    "VrikshPath Installation": {
        "on_submit": "vrikshpath_erpnext.vrikshpath.events.installation.on_submit",
    }
}

# ── Scheduled tasks ───────────────────────────────────────────────────────────
scheduler_events = {}

# ── Portal menu (dealer-technician web portal) ────────────────────────────────
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

# ── Roles ─────────────────────────────────────────────────────────────────────
default_roles = [
    {"role": "VrikshPath Dealer", "desk_access": 0},
    {"role": "VrikshPath Assembler", "desk_access": 1},
    {"role": "VrikshPath Manager", "desk_access": 1},
]

# ── Fixtures ──────────────────────────────────────────────────────────────────
# Committed to repo; loaded automatically on bench migrate.
fixtures = [
    {
        "dt": "Role",
        "filters": [["name", "in", ["VrikshPath Dealer", "VrikshPath Assembler", "VrikshPath Manager"]]],
    },
    {
        "dt": "Item Group",
        "filters": [
            ["name", "in", [
                "GNSS & RTK", "Steering Actuator", "Sensors", "Compute & Control",
                "Display & UI", "Power", "Connectivity", "Connectivity Services",
                "Enclosure & Wiring", "Civil & Mounting", "Finished Goods",
                "Rover Subsystems", "Stambha Subsystems", "IMU & Orientation",
            ]]
        ],
    },
    "Warehouse",
    "VrikshPath Product Line",
    "VrikshPath Installation",
    "Component Interface",
    "Tractor Compatibility",
    "Subsidy Scheme",
    "RTK Base Station",
    "Dealer Technician",
]

# ── Install / migrate hooks ───────────────────────────────────────────────────
after_install = "vrikshpath_erpnext.setup.after_install"
after_migrate = "vrikshpath_erpnext.setup.after_migrate"
