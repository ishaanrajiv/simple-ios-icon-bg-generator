# The Pillow library is required to run this script.
# Install it with: pip install Pillow
from PIL import Image, ImageDraw
import sys
import argparse

def create_icon_background(hex_color: str, size: int = 1024, depth_factor: float = 1.5):
    """
    Generates a square image with a subtle depth-like gradient.

    Args:
        hex_color (str): The hexadecimal color code for the icon background (e.g., "#007AFF").
        size (int): The resolution of the square image in pixels (e.g., 1024 for 1024x1024).
        depth_factor (float): A multiplier to control the intensity of the gradient effect.
                              Higher values create a more pronounced depth effect.
    """
    # Ensure the hex code starts with a '#'.
    if not hex_color.startswith('#'):
        hex_color = '#' + hex_color

    try:
        # Create a new blank square image.
        img = Image.new('RGB', (size, size), hex_color)
        draw = ImageDraw.Draw(img)

        # Convert the hex color to RGB.
        base_color = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        # Calculate a darker shade for the top of the gradient based on the depth_factor.
        dark_offset = int(20 * depth_factor)
        dark_shade_rgb = tuple(max(0, c - dark_offset) for c in base_color)
        
        # Calculate a lighter shade for the bottom of the gradient based on the depth_factor.
        light_offset = int(20 * depth_factor)
        light_shade_rgb = tuple(min(255, c + light_offset) for c in base_color)

        # Draw the linear gradient.
        # The gradient transitions from a lighter shade at the top to a darker shade
        # in the middle, then back to the base color at the bottom.
        for i in range(size):
            # Calculate the color for the current row based on its position.
            # This creates a smooth transition.
            
            # The top half (from 0 to size/2)
            if i < size / 2:
                # Interpolate from light_shade to base_color
                r = int(light_shade_rgb[0] + (base_color[0] - light_shade_rgb[0]) * (i / (size / 2)))
                g = int(light_shade_rgb[1] + (base_color[1] - light_shade_rgb[1]) * (i / (size / 2)))
                b = int(light_shade_rgb[2] + (base_color[2] - light_shade_rgb[2]) * (i / (size / 2)))
            # The bottom half (from size/2 to size)
            else:
                # Interpolate from base_color to a slightly darker color
                r = int(base_color[0] + (dark_shade_rgb[0] - base_color[0]) * ((i - size / 2) / (size / 2)))
                g = int(base_color[1] + (dark_shade_rgb[1] - base_color[1]) * ((i - size / 2) / (size / 2)))
                b = int(base_color[2] + (dark_shade_rgb[2] - base_color[2]) * ((i - size / 2) / (size / 2)))

            # Draw a single line of the calculated color.
            draw.line([(0, i), (size, i)], fill=(r, g, b))

        # Define the output file name.
        output_filename = f"icon_background_{size}.png"
        img.save(output_filename)
        print(f"Successfully generated and saved {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Use argparse to handle command-line arguments.
    parser = argparse.ArgumentParser(description="Generate an iOS-style icon background with a gradient.")
    parser.add_argument("hex_color", help="The hexadecimal color code (e.g., #007AFF).")
    parser.add_argument("-s", "--size", type=int, default=1024,
                        help="The resolution of the square image in pixels (default: 1024).")
    parser.add_argument("-d", "--depth_factor", type=float, default=3.0,
                        help="A multiplier to control the intensity of the gradient effect (default: 3.0).")

    args = parser.parse_args()
    
    # Call the function with the parsed arguments.
    create_icon_background(args.hex_color, args.size, args.depth_factor)
