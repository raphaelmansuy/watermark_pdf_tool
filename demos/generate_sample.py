from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf():
    c = canvas.Canvas("demos/sample.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Sample PDF Document")
    c.drawString(100, 730, "This document is used for demonstration purposes.")
    c.drawString(100, 710, "It contains some sample text to test the watermarking tool.")
    c.save()
    print("Created demos/sample.pdf")

if __name__ == "__main__":
    create_sample_pdf()
