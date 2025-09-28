#!/usr/bin/env python3
"""
Neon Texture Overlay Script

This script applies a transparent neon color overlay to textures.
Provides reusable functions for image processing operations.

Author: Karel Smutny, scrumdojo.cz
"""

import os
import sys
from typing import Tuple, Optional
from PIL import Image, ImageEnhance
from neon_colors import NEON_COLORS, DEFAULT_COLOR, get_color, list_colors, get_color_names


def load_image(input_path: str) -> Image.Image:
    """
    Load an image from the specified input path.
    
    Args:
        input_path (str): Path to the input image file
        
    Returns:
        Image.Image: Loaded PIL Image object
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        IOError: If the file cannot be opened as an image
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    try:
        image = Image.open(input_path)
        # Convert to RGBA to ensure we can work with transparency
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        return image
    except Exception as e:
        raise IOError(f"Cannot open image file {input_path}: {str(e)}")


def create_neon_overlay(size: Tuple[int, int], 
                       neon_color: Tuple[int, int, int] = (0, 255, 255),
                       opacity: float = 0.3) -> Image.Image:
    """
    Create a transparent neon overlay of the specified size.
    
    Args:
        size (Tuple[int, int]): Width and height of the overlay
        neon_color (Tuple[int, int, int]): RGB color for the neon effect (default: cyan)
        opacity (float): Opacity level (0.0 to 1.0, default: 0.3)
        
    Returns:
        Image.Image: RGBA image with neon overlay
    """
    if not (0.0 <= opacity <= 1.0):
        raise ValueError("Opacity must be between 0.0 and 1.0")
    
    # Create a solid color image
    overlay = Image.new('RGBA', size, (*neon_color, int(255 * opacity)))
    return overlay


def apply_neon_glow(image: Image.Image, 
                   glow_color: Tuple[int, int, int] = (0, 255, 255),
                   glow_intensity: float = 1.5) -> Image.Image:
    """
    Apply a subtle glow effect to enhance the neon appearance.
    
    Args:
        image (Image.Image): Input image
        glow_color (Tuple[int, int, int]): RGB color for the glow
        glow_intensity (float): Intensity of the glow effect
        
    Returns:
        Image.Image: Image with glow effect applied
    """
    # Create a copy to work with
    glowed = image.copy()
    
    # Enhance the brightness slightly for glow effect
    enhancer = ImageEnhance.Brightness(glowed)
    glowed = enhancer.enhance(glow_intensity)
    
    return glowed


def blend_texture_with_neon(texture: Image.Image,
                           neon_color: Tuple[int, int, int] = (0, 255, 255),
                           opacity: float = 0.3,
                           blend_mode: str = 'screen') -> Image.Image:
    """
    Blend a texture with a neon overlay using specified blend mode.
    
    Args:
        texture (Image.Image): Original texture image
        neon_color (Tuple[int, int, int]): RGB color for neon effect
        opacity (float): Opacity of the neon overlay
        blend_mode (str): Blending mode ('screen', 'overlay', 'multiply', 'normal')
        
    Returns:
        Image.Image: Blended image with neon effect
    """
    # Reduce saturation to make the image nearly black and white, but retain alpha channel
    enhancer = ImageEnhance.Color(texture)
    desaturated_texture = enhancer.enhance(0.0)
    # Create neon overlay
    neon_overlay = create_neon_overlay(desaturated_texture.size, neon_color, opacity)
    # Apply blending based on specified mode
    if blend_mode == 'screen':
        # Screen blend for bright neon effect
        result = Image.blend(desaturated_texture, neon_overlay, opacity)
    elif blend_mode == 'overlay':
        # Overlay blend for more dramatic effect
        result = Image.alpha_composite(desaturated_texture, neon_overlay)
    elif blend_mode == 'multiply':
        # Multiply for darker neon effect
        result = Image.blend(desaturated_texture, neon_overlay, opacity * 0.5)
    else:  # normal blend
        result = Image.alpha_composite(desaturated_texture, neon_overlay)
    # Apply glow effect
    result = apply_neon_glow(result, neon_color)
    return result


def save_image(image: Image.Image, output_path: str) -> None:
    """
    Save the processed image to the specified output path as PNG.
    
    Args:
        image (Image.Image): Image to save
        output_path (str): Path where to save the image (will be saved as PNG)
        
    Raises:
        IOError: If the image cannot be saved
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Ensure the output path has .png extension
    if not output_path.lower().endswith('.png'):
        output_path = os.path.splitext(output_path)[0] + '.png'
    
    try:
        # Save as PNG with transparency support
        image.save(output_path, 'PNG')
    except Exception as e:
        raise IOError(f"Cannot save image to {output_path}: {str(e)}")


def process_texture_with_neon(input_path: str,
                             output_path: str,
                             neon_color: Tuple[int, int, int] = None,
                             color_name: str = None,
                             opacity: float = 0.3,
                             blend_mode: str = 'screen') -> None:
    """
    Main function to process a texture with neon overlay effect.
    
    Args:
        input_path (str): Path to input texture file
        output_path (str): Path to save the processed image (will be saved as PNG)
        neon_color (Tuple[int, int, int]): RGB color for neon effect (deprecated, use color_name)
        color_name (str): Name of predefined neon color (default: 'cyan')
        opacity (float): Opacity of neon overlay (0.0 to 1.0)
        blend_mode (str): Blending mode for the effect
    """
    # Handle color selection - prefer color_name over neon_color
    if color_name is not None:
        final_color = get_color(color_name)
    elif neon_color is not None:
        final_color = neon_color
    else:
        final_color = get_color(DEFAULT_COLOR)
    print(f"Loading texture from: {input_path}")
    texture = load_image(input_path)
    
    print(f"Applying neon overlay (color: {final_color}, opacity: {opacity}, mode: {blend_mode})")
    processed_image = blend_texture_with_neon(texture, final_color, opacity, blend_mode)
    
    print(f"Saving result to: {output_path}")
    save_image(processed_image, output_path)
    
    print("✓ Neon texture overlay completed successfully!")


def main():
    """
    Command line interface for the neon texture overlay script.
    """
    if len(sys.argv) < 3:
        print("Usage: python neon_texture_overlay.py <input_path> <output_path> [options]")
        print("\nOptions:")
        print(f"  --color NAME     Neon color name (default: {DEFAULT_COLOR})")
        print("  --opacity FLOAT  Opacity level 0.0-1.0 (default: 0.3)")
        print("  --blend MODE     Blend mode: screen, overlay, multiply, normal (default: screen)")
        print("  --list-colors    Show all available neon colors and exit")
        print("\nAvailable Colors:")
        print(list_colors())
        print("\nExamples:")
        print("  python neon_texture_overlay.py input.png output.png")
        print("  python neon_texture_overlay.py input.png output.png --color purple --opacity 0.5")
        print("  python neon_texture_overlay.py input.png output.png --color red --blend overlay")
        print("\nNote: Output will always be saved as PNG format with transparency support.")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Default values
    color_name = DEFAULT_COLOR
    opacity = 0.3
    blend_mode = 'screen'
    
    # Parse optional arguments
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--list-colors':
            print("Available Neon Colors:")
            print(list_colors())
            sys.exit(0)
        elif sys.argv[i] == '--color' and i + 1 < len(sys.argv):
            color_name = sys.argv[i + 1].lower()
            if color_name not in get_color_names():
                available = ', '.join(get_color_names())
                print(f"Error: Unknown color '{color_name}'. Available colors: {available}")
                sys.exit(1)
            i += 2
        elif sys.argv[i] == '--opacity' and i + 1 < len(sys.argv):
            try:
                opacity = float(sys.argv[i + 1])
                if not (0.0 <= opacity <= 1.0):
                    raise ValueError()
            except ValueError:
                print("Error: --opacity must be a number between 0.0 and 1.0")
                sys.exit(1)
            i += 2
        elif sys.argv[i] == '--blend' and i + 1 < len(sys.argv):
            blend_mode = sys.argv[i + 1]
            if blend_mode not in ['screen', 'overlay', 'multiply', 'normal']:
                print("Error: --blend must be one of: screen, overlay, multiply, normal")
                sys.exit(1)
            i += 2
        else:
            print(f"Unknown option: {sys.argv[i]}")
            sys.exit(1)
    
    try:
        process_texture_with_neon(input_path, output_path, color_name=color_name, opacity=opacity, blend_mode=blend_mode)
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
