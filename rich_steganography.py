#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Steganography - Hidden Data"""

from rich.console import Console
from rich.panel import Panel
from PIL import Image

console = Console()

class Steganography:
    def hide_data(self, image, data):
        """Hide data in image"""
        console.print(Panel.fit(
            "[bold cyan]Steganography - Hiding Data[/bold cyan]",
            border_style="cyan"
        ))
        
        img = Image.open(image)
        pixels = img.load()
        
        # LSB steganography
        data_bin = ''.join(format(ord(c), '08b') for c in data)
        
        index = 0
        for y in range(img.height):
            for x in range(img.width):
                if index < len(data_bin):
                    r, g, b = pixels[x, y]
                    # Modify LSB
                    r = (r & 0xFE) | int(data_bin[index])
                    pixels[x, y] = (r, g, b)
                    index += 1
        
        img.save("hidden.png")
        console.print("[green]✓ Data hidden in image[/green]")

if __name__ == "__main__":
    steg = Steganography()
    console.print("[yellow]Steganography tool[/yellow]")

