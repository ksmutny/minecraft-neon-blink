#!/usr/bin/env python3
"""
Texture Grid Generator Script

This script creates a grid visualization showing all blend modes and opacity levels
for a given texture and color. Each cell in the grid shows the texture with a
specific blend mode and opacity combination, scaled 8x for better visibility.

Grid layout:
- Rows: Different blend modes (screen, overlay, multiply, normal)
- Columns: Different opacity levels (0.1 to 0.9, step 0.1)

Usage:
    python texture_grid_generator.py <texture_name> <color>

Example:
    python texture_grid_generator.py cobblestone red
    
This will create: cobblestone-red-grid.png

Author: Karel Smutny, scrumdojo.cz
"""

import os
import sys
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from neon_texture_overlay import (
    load_image,
    blend_texture_with_neon
)
from neon_colors import get_color_names, get_color, list_colors

# Configuration
BLEND_MODES = ['screen', 'overlay', 'multiply', 'normal']
OPACITY_LEVELS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
SCALE_FACTOR = 8
CELL_PADDING = 4
LABEL_HEIGHT = 20
INPUT_BASE_PATH = "orig/assets/minecraft/textures/blocks"
OUTPUT_BASE_PATH = "."


def scale_image_nearest(image: Image.Image, scale_factor: int) -> Image.Image:
    """
    Scale an image using nearest neighbor (no interpolation) for pixel-perfect scaling.
    
    Args:
        image (Image.Image): Input image to scale
        scale_factor (int): Factor to scale by (e.g., 8 for 8x scaling)
        
    Returns:
        Image.Image: Scaled image with crisp pixels
    """
    new_size = (image.width * scale_factor, image.height * scale_factor)
    return image.resize(new_size, Image.NEAREST)


def create_text_label(text: str, width: int, height: int) -> Image.Image:
    """
    Create a text label image with specified dimensions.
    
    Args:
        text (str): Text to render
        width (int): Width of the label
        height (int): Height of the label
        
    Returns:
        Image.Image: Label image with text
    """
    label = Image.new('RGBA', (width, height), (40, 40, 40, 255))
    draw = ImageDraw.Draw(label)
    
    # Try to use a basic font, fall back to default if not available
    try:
        # This might not work on all systems, so we'll catch the exception
        font = ImageFont.load_default()
    except:
        font = None
    
    # Calculate text position for centering
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        # Rough estimate for default font
        text_width = len(text) * 6
        text_height = 11
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text in white
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return label


def generate_texture_grid(texture_name: str, color_name: str) -> Image.Image:
    """
    Generate a grid showing all blend modes and opacity combinations.
    
    Args:
        texture_name (str): Name of the texture file (without .png extension)
        color_name (str): Name of the neon color to apply
        
    Returns:
        Image.Image: Grid image showing all combinations
    """
    # Load and validate inputs
    input_path = os.path.join(INPUT_BASE_PATH, f"{texture_name}.png")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Texture file not found: {input_path}")
    
    if color_name.lower() not in get_color_names():
        available = ', '.join(get_color_names())
        raise ValueError(f"Unknown color '{color_name}'. Available colors: {available}")
    
    print(f"Loading texture: {texture_name}")
    print(f"Color: {color_name}")
    print(f"Creating grid with {len(BLEND_MODES)} blend modes and {len(OPACITY_LEVELS)} opacity levels")
    
    # Load the base texture
    base_texture = load_image(input_path)
    
    # Scale the base texture 8x
    scaled_texture = scale_image_nearest(base_texture, SCALE_FACTOR)
    cell_width = scaled_texture.width
    cell_height = scaled_texture.height
    
    # Calculate grid dimensions
    grid_cols = len(OPACITY_LEVELS)
    grid_rows = len(BLEND_MODES)
    
    # Calculate total image dimensions including labels and padding
    total_width = (cell_width + CELL_PADDING) * grid_cols + CELL_PADDING + 100  # Extra space for row labels
    total_height = (cell_height + CELL_PADDING) * grid_rows + CELL_PADDING + LABEL_HEIGHT + 30  # Extra space for column labels
    
    # Create the output image
    grid_image = Image.new('RGBA', (total_width, total_height), (20, 20, 20, 255))
    
    print(f"Grid dimensions: {grid_cols} cols x {grid_rows} rows")
    print(f"Cell size: {cell_width}x{cell_height} pixels")
    print(f"Output size: {total_width}x{total_height} pixels")
    
    # Add column labels (opacity values)
    label_y = 5
    for col, opacity in enumerate(OPACITY_LEVELS):
        label_x = 100 + col * (cell_width + CELL_PADDING) + CELL_PADDING + cell_width // 2 - 20
        label = create_text_label(f"{opacity:.1f}", 40, LABEL_HEIGHT)
        grid_image.paste(label, (label_x, label_y), label)
    
    # Generate grid cells
    for row, blend_mode in enumerate(BLEND_MODES):
        print(f"  Processing {blend_mode} blend mode...")
        
        # Add row label (blend mode)
        label_y = LABEL_HEIGHT + 30 + row * (cell_height + CELL_PADDING) + CELL_PADDING + cell_height // 2 - 10
        label = create_text_label(blend_mode, 90, 20)
        grid_image.paste(label, (5, label_y), label)
        
        for col, opacity in enumerate(OPACITY_LEVELS):
            # Create the blended texture
            try:
                blended_texture = blend_texture_with_neon(
                    base_texture,
                    neon_color=get_color(color_name),
                    opacity=opacity,
                    blend_mode=blend_mode
                )
                
                # Scale the blended texture
                scaled_blended = scale_image_nearest(blended_texture, SCALE_FACTOR)
                
                # Calculate position in grid
                x = 100 + col * (cell_width + CELL_PADDING) + CELL_PADDING
                y = LABEL_HEIGHT + 30 + row * (cell_height + CELL_PADDING) + CELL_PADDING
                
                # Paste into grid
                grid_image.paste(scaled_blended, (x, y), scaled_blended)
                
            except Exception as e:
                print(f"    Warning: Failed to create {blend_mode} with opacity {opacity}: {e}")
                continue
    
    return grid_image


def main():
    """Command line interface for the texture grid generator."""
    if len(sys.argv) != 3:
        print("Texture Grid Generator")
        print("=" * 50)
        print()
        print("Creates a grid visualization showing all blend modes and opacity levels")
        print("for a given texture and color combination.")
        print()
        print("Usage: python texture_grid_generator.py <texture_name> <color>")
        print()
        print("Arguments:")
        print("  texture_name  Name of texture file (without .png extension)")
        print("  color         Neon color name")
        print()
        print("Available Colors:")
        print(list_colors())
        print()
        print("Grid Layout:")
        print("  - Rows: Blend modes (screen, overlay, multiply, normal)")
        print("  - Columns: Opacity levels (0.1 to 0.9, step 0.1)")
        print("  - Each texture is scaled 8x for better visibility")
        print()
        print("Examples:")
        print("  python texture_grid_generator.py cobblestone red")
        print("  python texture_grid_generator.py stone cyan")
        print("  python texture_grid_generator.py diamond_ore purple")
        print()
        print("Output file will be created as: texture-color-grid.png")
        sys.exit(1)
    
    texture_name = sys.argv[1]
    color_name = sys.argv[2]
    
    try:
        print("Starting grid generation...")
        grid_image = generate_texture_grid(texture_name, color_name)
        
        # Save the grid
        output_filename = f"{texture_name}-{color_name}-grid.png"
        output_path = os.path.join(OUTPUT_BASE_PATH, output_filename)
        
        print(f"Saving grid to: {output_filename}")
        grid_image.save(output_path, 'PNG')
        
        print(f"+ Successfully created grid: {output_filename}")
        print(f"  Grid shows {len(BLEND_MODES)} blend modes x {len(OPACITY_LEVELS)} opacity levels")
        print(f"  Each texture scaled {SCALE_FACTOR}x for better visibility")
        
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
