from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from kwota import * 
from save_location import give
import os

current_path = os.path.dirname(os.path.realpath(__file__))

def wrap_text(text, max_width, font_name, font_size, canvas_obj):
    words = text.split(" ")
    lines = []
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_width = canvas_obj.stringWidth(test_line, font_name, font_size)
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def generate_invoice(file_name, invoice_data):
    # Rejestracja czcionki obsługującej polskie znaki
    filepath = "code/font/Roboto-Light.ttf"
    #full_file_path = os.path.join(current_path, filepath)
    pdfmetrics.registerFont(TTFont("DejaVuSans", filepath))
    filepath = "code/font/Roboto-Black.ttf"
    #full_file_path = os.path.join(current_path, filepath)
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", filepath))

    # Dane do faktury
    sellerp1 = invoice_data["sellerp1"]
    sellerp2 = invoice_data["sellerp2"]
    sellerp3 = invoice_data["sellerp3"]
    sellerp4 = invoice_data["sellerp4"]
    sellerp5 = invoice_data["sellerp5"]
    buyerp1 = invoice_data["buyerp1"]
    buyerp2 = invoice_data["buyerp2"]
    buyerp3 = invoice_data["buyerp3"]
    buyerp4 = invoice_data["buyerp4"]
    items = invoice_data["items"]
    invoice_number = invoice_data["invoice_number"]
    date = invoice_data["date"]
    pay_method = invoice_data["pay_method"]
    invoices_folder=give()
    full_file_path = os.path.join(invoices_folder, file_name)

    # Rozpoczęcie tworzenia PDF

    c = canvas.Canvas(full_file_path, pagesize=A4)
    c.setFont("DejaVuSans", 12)  # Ustawienie czcionki obsługującej polskie znaki
    width, height = A4

    # Marginesy
    margin_left = 50
    content_width = width - margin_left - 50

    # Nagłówek faktury
    c.setFont("DejaVuSans-Bold", 16)
    c.drawString(margin_left, height - 50, f"Faktura nr: {invoice_number}")
    c.setFont("DejaVuSans", 16)
    c.drawString(margin_left+200, height - 50, f"oryginał/kopia")

    #Data i miejsce wystawienia
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left+360, height - 80, f"{date}")

    # Sprzedawca
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left, height - 120, "Sprzedawca:")

    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left, height - 140, sellerp1)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left, height - 160, sellerp2)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left, height - 180, sellerp3)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left, height - 200, sellerp4)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left, height - 220, sellerp5)

    seller_lines=["1"]

    # Nabywca
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left + 320, height - 120, "Nabywca:")

    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left + 320, height - 140, buyerp1)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left + 320, height - 160, buyerp2)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left + 320, height - 180, buyerp3)
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(margin_left + 320, height - 200, buyerp4)
   
    buyer_lines=["1"]

    # Tabela z pozycjami
    start_y = height - 240 - len(seller_lines) * 15 - len(buyer_lines) * 15
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left, start_y, "Lp.")
    c.drawString(margin_left + 50, start_y, "Nazwa towaru/usługi")
    c.drawString(margin_left + 250, start_y, "Ilość")
    c.drawString(margin_left + 320, start_y, "Cena jedn.")
    c.drawString(margin_left + 400, start_y, "Wartość")

    c.setStrokeColor(colors.black)
    c.line(margin_left, start_y - 5, margin_left + content_width, start_y - 5)  # Linia pod nagłówkiem tabeli

    # Pozycje
    y = start_y - 25
    for idx, item in enumerate(items):
        c.setFont("DejaVuSans", 12)
        c.drawString(margin_left, y, str(idx + 1))
        item_lines = wrap_text(item["name"], 180, "DejaVuSans", 12, c)
        for j, line in enumerate(item_lines):
            c.drawString(margin_left + 50, y - j * 15, line)
        c.drawString(margin_left + 250, y, str(item["quantity"])+" szt.")
        c.drawString(margin_left + 320, y, f"{item['unit_price']:.2f} zł")
        c.drawString(margin_left + 400, y, f"{item['total']:.2f} zł")
        y -= max(20, len(item_lines) * 15)

    # Podsumowanie
    total_value = sum(item["total"] for item in items)
    y -= 20
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left + 320, y, "Razem:")
    c.drawString(margin_left + 400, y, f"{total_value:.2f} zł")

    #Słowna kwota
    y -= 20
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left, y, "Słownie:")

    y -= 20
    c.setFont("DejaVuSans", 12)
    slowne=kwota_slownie(f"{total_value:.2f}")
    slowne_lines = wrap_text(slowne, content_width, "DejaVuSans", 12, c)
    for i, line in enumerate(slowne_lines):
        c.drawString(margin_left, y - i * 15, line)

    #Pouczenie    
    y -= 40
    c.setFont("DejaVuSans", 12)
    pouczenie="Faktura dokumentuje dostawę towarów lub świadczenie usług zwolnionych z podatku od towarów i usług na podstawie: art.43 ust.1 pkt.19 ustawy z dnia 11 marca 2004r. o podatku od towarów i usług (t.j. Dz.U. z 2021r. poz. 685, z późn. zm.)"
    poucz_lines = wrap_text(pouczenie, content_width, "DejaVuSans", 12, c)
    for i, line in enumerate(poucz_lines):
        c.drawString(margin_left, y - i * 15, line)

    #Sposób zapłaty
    y -= 80
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left, y, "Sposób zapłaty: "+pay_method)

    #Podpis
    y -= 80
    c.setFont("DejaVuSans", 12)
    c.drawString(margin_left + 350, y, "Podpis wystawcy faktury:")

    # Zakończenie
    c.save()
    os.startfile(full_file_path)