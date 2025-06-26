#!/usr/bin/env python3
"""
Generate PNG icon for VS Code extension from SVG
"""

import os
import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    print("Installing cairosvg...")
    os.system("pip install cairosvg")
    import cairosvg

def generate_png_icon():
    """Generate PNG icon from SVG"""
    current_dir = Path(__file__).parent
    svg_path = current_dir / "resources" / "icon.svg"
    png_path = current_dir / "resources" / "icon.png"
    
    if not svg_path.exists():
        print(f"SVG file not found: {svg_path}")
        return False
    
    try:
        # Convert SVG to PNG
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=128,
            output_height=128
        )
        print(f"✅ PNG icon generated: {png_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating PNG: {e}")
        return False

if __name__ == "__main__":
    success = generate_png_icon()
    sys.exit(0 if success else 1) 