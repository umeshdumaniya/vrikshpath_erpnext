import frappe
from frappe.model.document import Document


class DealerTechnician(Document):
    def after_save(self):
        self._update_stats()

    def _update_stats(self):
        installs = frappe.db.count(
            "VrikshPath Installation",
            filters={"dealer_technician": self.name, "status": ["!=", "Scheduled"]},
        )
        self.db_set("total_installations", installs, update_modified=False)
