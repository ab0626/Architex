#!/usr/bin/env python3
"""
Create a simple PNG icon for VS Code extension
"""

from PIL import Image, ImageDraw
import os

def create_icon():
    """Create a simple icon"""
    # Create a 128x128 image with a dark background
    img = Image.new('RGBA', (128, 128), (30, 41, 59, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple building/architecture icon
    # Main building
    draw.rectangle([24, 64, 104, 112], fill=(59, 130, 246, 230), outline=(30, 64, 175, 255), width=2)
    
    # Windows
    for x in [32, 48, 64, 80]:
        draw.rectangle([x, 72, x+8, 80], fill=(255, 255, 255, 200))
        draw.rectangle([x, 88, x+8, 96], fill=(255, 255, 255, 200))
    
    # Entrance
    draw.rectangle([56, 96, 72, 112], fill=(255, 255, 255, 230))
    
    # Code blocks (top)
    draw.rectangle([16, 16, 40, 32], fill=(16, 185, 129, 200))
    draw.rectangle([88, 16, 112, 32], fill=(16, 185, 129, 200))
    
    # Connection lines
    draw.line([40, 24, 88, 24], fill=(16, 185, 129, 150), width=2)
    draw.line([64, 24, 64, 64], fill=(16, 185, 129, 150), width=2)
    
    # AI dots
    for x in [32, 48, 64, 80, 96]:
        draw.ellipse([x-2, 38, x+2, 42], fill=(16, 185, 129, 200))
    
    # Save the image
    icon_path = os.path.join('resources', 'icon.png')
    img.save(icon_path, 'PNG')
    print(f"✅ Icon created: {icon_path}")
    return True

if __name__ == "__main__":
    create_icon() 