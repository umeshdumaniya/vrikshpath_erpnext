// VrikshPath Installation — client script
// Auto-checks RTK coverage from the VrikshPath CORS API when lat/lng are set.

const CORS_API = "https://api.prashang.com/geo/cors/nearby";
const COVERAGE_RADIUS_KM = 60;

frappe.ui.form.on("VrikshPath Installation", {
    farm_lat: check_rtk_coverage,
    farm_lng: check_rtk_coverage,
});

async function check_rtk_coverage(frm) {
    const lat = frm.doc.farm_lat;
    const lng = frm.doc.farm_lng;
    if (!lat || !lng) return;

    frm.set_value("rtk_coverage_note", "Checking CORS coverage...");

    try {
        const url = `${CORS_API}?lat=${lat}&lon=${lng}&max_distance_km=${COVERAGE_RADIUS_KM}&limit=1`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(`API ${res.status}`);
        const data = await res.json();

        if (!data || data.length === 0) {
            frm.set_value("nearest_cors_code", "");
            frm.set_value("nearest_cors_name", "");
            frm.set_value("nearest_cors_dist_km", null);
            frm.set_value("rtk_in_coverage", 0);
            frm.set_value("rtk_coverage_note",
                `No CORS station found within ${COVERAGE_RADIUS_KM} km. ` +
                "A village RTK base station will be required.");
            frappe.show_alert({ message: "No CORS coverage — village base station needed.", indicator: "orange" });
            return;
        }

        const nearest = data[0];
        frm.set_value("nearest_cors_code", nearest.station_code);
        frm.set_value("nearest_cors_name", nearest.station_name + (nearest.state ? ` (${nearest.state})` : ""));
        frm.set_value("nearest_cors_dist_km", nearest.distance_km);
        frm.set_value("rtk_in_coverage", nearest.in_coverage ? 1 : 0);

        const sub_note = nearest.subscription_required
            ? `Subscription required (~₹${nearest.monthly_cost_per_device_inr || "?"}/mo)`
            : "Free public CORS";
        const note = nearest.in_coverage
            ? `✓ CORS ${nearest.station_code} is ${nearest.distance_km} km away — within coverage radius (${nearest.coverage_radius_km} km). ${sub_note}.`
            : `✗ Nearest CORS ${nearest.station_code} is ${nearest.distance_km} km — outside ${nearest.coverage_radius_km} km radius. Village base station needed.`;
        frm.set_value("rtk_coverage_note", note);

        const indicator = nearest.in_coverage ? "green" : "orange";
        const msg = nearest.in_coverage
            ? `RTK covered by CORS ${nearest.station_code} (${nearest.distance_km} km)`
            : `No CORS coverage — ${nearest.distance_km} km to nearest station`;
        frappe.show_alert({ message: msg, indicator });

    } catch (err) {
        frm.set_value("rtk_coverage_note", `Coverage check failed: ${err.message}. Check network.`);
        frappe.show_alert({ message: "RTK coverage check failed", indicator: "red" });
    }
}
