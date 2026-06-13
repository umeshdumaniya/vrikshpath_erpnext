from frappe.model.document import Document


# Class name must match Frappe's derivation from the doctype name
# "RTK Base Station" -> "RTKBaseStation" (acronym capitalization preserved).
# A mismatch (e.g. RtkBaseStation) causes ImportError on get_doc and makes
# `bench migrate` treat the doctype as orphaned and delete it.
class RTKBaseStation(Document):
    pass
