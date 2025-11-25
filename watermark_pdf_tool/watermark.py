#!/usr/bin/env python3
"""Core watermarking functionality for PDF files."""

import click
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, white

import re
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors
import pypdfium2 as pdfium
from PIL import Image

def get_dominant_color(pdf_path, page_index):
    """
    Detects the dominant color of a specific page in the PDF.
    Returns a hex string (e.g., '#FFFFFF').
    """
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        page = pdf[page_index]
        
        # Render page to image (low res is fine for color detection)
        bitmap = page.render(scale=0.5)
        pil_image = bitmap.to_pil()
        
        # Resize to 1x1 to get average color
        # This is a fast approximation of dominant color
        img = pil_image.resize((1, 1))
        color = img.getpixel((0, 0))
        
        # Convert to hex
        return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
    except Exception as e:
        # Fallback to white if anything fails
        return '#FFFFFF'

def get_contrast_color(hex_color):
    """
    Returns 'black' or 'white' depending on which has better contrast 
    against the given hex_color.
    """
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculate luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        if luminance > 0.5:
            return 'black'
        else:
            return 'white'
    except Exception:
        return 'black'

def create_watermark(text, width, height, position='bottomright', font_size=18, bg_color='auto', text_color='black'):
    """Creates a temporary PDF with the watermark text, making URLs clickable."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    
    # URL detection regex
    url_pattern = r'(https?://[^\s]+)'
    
    # Function to wrap URLs in anchor tags
    def replace_url(match):
        url = match.group(0)
        return f'<a href="{url}" color="{text_color}">{url}</a>'
    
    # Process text to make links clickable
    from xml.sax.saxutils import escape
    safe_text = escape(text)
    formatted_text = re.sub(url_pattern, replace_url, safe_text)
    
    # Use Paragraph for rich text support
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = font_size
    
    # Set text color
    try:
        style.textColor = colors.toColor(text_color)
    except:
        style.textColor = black
    
    p = Paragraph(formatted_text, style)
    
    # Calculate width and height of the paragraph
    max_width = width - 20
    _, p_height = p.wrap(max_width, height)
    
    # Get actual width of the text to position it correctly
    try:
        actual_widths = p.getActualLineWidths0()
        if actual_widths:
            p_width = max(actual_widths)
        else:
            p_width = 0
    except Exception:
        p_width = p.width
    
    # Calculate coordinates based on position
    margin = 10
    x = margin
    y = margin

    if position == 'bottomleft':
        x = margin
        y = margin
    elif position == 'bottomright':
        x = width - p_width - margin
        y = margin
    elif position == 'topleft':
        x = margin
        y = height - p_height - margin
    elif position == 'topright':
        x = width - p_width - margin
        y = height - p_height - margin

    # Draw background box
    padding = 4
    box_x = x - padding
    box_y = y - padding
    box_width = p_width + (padding * 2)
    box_height = p_height + (padding * 2)
    
    try:
        bg_col = colors.toColor(bg_color)
        c.setFillColor(bg_col)
        c.rect(box_x, box_y, box_width, box_height, fill=1, stroke=0)
    except Exception:
        # Fallback if color name is invalid or 'auto' was passed but not handled here
        # (Though 'auto' should be resolved before calling this function usually, 
        # but if we want per-page auto, we pass the resolved color)
        c.setFillColor(colors.white)
        c.rect(box_x, box_y, box_width, box_height, fill=1, stroke=0)

    # Draw at calculated position
    p.drawOn(c, x, y)
    
    c.save()
    packet.seek(0)
    return packet

def add_watermark(input_pdf, output_pdf, text, position, font_size, bg_color):
    """
    Adds a text watermark to a PDF file.
    
    INPUT_PDF: Path to the source PDF file.
    OUTPUT_PDF: Path where the watermarked PDF will be saved.
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            # Get page dimensions
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            # Resolve background color
            current_bg_color = bg_color
            current_text_color = 'black'
            
            if bg_color.lower() == 'auto':
                # Detect dominant color for this page
                detected_hex = get_dominant_color(input_pdf, i)
                current_bg_color = detected_hex
                # Calculate contrast text color
                current_text_color = get_contrast_color(detected_hex)
            else:
                # If user specified a color, we still want good contrast if possible,
                # or we just default to black. Let's try to be smart.
                try:
                    # Convert named color to hex if possible, or just use it
                    # ReportLab handles names, but our contrast logic needs RGB.
                    # For simplicity, if manual color, default text to black unless we want to get fancy.
                    # Let's keep it simple: manual bg -> black text (or maybe we can improve this later)
                    current_text_color = 'black' 
                    
                    # Optional: Try to calculate contrast for manual colors too if they are hex
                    if bg_color.startswith('#'):
                         current_text_color = get_contrast_color(bg_color)
                except:
                    pass

            # Create watermark for this specific page size
            watermark_pdf = create_watermark(text, width, height, position, font_size, current_bg_color, current_text_color)
            watermark_reader = PdfReader(watermark_pdf)
            watermark_page = watermark_reader.pages[0]

            # Merge
            page.merge_page(watermark_page)
            writer.add_page(page)

        with open(output_pdf, "wb") as f:
            writer.write(f)
        
        click.echo(f"Successfully added watermark to {output_pdf}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
