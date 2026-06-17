"""
Convert SVG chess pieces to PNG for Pygame
"""
from PIL import Image
import os
import subprocess
import sys

# Install required packages
print("Installing required packages...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'svglib', 'reportlab'])

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# Piece mapping matching your files in the Pieces folder
piece_files = {
    'white_king': 'Pieces/wK.svg',
    'white_queen': 'Pieces/wQ.svg', 
    'white_rook': 'Pieces/wR.svg',
    'white_bishop': 'Pieces/wB.svg',
    'white_knight': 'Pieces/wN.svg',
    'white_pawn': 'Pieces/wP.svg',
    'black_king': 'Pieces/bK.svg',
    'black_queen': 'Pieces/bQ.svg',
    'black_rook': 'Pieces/bR.svg',
    'black_bishop': 'Pieces/bB.svg',
    'black_knight': 'Pieces/bN.svg',
    'black_pawn': 'Pieces/bP.svg',
}

# Create output directory
output_dir = 'pieces_png'
os.makedirs(output_dir, exist_ok=True)

print("\nConverting SVG files to PNG...")
success_count = 0

for piece_name, svg_path in piece_files.items():
    if os.path.exists(svg_path):
        try:
            # Convert SVG to drawing object
            drawing = svg2rlg(svg_path)
            
            # Save as PNG
            png_path = os.path.join(output_dir, f'{piece_name}.png')
            renderPM.drawToFile(drawing, png_path, fmt='PNG')
            
            # Resize to 80x80 pixels
            img = Image.open(png_path)
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            img.save(png_path)
            
            print(f'✓ Converted {svg_path} -> {png_path}')
            success_count += 1
            
        except Exception as e:
            print(f'✗ Error converting {svg_path}: {e}')
    else:
        print(f'✗ File not found: {svg_path}')

print(f'\nConversion complete! {success_count}/12 pieces converted.')
print(f'PNG files saved in: {os.path.abspath(output_dir)}')