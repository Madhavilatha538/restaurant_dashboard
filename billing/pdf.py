from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def render_bill_pdf(bill):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Restaurant Bill #{bill.id}")
    y -= 25
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Table: {bill.table.number}   Order: {bill.order.id}")
    y -= 20
    c.drawString(50, y, f"Created: {bill.created_at.strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Item")
    c.drawString(300, y, "Qty")
    c.drawString(360, y, "Price")
    c.drawString(450, y, "Line Total")
    y -= 15
    c.line(50, y, 550, y)
    y -= 18

    c.setFont("Helvetica", 11)
    for oi in bill.order.items.select_related("menu_item").all():
        c.drawString(50, y, oi.menu_item.name[:35])
        c.drawRightString(330, y, str(oi.quantity))
        c.drawRightString(420, y, f"{oi.menu_item.price:.2f}")
        c.drawRightString(550, y, f"{oi.line_total():.2f}")
        y -= 18
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 10
    c.line(50, y, 550, y)
    y -= 25
    c.drawRightString(550, y, f"Subtotal: {bill.subtotal:.2f}")
    y -= 18
    c.drawRightString(550, y, f"Tax: {bill.tax_amount:.2f}")
    y -= 18
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(550, y, f"Total: {bill.total:.2f}")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf
