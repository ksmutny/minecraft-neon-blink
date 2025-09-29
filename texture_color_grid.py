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
OUTPUT_BASE_PATH = "resource-pack/assets/minecraft/textures/blocks"

BLOCK_GROUPS = [
    "log_oak", "log_spruce", "log_birch", "log_jungle", "log_acacia", "log_big_oak",
    "quartz_block_lines", "hay_block_side", "tnt", "bed", 
    "door_wood", "door_spruce", "door_birch", "door_jungle", "door_acacia", "door_dark_oak",
    "door_iron", "piston", "anvil", "brewing_stand", "enchanting_table",
    "cauldron", "crafting_table", "furnace", "dispenser", "dropper",
    "jukebox", "grass", "mycelium", "podzol", "pumpkin", "melon"
]

def get_texture_prefix(texture_name: str) -> str:
    """
    Get the prefix of a texture name for consistent color ordering.
    
    Args:
        texture_name (str): Name of the texture
        
    Returns:
        str: Prefix of the texture name or the full name if no prefix found
    """
    # Find matching prefix from BLOCK_GROUPS
    for group in BLOCK_GROUPS:
        if group.startswith(texture_name.split('_')[0]):
            return group.split('_')[0]
    return texture_name

def generate_color_grid(texture_name: str) -> Image.Image:
    """
    Generate a 1x10 grid showing the texture with each neon color overlay.
    Textures with same prefix will have identical color sequence.
    
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
    
    # Get prefix and use it as seed for consistent ordering
    prefix = get_texture_prefix(texture_name)
    random.seed(prefix)
    
    # Generate grid cells - one for each color with prefix-based ordering
    color_names = get_color_names()
    random_color_names = color_names.copy()
    random.shuffle(random_color_names)
    
    # Reset the random seed to not affect other random operations
    random.seed()
    
    print(f"Color order for prefix '{prefix}': {', '.join(random_color_names)}")
    
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


def create_mcmeta_file(texture_path: str) -> str:
    """
    Create a .mcmeta file for animation alongside the texture.
    
    Args:
        texture_path (str): Path to the texture file
        
    Returns:
        str: Path to the created .mcmeta file
    """
    mcmeta_path = f"{texture_path}.mcmeta"
    mcmeta_content = '{\n  "animation": {}\n}'
    
    try:
        with open(mcmeta_path, 'w') as f:
            f.write(mcmeta_content)
        return mcmeta_path
    except Exception as e:
        raise IOError(f"Cannot create mcmeta file {mcmeta_path}: {str(e)}")


def process_texture_color_grid(texture_name: str, output_path: str = None) -> tuple[str, str]:
    """
    Create a color grid for the specified texture and save it with mcmeta file.
    
    Args:
        texture_name (str): Name of the texture (without path or extension)
        output_path (str, optional): Path to save the grid. If None, uses resource-pack structure.
        
    Returns:
        tuple[str, str]: Paths to the saved texture file and mcmeta file
    """
    # Use resource-pack structure if no output path provided
    if output_path is None:
        output_filename = f"{texture_name}.png"
        output_path = os.path.join(OUTPUT_BASE_PATH, output_filename)
    
    print("Starting color grid generation...")
    grid_image = generate_color_grid(texture_name)
    
    print(f"Saving texture to: {output_path}")
    save_image(grid_image, output_path)
    
    print(f"Creating animation mcmeta file...")
    mcmeta_path = create_mcmeta_file(output_path)
    print(f"Saved mcmeta to: {mcmeta_path}")
    
    return output_path, mcmeta_path


def main():
    """Command line interface for the texture color grid generator."""
    if len(sys.argv) < 2:
        print("Texture Color Grid Generator")
        print("=" * 50)
        print()
        print("Creates a 1x10 grid (1 column, 10 rows) showing a texture with")
        print("overlay blend mode for each of the 10 predefined neon colors in random order.")
        print()
        print("Usage: python texture_color_grid.py <texture_name>")
        print()
        print("Arguments:")
        print("  texture_name        Name of the texture file (without path or .png extension)")
        print()
        print("Output:")
        print("  - Creates texture.png in resource-pack/assets/minecraft/textures/blocks/")
        print("  - Creates texture.png.mcmeta with animation data")
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
        print("  python texture_color_grid.py cobblestone")
        print()
        print("Output files will be created in resource-pack structure:")
        sys.exit(1)
    
    texture_name = sys.argv[1]
    
    try:
        texture_path, mcmeta_path = process_texture_color_grid(texture_name)
        
        print(f"+ Successfully created animated texture:")
        print(f"  Texture: {os.path.basename(texture_path)}")
        print(f"  Animation: {os.path.basename(mcmeta_path)}")
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
