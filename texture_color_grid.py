#!/usr/bin/env python3
"""
Texture Color Grid Generator Script

This script creates a 1x10 grid (1 column, 10 rows) showing a texture with 
overlay blend mode at 0.7 opacity for each of the 10 predefined neon colors.

Usage:
    python texture_color_grid.py <texture_name>

Example:
    python texture_color_grid.py stone
    
This will create: stone-color-grid.png (showing the texture with all 10 neon colors)

Author: Karel Smutny, scrumdojo.cz
"""

import os
import sys
import random
from typing import List, Tuple
from PIL import Image
from neon_texture_overlay import (
    load_image,
    blend_texture_with_neon,
    save_image
)
from neon_colors import NEON_COLORS, get_color_names, get_color

# Configuration
BLEND_MODE = 'overlay'
OPACITY = 0.6
INPUT_BASE_PATH = "orig/assets/minecraft/textures/blocks"
OUTPUT_BASE_PATH = "."


def generate_color_grid(texture_name: str) -> Image.Image:
    """
    Generate a 1x10 grid showing the texture with each neon color overlay.
    
    Args:
        texture_name (str): Name of the texture file (without path or extension)
        
    Returns:
        Image.Image: Grid image showing all color variations
    """
    # Construct input path
    input_path = os.path.join(INPUT_BASE_PATH, f"{texture_name}.png")
    
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Texture file not found: {input_path}")
    
    print(f"Loading texture: {texture_name}")
    print(f"Creating 1x10 grid with overlay blend mode at {OPACITY} opacity")
    print(f"Using all {len(NEON_COLORS)} colors in random order")
    
    # Load the base texture
    base_texture = load_image(input_path)
    
    # Use original texture size (no scaling)
    cell_width = base_texture.width
    cell_height = base_texture.height
    
    # Grid configuration: 1 column, 10 rows (one for each color)
    grid_cols = 1
    grid_rows = len(NEON_COLORS)
    
    # Calculate total image dimensions (no padding, just pure tiles)
    total_width = cell_width
    total_height = cell_height * grid_rows
    
    # Create the output image with transparent background
    grid_image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
    
    print(f"Grid dimensions: {grid_cols} col x {grid_rows} rows")
    print(f"Cell size: {cell_width}x{cell_height} pixels")
    print(f"Output size: {total_width}x{total_height} pixels")
    
    # Generate grid cells - one for each color in random order
    color_names = get_color_names()
    random_color_names = color_names.copy()
    random.shuffle(random_color_names)
    
    print(f"Random color order: {', '.join(random_color_names)}")
    
    for row, color_name in enumerate(random_color_names):
        print(f"  Processing {color_name} overlay...")
        
        try:
            # Create the blended texture with current color
            blended_texture = blend_texture_with_neon(
                base_texture,
                neon_color=get_color(color_name),
                opacity=OPACITY,
                blend_mode=BLEND_MODE
            )
            
            # Calculate position in grid (no padding, pure tiles)
            x = 0
            y = row * cell_height
            
            # Paste into grid
            grid_image.paste(blended_texture, (x, y), blended_texture)
            
        except Exception as e:
            print(f"    Warning: Failed to create {color_name} overlay: {e}")
            continue
    
    return grid_image


def process_texture_color_grid(texture_name: str, output_path: str = None) -> str:
    """
    Create a color grid for the specified texture and save it.
    
    Args:
        texture_name (str): Name of the texture (without path or extension)
        output_path (str, optional): Path to save the grid. If None, auto-generates based on texture name.
        
    Returns:
        str: Path to the saved grid file
    """
    # Auto-generate output path if not provided
    if output_path is None:
        output_filename = f"{texture_name}-color-grid.png"
        output_path = os.path.join(OUTPUT_BASE_PATH, output_filename)
    
    print("Starting color grid generation...")
    grid_image = generate_color_grid(texture_name)
    
    print(f"Saving grid to: {output_path}")
    save_image(grid_image, output_path)
    
    return output_path


def main():
    """Command line interface for the texture color grid generator."""
    if len(sys.argv) < 2:
        print("Texture Color Grid Generator")
        print("=" * 50)
        print()
        print("Creates a 1x10 grid (1 column, 10 rows) showing a texture with")
        print("overlay blend mode for each of the 10 predefined neon colors in random order.")
        print()
        print("Usage: python texture_color_grid.py <texture_name> [output_path]")
        print()
        print("Arguments:")
        print("  texture_name        Name of the texture file (without path or .png extension)")
        print("  output_path         Optional: Path to save the grid (auto-generated if omitted)")
        print()
        print("Available Colors (randomized each run):")
        for color_name in get_color_names():
            rgb = get_color(color_name)
            print(f"  - {color_name:<8} - RGB{rgb}")
        print()
        print("Configuration:")
        print(f"  - Blend mode: {BLEND_MODE}")
        print(f"  - Opacity: {OPACITY}")
        print(f"  - Original texture resolution (no scaling)")
        print(f"  - No borders (pure tiles)")
        print()
        print("Examples:")
        print("  python texture_color_grid.py stone")
        print("  python texture_color_grid.py diamond_ore")
        print("  python texture_color_grid.py cobblestone my_grid.png")
        print()
        print("Output file will be created as: texture-color-grid.png (or specified path)")
        sys.exit(1)
    
    texture_name = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else None
    
    try:
        result_path = process_texture_color_grid(texture_name, output_path)
        
        print(f"+ Successfully created color grid: {os.path.basename(result_path)}")
        print(f"  Grid shows texture with all {len(NEON_COLORS)} neon colors")
        print(f"  Layout: 1 column x {len(NEON_COLORS)} rows")
        print(f"  Original texture resolution (no scaling)")
        print(f"  No borders (pure tiles)")
        print(f"  Blend mode: {BLEND_MODE} at {OPACITY} opacity")
        
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
