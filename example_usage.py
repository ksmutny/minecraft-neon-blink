#!/usr/bin/env python3
"""
Example usage of the neon texture overlay script.

This file demonstrates how to use the individual functions
programmatically instead of using the command line interface.
"""

from neon_texture_overlay import (
    load_image,
    create_neon_overlay,
    blend_texture_with_neon,
    save_image,
    process_texture_with_neon
)


def example_basic_usage():
    """Basic example: Apply cyan neon overlay to a texture."""
    input_file = "orig/assets/minecraft/textures/blocks/stone.png"
    output_file = "resource-pack/assets/minecraft/textures/blocks/stone.png"
    
    # Simple one-liner processing
    process_texture_with_neon(input_file, output_file)


def example_custom_colors():
    """Example with different neon colors."""
    input_file = "orig/assets/minecraft/textures/blocks/diamond_ore.png"
    
    # Purple neon
    process_texture_with_neon(
        input_file,
        "resource-pack/assets/minecraft/textures/blocks/diamond_ore_purple.png",
        neon_color=(255, 0, 255),  # Purple
        opacity=0.4
    )
    
    # Green neon
    process_texture_with_neon(
        input_file,
        "resource-pack/assets/minecraft/textures/blocks/diamond_ore_green.png",
        neon_color=(0, 255, 0),  # Green
        opacity=0.5,
        blend_mode='overlay'
    )


def example_manual_processing():
    """Example using individual functions for more control."""
    input_file = "orig/assets/minecraft/textures/blocks/redstone_ore.png"
    output_file = "resource-pack/assets/minecraft/textures/blocks/redstone_ore.png"
    
    # Load the texture
    texture = load_image(input_file)
    
    # Apply red neon overlay manually
    neon_texture = blend_texture_with_neon(
        texture,
        neon_color=(255, 50, 50),  # Red with slight orange tint
        opacity=0.6,
        blend_mode='screen'
    )
    
    # Save the result
    save_image(neon_texture, output_file)
    print(f"Processed {input_file} → {output_file}")


def example_batch_processing():
    """Example of processing multiple textures with different effects."""
    
    # Define textures and their neon colors
    texture_configs = [
        ("stone.png", (100, 200, 255), 0.3),     # Light blue
        ("dirt.png", (139, 69, 19), 0.25),       # Brown glow
        ("grass_side.png", (50, 255, 50), 0.4),  # Green
        ("sand.png", (255, 255, 100), 0.3),      # Yellow
        ("cobblestone.png", (150, 150, 255), 0.35) # Light purple
    ]
    
    for texture_name, color, opacity in texture_configs:
        input_path = f"orig/assets/minecraft/textures/blocks/{texture_name}"
        output_path = f"resource-pack/assets/minecraft/textures/blocks/{texture_name}"
        
        try:
            process_texture_with_neon(
                input_path,
                output_path,
                neon_color=color,
                opacity=opacity,
                blend_mode='screen'
            )
            print(f"✓ Processed {texture_name}")
        except (FileNotFoundError, IOError) as e:
            print(f"✗ Skipped {texture_name}: {e}")


if __name__ == "__main__":
    print("Neon Texture Overlay Examples")
    print("=" * 40)
    
    print("\n1. Basic usage example:")
    try:
        example_basic_usage()
    except Exception as e:
        print(f"Example failed: {e}")
    
    print("\n2. Custom colors example:")
    try:
        example_custom_colors()
    except Exception as e:
        print(f"Example failed: {e}")
    
    print("\n3. Manual processing example:")
    try:
        example_manual_processing()
    except Exception as e:
        print(f"Example failed: {e}")
    
    print("\n4. Batch processing example:")
    try:
        example_batch_processing()
    except Exception as e:
        print(f"Example failed: {e}")
    
    print("\nAll examples completed!")
