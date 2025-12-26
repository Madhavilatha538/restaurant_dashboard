from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import Bill
from django.core.mail import send_mail

@shared_task
def alert_manager_pending_bills():
    threshold = timezone.now() - timedelta(minutes=settings.BILL_PENDING_ALERT_MINUTES)
    pending = Bill.objects.filter(status=Bill.Status.PENDING_PAYMENT, created_at__lt=threshold).select_related("table","order")
    if not pending.exists():
        return 0

    # In real deployment, set MANAGER_EMAIL in env, or notify via in-app.
    manager_email = getattr(settings, "MANAGER_EMAIL", None) or "manager@example.com"
    lines = [f"Bill #{b.id} | Table {b.table.number} | Total {b.total} | Created {b.created_at}" for b in pending]
    send_mail(
        subject="Pending bills alert",
        message="Pending bills:
" + "
".join(lines),
        from_email="noreply@example.com",
        recipient_list=[manager_email],
        fail_silently=True,
    )
    return pending.count()
