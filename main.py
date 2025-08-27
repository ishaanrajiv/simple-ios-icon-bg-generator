#!/usr/bin/env python3
"""
iOS Style Icon Background Generator
Generates 1024x1024 PNG backgrounds with iOS-style depth effects from hex colors
"""

from PIL import Image, ImageDraw
import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL"""
    return colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

def hsl_to_rgb(h, s, l):
    """Convert HSL to RGB"""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))

def adjust_lightness(rgb, factor):
    """Adjust lightness of RGB color by factor"""
    h, l, s = rgb_to_hsl(*rgb)
    l = max(0, min(1, l * factor))
    return hsl_to_rgb(h, s, l)

def create_gradient_colors(base_hex):
    """Create gradient color stops for iOS style effect"""
    base_rgb = hex_to_rgb(base_hex)
    
    # Create 4 gradient stops
    colors = [
        adjust_lightness(base_rgb, 1.15),  # Lightest (top)
        base_rgb,                          # Base color
        adjust_lightness(base_rgb, 0.92),  # Slightly darker
        adjust_lightness(base_rgb, 0.85)   # Darkest (bottom)
    ]
    
    return colors

def create_radial_gradient(width, height, colors, center_x, center_y, radius):
    """Create a radial gradient"""
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    
    for y in range(height):
        for x in range(width):
            # Calculate distance from center
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            
            # Normalize distance (0 to 1)
            if distance <= radius:
                ratio = distance / radius
            else:
                ratio = 1.0
            
            # Interpolate colors
            if ratio <= 0.33:
                # First third - colors[0] to colors[1]
                t = ratio / 0.33
                color = tuple(int(colors[0][i] + (colors[1][i] - colors[0][i]) * t) for i in range(3))
            elif ratio <= 0.66:
                # Second third - colors[1] to colors[2]
                t = (ratio - 0.33) / 0.33
                color = tuple(int(colors[1][i] + (colors[2][i] - colors[1][i]) * t) for i in range(3))
            else:
                # Final third - colors[2] to colors[3]
                t = (ratio - 0.66) / 0.34
                color = tuple(int(colors[2][i] + (colors[3][i] - colors[2][i]) * t) for i in range(3))
            
            pixels[x, y] = color
    
    return image

def add_inner_highlight(image):
    """Add subtle inner highlight effect (square, no rounded corners)"""
    width, height = image.size
    highlight = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(highlight)
    
    # Create highlight for top portion
    highlight_height = int(height * 0.35)  # Top 35%
    
    # Draw rectangle with white fill, fading opacity
    for i in range(highlight_height):
        opacity = int(255 * 0.4 * (1 - i / highlight_height))  # Fade from 40% to 0%
        color = (255, 255, 255, opacity)
        
        # Draw full-width rectangle for this row
        draw.rectangle([0, i, width, i + 1], fill=color)
    
    # Composite highlight onto base image
    base_rgba = image.convert('RGBA')
    return Image.alpha_composite(base_rgba, highlight)

def add_subtle_shadow(image):
    """Add very subtle inner shadow (square, no rounded corners)"""
    width, height = image.size
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    
    # Very subtle shadow at bottom
    shadow_height = int(height * 0.15)  # Bottom 15%
    
    for i in range(shadow_height):
        opacity = int(255 * 0.08 * (i / shadow_height))  # Fade from 0% to 8%
        color = (0, 0, 0, opacity)
        
        y = height - shadow_height + i
        draw.rectangle([0, y, width, y + 1], fill=color)
    
    # Composite shadow onto image
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    return Image.alpha_composite(image, shadow)

def generate_ios_icon_background(hex_color, output_path='ios_icon_bg.png', size=1024):
    """
    Generate iOS-style icon background for Xcode (square, no rounded corners)
    
    Args:
        hex_color: Input hex color (e.g., '#B3E6E6')
        output_path: Output file path
        size: Output size in pixels (default 1024x1024)
    """
    
    # Create gradient colors
    gradient_colors = create_gradient_colors(hex_color)
    
    # Create radial gradient (slightly off-center for more natural look)
    center_x = int(size * 0.45)  # Slightly left of center
    center_y = int(size * 0.35)  # Higher than center
    radius = int(size * 0.8)     # Large radius for subtle effect
    
    # Generate base gradient
    image = create_radial_gradient(size, size, gradient_colors, center_x, center_y, radius)
    
    # Add inner highlight (no corner radius - full square)
    image = add_inner_highlight(image)
    
    # Add subtle shadow (no corner radius - full square)
    image = add_subtle_shadow(image)
    
    # Convert to RGB for final output (no alpha channel needed)
    if image.mode == 'RGBA':
        # Create white background and composite
        background = Image.new('RGB', image.size, (255, 255, 255))
        image = Image.alpha_composite(background.convert('RGBA'), image).convert('RGB')
    
    # Save as PNG
    image.save(output_path, 'PNG', quality=100, optimize=True)
    print(f"iOS-style icon background saved to: {output_path}")
    print(f"Size: {size}x{size} pixels (square, ready for Xcode)")
    print(f"Base color: {hex_color}")
    print(f"Gradient colors used: {[f'#{r:02x}{g:02x}{b:02x}' for r, g, b in gradient_colors]}")

# Example usage and CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ios_icon_generator.py <hex_color> [output_path] [size]")
        print("Example: python ios_icon_generator.py '#B3E6E6' my_icon_bg.png 1024")
        sys.exit(1)
    
    hex_color = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'ios_icon_bg.png'
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    
    try:
        generate_ios_icon_background(hex_color, output_path, size)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)