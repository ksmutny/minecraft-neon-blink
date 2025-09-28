#!/usr/bin/env python3
"""
Texture Blend Generator Script

This script takes a texture name, color, and opacity and generates outputs 
for all available blend modes. Each output file includes the blend mode, 
color, and opacity in the filename.

Usage:
    python texture_blend_generator.py <texture_name> <color> <opacity>

Example:
    python texture_blend_generator.py cobblestone red 0.5
    
This will create:
    - cobblestone-red-0.5-screen.png
    - cobblestone-red-0.5-overlay.png
    - cobblestone-red-0.5-multiply.png
    - cobblestone-red-0.5-normal.png

Author: Karel Smutny, scrumdojo.cz
"""

import os
import sys
from typing import List
from neon_texture_overlay import process_texture_with_neon
from neon_colors import get_color_names, list_colors

# Available blend modes
BLEND_MODES = ['screen', 'overlay', 'multiply', 'normal']

# Input and output paths
INPUT_BASE_PATH = "orig/assets/minecraft/textures/blocks"
OUTPUT_BASE_PATH = "resource-pack/assets/minecraft/textures/blocks"


def generate_all_blend_modes(texture_name: str, color_name: str, opacity: float) -> None:
    """
    Generate texture variants for all blend modes.
    
    Args:
        texture_name (str): Name of the texture file (without .png extension)
        color_name (str): Name of the neon color to apply
        opacity (float): Opacity level (0.0 to 1.0)
    """
    # Construct input path
    input_path = os.path.join(INPUT_BASE_PATH, f"{texture_name}.png")
    
    # Verify input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Texture file not found: {input_path}")
    
    # Verify color is valid
    if color_name.lower() not in get_color_names():
        available = ', '.join(get_color_names())
        raise ValueError(f"Unknown color '{color_name}'. Available colors: {available}")
    
    # Verify opacity is valid
    if not (0.0 <= opacity <= 1.0):
        raise ValueError("Opacity must be between 0.0 and 1.0")
    
    print(f"Processing texture: {texture_name}")
    print(f"Color: {color_name}")
    print(f"Opacity: {opacity}")
    print(f"Input: {input_path}")
    print(f"Generating {len(BLEND_MODES)} blend mode variants...")
    print()
    
    results = []
    
    # Generate a variant for each blend mode
    for blend_mode in BLEND_MODES:
        # Create output filename with pattern: texture-color-opacity-blendmode.png
        output_filename = f"{texture_name}-{color_name}-{opacity}-{blend_mode}.png"
        output_path = os.path.join(OUTPUT_BASE_PATH, output_filename)
        
        try:
            print(f"  Creating {blend_mode} blend: {output_filename}")
            process_texture_with_neon(
                input_path=input_path,
                output_path=output_path,
                color_name=color_name,
                opacity=opacity,
                blend_mode=blend_mode
            )
            results.append(output_filename)
            
        except Exception as e:
            print(f"  X Failed to create {blend_mode} blend: {str(e)}")
            continue
    
    print()
    print("Results:")
    for result in results:
        print(f"  + {result}")
    
    if len(results) == len(BLEND_MODES):
        print(f"\n+ Successfully generated all {len(BLEND_MODES)} blend mode variants!")
    else:
        print(f"\n! Generated {len(results)} out of {len(BLEND_MODES)} variants")


def main():
    """Command line interface for the texture blend generator."""
    if len(sys.argv) != 4:
        print("Texture Blend Generator")
        print("=" * 50)
        print()
        print("Usage: python texture_blend_generator.py <texture_name> <color> <opacity>")
        print()
        print("Arguments:")
        print("  texture_name  Name of texture file (without .png extension)")
        print("  color         Neon color name")
        print("  opacity       Opacity level (0.0 to 1.0)")
        print()
        print("Available Colors:")
        print(list_colors())
        print()
        print("Available Blend Modes:")
        for mode in BLEND_MODES:
            print(f"  {mode}")
        print()
        print("Examples:")
        print("  python texture_blend_generator.py cobblestone red 0.5")
        print("  python texture_blend_generator.py stone cyan 0.3")
        print("  python texture_blend_generator.py diamond_ore purple 0.4")
        print()
        print("Output files will be created in the current directory with names like:")
        print("  texture-color-opacity-blendmode.png")
        print("  Example: cobblestone-red-0.5-overlay.png")
        sys.exit(1)
    
    texture_name = sys.argv[1]
    color_name = sys.argv[2]
    
    try:
        opacity = float(sys.argv[3])
    except ValueError:
        print("Error: Opacity must be a valid number between 0.0 and 1.0")
        sys.exit(1)
    
    try:
        generate_all_blend_modes(texture_name, color_name, opacity)
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
