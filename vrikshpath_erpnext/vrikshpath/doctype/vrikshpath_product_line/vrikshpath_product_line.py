import frappe
from frappe.model.document import Document


class VrikshPathProductLine(Document):
    def validate(self):
        if self.smam_eligible and self.mrp and self.smam_subsidy_pct:
            self.farmer_price_post_smam = self.mrp * (1 - self.smam_subsidy_pct / 100)

    def before_save(self):
        self.validate()
