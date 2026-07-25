# Pharmacy Stock Management System

A command-line application for managing a pharmacy's medicine inventory.
Built by **Group 14** , backed by a MySQL
database hosted on Aiven cloud.

---

## Features

- **Add medicine** — record name, quantity, price, and expiry date.
- **View stock** — list all medicines sorted alphabetically.
- **Search** — find medicines by full or partial name.
- **Update** — change a medicine's name, price, or adjust its quantity
  (add or deduct).
- **Delete** — remove a medicine, with a confirmation prompt if stock remains.
- **Alerts** — flag expired medicines, medicines expiring within 30 days,
  and items at or below the low-stock threshold (10 units).
- **Requests** — log requests for medicines that need to be ordered.
- **Reports** — summarise total medicines, total items, total stock value,
  and all logged requests.

---

## Requirements

- **Python 3.7+**
- **mysql-connector-python** package
- Internet access (the database is hosted online)

Install the one dependency with:

```bash
pip install mysql-connector-python
```

---

## Setup
.
1. The database connection details are already set inside the file
   (host, port, user, password, database). No extra configuration is needed
   to run against the shared Aiven database.
2. The first time you run the program, it automatically creates the two
   required tables (`medicines` and `requests`) if they do not already exist.
   You do not need to set up the tables manually.

---

## How to Run

From the folder containing the file, run:

```bash
python3 `pharmacy-stock-managment.py`
```

You'll see a welcome message followed by the main menu. Type the number of
the action you want and press Enter:

```
***** What do you want to do? *****
1. Add medicine
2. View medicine stocks
3. Search medicine
4. Update medicine
5. Delete medicine
6. Medicine alerts
7. Requests
8. Reports
9. Exit
```

The program loops back to this menu after each action until you choose **9**
to exit.

---

## How It Works

### Database connection
Every operation opens a fresh connection to the MySQL database, runs its
query, commits any changes, and closes the connection. This keeps each action
self-contained.

### Input validation
Three helper functions guard against bad input by re-asking until the value
is valid:

- `ask_number` — accepts only whole numbers.
- `ask_price` — accepts whole numbers or decimals, and rejects negatives.
- `ask_date` — requires the `dd/mm/yyyy` format.

### Data storage
Two tables hold all data:

| Table | Columns |
|-------|---------|
| `medicines` | id, name, quantity, price, expiry_date |
| `requests`  | id, name, description, request_date |

The `id` column is auto-generated, so you never type it in — you read it from
the stock list when updating or deleting.

### Alerts logic
When you open **Medicine alerts**, the program compares each expiry date
against today:

- **Expired** — expiry date is before today.
- **Expiring soon** — expiry date falls within the next 30 days.
- **Low stock** — quantity is 10 or below.

You can change these thresholds by editing the `LOW_STOCK` and
`DAYS_BEFORE_EXPIRY` values near the top of the file.

---

## Typical Workflow

1. Run the program and choose **1** to add a few medicines.
2. Use **2** to confirm they're stored.
3. Check **6** regularly to catch expiring or low-stock items.
4. Use **7** to log anything that needs reordering.
5. Use **8** for a quick overview of inventory value and pending requests.

---

## Notes & Security

- **Credentials in the code:** the database username and password are written
  directly inside `pharmacy-stock-management.py`. This is fine for a class project, but for any real
  use you should move them into environment variables or a separate config
  file that is not shared publicly.
- **Shared database:** because everyone runs against the same online database,
  changes made by one user are visible to all.
- **Dates** are always entered and displayed in `dd/mm/yyyy` format.

---

## GROUP MEMBERS
ACE SWENDO
CRAIG DAVID 
DAVID BOYO
JUANNE ASABAH
DAVID AURELIEN

---

*Group 14 — Pharmacy Stock Management System*
