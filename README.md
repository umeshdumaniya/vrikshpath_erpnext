# vrikshpath_erpnext

Custom Frappe/ERPNext app for **Prashang Technologies Pvt Ltd** — the company behind the VrikshPath product line.

## Products managed in this app

| Module | Product | Status |
|--------|---------|--------|
| M19T | AutoSteer Kit (Path 1 + Path 2) | Prototype |
| M19T-BASE | RTK Base Station | Prototype |
| M19W | Cotton Picking Rover | Design |
| M19X | Kshetra Kendra (Stambha village edge) | Design |
| M19N | LoRaWAN Pump Controller | Design |

## Architecture

This is a **custom Frappe app** — it installs on top of standard ERPNext.  
ERPNext core lives at [umeshdumaniya/erpnext](https://github.com/umeshdumaniya/erpnext) (fork of frappe/erpnext).  
This app adds VrikshPath-specific doctypes, reports, and the dealer-technician portal.

## Custom Doctypes

- **VrikshPath Product Line** — registry of all hardware products with SMAM eligibility, pricing, BOM link
- **VrikshPath Installation** — tracks every kit deployed at a farm (dealer, tractor, GPS, calibration, SMAM)

## Development workflow

```
# Pull upstream ERPNext updates into the fork
cd erpnext-fork
git remote add upstream https://github.com/frappe/erpnext
git fetch upstream
git checkout version-15
git merge upstream/version-15
git push origin version-15

# Then rebase vrikshpath-prod on top
git checkout vrikshpath-prod
git rebase version-15
git push origin vrikshpath-prod --force-with-lease
```

## Adding a new product

1. Create a new BOM in ERPNext under Manufacturing → BOM
2. Add a new row in **VrikshPath Product Line** linking the FG item + BOM
3. If the product needs custom fields/logic, add a new doctype here

## Deployment

Deployed via Coolify on `192.168.80.10` → `erp.prashang.com`  
See `apps.json` — frappe_docker pulls frappe + erpnext fork + this app together.
