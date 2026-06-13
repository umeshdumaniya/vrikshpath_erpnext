import frappe
from frappe.model.document import Document


class AssemblyPreCheck(Document):
    def validate(self):
        # ESD-safe is true only when all three conditions hold.
        humidity_ok = bool(self.humidity_pct and self.humidity_pct > 40)
        self.esd_safe_confirmed = int(
            bool(self.anti_static_mat) and bool(self.wrist_strap) and humidity_ok
        )
        if self.anti_static_mat and self.wrist_strap and not humidity_ok:
            frappe.msgprint(
                "Mat and strap are set, but humidity is not above 40% — "
                "ESD risk remains HIGH. Component damage may be silent.",
                indicator="orange",
                title="ESD Warning",
            )
