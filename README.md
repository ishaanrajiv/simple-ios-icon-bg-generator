# Simple iOS Icon Background Generator (from Hex Code)

A Python script that generates square images with subtle gradient backgrounds from a hex code, with optional transparent PNG overlay support, perfect for iOS app icons.

## Features

- Creates square images with customizable gradient effects
- Supports any hex color input
- Configurable image size and gradient depth
- Generates smooth linear gradients with depth-like appearance
- Optional transparent PNG foreground overlay support

## Requirements

- Python 3.x
- Pillow library

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py "#007AFF"
```

### Advanced Options

```bash
python main.py "#007AFF" --size 512 --depth_factor 2.0 --foreground icon.png
```

### Arguments

- `hex_color` (required): The hexadecimal color code (e.g., "#007AFF")
- `-s, --size`: Resolution of the square image in pixels (default: 1024)
- `-d, --depth_factor`: Multiplier to control gradient intensity (default: 3.0)
- `-f, --foreground`: Optional path to a transparent PNG to overlay on the background

## Examples

Generate a blue icon background:
```bash
python main.py "#007AFF"
```

Create a smaller red background with subtle gradient:
```bash
python main.py "#FF3B30" --size 256 --depth_factor 1.0
```

Create a green background with pronounced depth effect:
```bash
python main.py "#34C759" --size 1024 --depth_factor 2.5
```

Generate a background with foreground overlay:
```bash
python main.py "#FF9500" --foreground logo.png
```

## Output

The script generates a PNG file named `icon_background_{size}.png` in the current directory.

## How It Works

The gradient creates a subtle depth effect by:
1. Starting with a lighter shade at the top
2. Transitioning to the base color in the middle
3. Ending with a slightly darker shade at the bottom

The `depth_factor` parameter controls how pronounced this gradient effect appears.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.