import frappe


def after_install():
    _create_item_groups()
    _create_warehouses()
    print("VrikshPath ERP installed successfully.")


def after_migrate():
    _create_item_groups()
    _create_warehouses()


def _create_item_groups():
    groups = [
        "GNSS & RTK", "IMU & Orientation", "Steering Actuator", "Sensors",
        "Compute & Control", "Display & UI", "Power", "Connectivity",
        "Connectivity Services", "Enclosure & Wiring", "Civil & Mounting",
        "Finished Goods", "Rover Subsystems", "Stambha Subsystems",
    ]
    for name in groups:
        if not frappe.db.exists("Item Group", name):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": name,
                "parent_item_group": "All Item Groups",
                "is_group": 0,
            }).insert(ignore_permissions=True)
    frappe.db.commit()


def _create_warehouses():
    warehouses = [
        ("Components Store - VPPL", "Stock"),
        ("Work In Progress - VPPL", "Work In Progress"),
        ("Finished Goods - VPPL", "Stock"),
        ("Quality Hold - VPPL", "Stock"),
    ]
    for name, wh_type in warehouses:
        if not frappe.db.exists("Warehouse", name):
            frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": name,
                "warehouse_type": wh_type,
            }).insert(ignore_permissions=True)
    frappe.db.commit()
