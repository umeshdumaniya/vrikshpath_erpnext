import frappe
from frappe.model.document import Document


class SubsidyApplication(Document):
    def validate(self):
        self._calculate_amounts()

    def _calculate_amounts(self):
        if self.full_price_inr and self.subsidy_pct:
            self.subsidy_amount_inr = round(self.full_price_inr * self.subsidy_pct / 100, 2)
            self.farmer_net_inr = round(self.full_price_inr - self.subsidy_amount_inr, 2)

    def on_submit(self):
        if self.status == "Draft":
            self.db_set("status", "Submitted")
