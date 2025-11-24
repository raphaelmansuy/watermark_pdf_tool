import pypdfium2 as pdfium
from PIL import Image

def convert_pdf_to_image(pdf_path, output_path):
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        page = pdf[0]
        bitmap = page.render(scale=2.0) # Higher scale for better quality
        pil_image = bitmap.to_pil()
        pil_image.save(output_path)
        print(f"Saved {output_path}")
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

if __name__ == "__main__":
    convert_pdf_to_image("demos/sample.pdf", "demos/before.png")
    convert_pdf_to_image("demos/sample_watermarked.pdf", "demos/after.png")
