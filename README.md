# Restaurant Live Table Order & Billing System (Django)

Implements the take-home assignment requirements:
- Table dashboard with statuses (Available / Occupied / Bill Requested / Closed)
- Menu items CRUD (Manager)
- Order create + status updates (Waiter) — auto sets table to **Occupied** when order placed
- Billing (Cashier) — generate bill, mark paid (table becomes Available again)
- Notification option implemented: **In-app / WebSocket** kitchen notification when a new order is placed (Django Channels)
- Background task option implemented: **Celery** task to alert manager when bills are pending too long (email; fail_silently by default)

## Tech stack
- Django 4.2, SQLite
- Django REST Framework (bonus APIs)
- Django Channels + Redis (bonus real-time)
- Celery + Redis (background task)
- ReportLab (PDF bill export)

---

## Setup (local)
> Requires Python 3.10+

```bash
cd restaurant_system
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

### Demo credentials
- Waiter: `waiter1` / `waiter123`
- Cashier: `cashier1` / `cashier123`
- Manager: `manager1` / `manager123`

---

## Redis (for WebSockets + Celery)
If you want real-time dashboard updates + kitchen notifications, run Redis:

### Option A: Docker
```bash
docker run --rm -p 6379:6379 redis:7
```

### Option B: Local install
Run redis-server on 6379.

Then run Django (ASGI is already configured in `config/asgi.py`).

---

## Celery (bill pending alerts)
Default threshold: 30 minutes (`BILL_PENDING_ALERT_MINUTES` env).

Run worker:
```bash
celery -A config worker -l info
```

Run beat scheduler (to execute periodic checks):
```bash
celery -A config beat -l info
```

Add a periodic schedule in `config/__init__.py` or via Celery beat DB in production.
For demo, you can run the task manually in Django shell:
```bash
python manage.py shell
>>> from billing.tasks import alert_manager_pending_bills
>>> alert_manager_pending_bills.delay()
```

---

## REST APIs (bonus)
- `/api/tables/` (Manager)
- `/api/menu/` (Manager)
- `/api/orders/` (Waiter)
- `/api/bills/` (Cashier)

---

## Architecture notes
- `restaurant` app: tables + menu CRUD
- `orders` app: order workflow + table status automation
- `billing` app: bill generation + payment workflow + PDF export
- `realtime` app: Channels consumers and broadcast helpers
- `accounts` app: login + seed command

Role-based access is implemented using **Django Groups**:
- Waiter: order operations
- Cashier: billing operations
- Manager: manage tables/menu, view reports (extendable)

---

## Assumptions
- Each table can have multiple orders historically; the latest non-closed order is billed.
- When bill is paid: order is closed and table becomes Available.
