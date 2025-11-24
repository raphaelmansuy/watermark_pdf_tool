from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import black

def debug_paragraph_width():
    text = "https://www.linkedin.com/in/raphaelmansuy/"
    width = 595.0 # A4 width approx
    height = 842.0
    
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 12
    
    p = Paragraph(text, style)
    
    max_width = width - 20
    p_width, p_height = p.wrap(max_width, height)
    
    print(f"Page Width: {width}")
    print(f"Max Width passed to wrap: {max_width}")
    print(f"Returned p_width: {p_width}")
    
    # Check actual line widths
    try:
        actual_widths = p.getActualLineWidths0()
        print(f"Actual line widths: {actual_widths}")
        if actual_widths:
            print(f"Max actual width: {max(actual_widths)}")
    except AttributeError:
        print("getActualLineWidths0 not available")

if __name__ == "__main__":
    debug_paragraph_width()
