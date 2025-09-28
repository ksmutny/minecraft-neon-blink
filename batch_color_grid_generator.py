#!/usr/bin/env python3
"""
Batch Color Grid Generator Script

This script processes all textures in the orig/assets/minecraft/textures/blocks directory
and creates animated color grids for each one, except for textures that already have
.mcmeta files (which are already animated).

The script creates a 1x10 grid (1 column, 10 rows) for each texture showing the texture
with overlay blend mode at 0.6 opacity for each of the 10 predefined neon colors in
random order.

Usage:
    python batch_color_grid_generator.py

Output:
    - Creates texture.png files in resource-pack/assets/minecraft/textures/blocks/
    - Creates texture.png.mcmeta files with animation data for each processed texture

Author: Karel Smutny, scrumdojo.cz
"""

import os
import sys
from pathlib import Path
from typing import List, Set
from texture_color_grid import process_texture_color_grid

# Configuration
INPUT_BASE_PATH = "orig/assets/minecraft/textures/blocks"
OUTPUT_BASE_PATH = "resource-pack/assets/minecraft/textures/blocks"


def get_all_png_files() -> List[str]:
    """
    Get all PNG files in the input directory.
    
    Returns:
        List[str]: List of PNG filenames (without extension)
    """
    input_path = Path(INPUT_BASE_PATH)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {INPUT_BASE_PATH}")
    
    png_files = []
    for file_path in input_path.glob("*.png"):
        # Get filename without extension
        texture_name = file_path.stem
        png_files.append(texture_name)
    
    return sorted(png_files)


def get_existing_mcmeta_textures() -> Set[str]:
    """
    Get textures that already have .mcmeta files in the original directory.
    
    Returns:
        Set[str]: Set of texture names (without extension) that have .mcmeta files
    """
    input_path = Path(INPUT_BASE_PATH)
    mcmeta_textures = set()
    
    for mcmeta_file in input_path.glob("*.mcmeta"):
        # Extract texture name from filename.png.mcmeta
        texture_name = mcmeta_file.name.replace(".png.mcmeta", "")
        mcmeta_textures.add(texture_name)
    
    return mcmeta_textures


def get_textures_to_process() -> List[str]:
    """
    Get list of textures that need processing (all PNG files except those with .mcmeta).
    
    Returns:
        List[str]: List of texture names to process
    """
    all_textures = get_all_png_files()
    existing_mcmeta = get_existing_mcmeta_textures()
    
    # Filter out textures that already have .mcmeta files
    textures_to_process = [texture for texture in all_textures 
                          if texture not in existing_mcmeta]
    
    return textures_to_process


def batch_process_textures(textures: List[str]) -> None:
    """
    Process a batch of textures to create color grids.
    
    Args:
        textures (List[str]): List of texture names to process
    """
    total_count = len(textures)
    success_count = 0
    failed_textures = []
    
    print(f"Processing {total_count} textures...")
    print(f"Output directory: {OUTPUT_BASE_PATH}")
    print("=" * 60)
    
    for i, texture_name in enumerate(textures, 1):
        print(f"\n[{i:3d}/{total_count}] Processing: {texture_name}")
        
        try:
            texture_path, mcmeta_path = process_texture_color_grid(texture_name)
            success_count += 1
            print(f"  ✓ Created: {os.path.basename(texture_path)}")
            print(f"  ✓ Created: {os.path.basename(mcmeta_path)}")
            
        except Exception as e:
            failed_textures.append((texture_name, str(e)))
            print(f"  ✗ Failed: {str(e)}")
            continue
    
    # Summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total textures processed: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_textures)}")
    
    if failed_textures:
        print(f"\nFailed textures:")
        for texture_name, error in failed_textures:
            print(f"  - {texture_name}: {error}")
    
    if success_count > 0:
        print(f"\n✓ Successfully created {success_count * 2} files:")
        print(f"  - {success_count} animated texture files (.png)")
        print(f"  - {success_count} animation metadata files (.mcmeta)")
        print(f"\nFiles created in: {OUTPUT_BASE_PATH}")


def main():
    """Main function for batch processing."""
    print("Batch Color Grid Generator")
    print("=" * 60)
    print()
    
    try:
        # Get textures to process
        print("Scanning for textures...")
        all_textures = get_all_png_files()
        existing_mcmeta = get_existing_mcmeta_textures()
        textures_to_process = get_textures_to_process()
        
        print(f"Found {len(all_textures)} total PNG textures")
        print(f"Found {len(existing_mcmeta)} textures with existing .mcmeta files:")
        for texture in sorted(existing_mcmeta):
            print(f"  - {texture}")
        
        print(f"\nTextures to process: {len(textures_to_process)}")
        
        if not textures_to_process:
            print("No textures need processing. All PNG files already have .mcmeta files.")
            return
        
        # Ask for confirmation
        print(f"\nWill create animated color grids for {len(textures_to_process)} textures.")
        print("Each texture will have a 1x10 grid with randomized neon color overlays.")
        
        response = input("\nProceed with batch processing? (y/n): ").lower().strip()
        if response not in ['y', 'yes']:
            print("Batch processing cancelled.")
            return
        
        # Process textures
        batch_process_textures(textures_to_process)
        
    except (FileNotFoundError, IOError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nBatch processing interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
