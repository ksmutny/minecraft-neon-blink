#!/usr/bin/env python3
"""
Neon Colors Module

Predefined neon color palette covering all basic colors from Paint.NET color wheel.
Each color is optimized for vibrant neon overlay effects on textures.

Author: Karel Smutny, scrumdojo.cz
"""

from typing import Dict, Tuple

# Neon color palette - RGB tuples covering Paint.NET color wheel
NEON_COLORS: Dict[str, Tuple[int, int, int]] = {
    'red': (255, 0, 0),            # Bright red
    'orange': (255, 165, 0),       # Electric orange
    'yellow': (255, 255, 0),       # Bright yellow
    'lime': (50, 255, 50),         # Lime green
    'green': (0, 255, 0),          # Pure green
    'cyan': (0, 255, 255),         # Cyan/aqua (default)
    'blue': (0, 100, 255),         # Electric blue
    'purple': (128, 0, 255),       # Purple
    'magenta': (255, 0, 255),      # Magenta/fuchsia
    'pink': (255, 20, 147)         # Hot pink
}

# Default neon color
DEFAULT_COLOR = 'cyan'


def get_color(color_name: str) -> Tuple[int, int, int]:
    """
    Get RGB tuple for a neon color by name.
    
    Args:
        color_name (str): Name of the neon color
        
    Returns:
        Tuple[int, int, int]: RGB color tuple
        
    Raises:
        ValueError: If color name is not found
    """
    color_name = color_name.lower()
    if color_name not in NEON_COLORS:
        available = ', '.join(NEON_COLORS.keys())
        raise ValueError(f"Unknown color '{color_name}'. Available colors: {available}")
    
    return NEON_COLORS[color_name]


def list_colors() -> str:
    """
    Get a formatted string of all available neon colors.
    
    Returns:
        str: Formatted list of color names with RGB values
    """
    lines = []
    for name, rgb in NEON_COLORS.items():
        lines.append(f"  {name:<8} - RGB{rgb}")
    return '\n'.join(lines)


def get_color_names() -> list[str]:
    """
    Get list of all available color names.
    
    Returns:
        list[str]: List of color names
    """
    return list(NEON_COLORS.keys())
