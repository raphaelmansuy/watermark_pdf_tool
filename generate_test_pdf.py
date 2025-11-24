from reportlab.pdfgen import canvas

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "This is a test PDF document.")
    c.drawString(100, 730, "It has some content.")
    c.save()

if __name__ == "__main__":
    create_dummy_pdf("test_input.pdf")
