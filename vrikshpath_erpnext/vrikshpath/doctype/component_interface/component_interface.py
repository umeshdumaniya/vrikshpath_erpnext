import frappe
from frappe.model.document import Document


class ComponentInterface(Document):
    def validate(self):
        if self.from_item == self.to_item:
            frappe.throw("From Component and To Component cannot be the same item.")
        if self.damage_risk == "HIGH" and not self.damage_note:
            frappe.throw("Damage Risk is HIGH — a Damage Warning note is required.")

    def before_save(self):
        if not self.signal_name:
            self.signal_name = f"{self.from_pin} → {self.to_pin}"
