import frappe


def after_install():
    _create_warehouses()
    _create_company_defaults()
    print("VrikshPath ERP installed successfully.")


def after_migrate():
    pass


def _create_warehouses():
    site = frappe.local.site
    warehouses = [
        ("Components Store - PT", "Kholadiyad", "Stock"),
        ("Work In Progress - PT", "Kholadiyad", "Work In Progress"),
        ("Finished Goods - PT", "Kholadiyad", "Stock"),
        ("Quality Hold - PT", "Kholadiyad", "Stock"),
    ]
    for name, city, wh_type in warehouses:
        if not frappe.db.exists("Warehouse", name):
            frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": name,
                "city": city,
                "warehouse_type": wh_type,
            }).insert(ignore_permissions=True)
    frappe.db.commit()


def _create_company_defaults():
    pass
