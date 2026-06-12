import frappe
from frappe.model.document import Document


class VrikshPathInstallation(Document):
    def validate(self):
        if self.cross_track_error_cm and self.cross_track_error_cm < 5:
            if not self.gnss_rtk_achieved:
                frappe.throw("Cross-track error < 5cm requires RTK fix to be confirmed.")

    def on_submit(self):
        self.status = "Active"
        self.db_set("status", "Active")
