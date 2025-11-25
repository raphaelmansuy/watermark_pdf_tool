#!/usr/bin/env python3
"""Watermark CLI entry point.
Imports the core add_watermark function from the package and exposes it as a console script.
"""

import click
from .watermark import add_watermark

@click.command()
@click.argument('input_pdf', type=click.Path(exists=True))
@click.argument('output_pdf', type=click.Path())
@click.option('--text', required=True, help='Text to add as watermark. URLs starting with http/https will be automatically detected and made clickable.')
@click.option('--position', type=click.Choice(['topleft', 'bottomleft', 'topright', 'bottomright'], case_sensitive=False), default='bottomright', help='Position of the watermark on the page. Default is bottomright.')
@click.option('--font-size', type=int, default=18, help='Font size of the watermark text. Default is 18.')
@click.option('--bg-color', default='auto', help='Background color of the watermark box. Default is "auto" (detects dominant page color).')
def main(input_pdf, output_pdf, text, position, font_size, bg_color):
    """Thin wrapper that forwards arguments to :func:`watermark.add_watermark`."""
    add_watermark(input_pdf, output_pdf, text, position, font_size, bg_color)

if __name__ == '__main__':
    main()
