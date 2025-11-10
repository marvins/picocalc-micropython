
#  Codes per GS4_HMSB
class GS4:
    BLACK      =  0
    GRAY       =  8
    RED        =  9
    GREEN      = 10
    YELLOW     = 11
    BLUE       = 12
    PURPLE     = 13
    CYAN       = 14
    LIGHT_GRAY = 15

class RGB_565:

    # Extended RGB565 color palette (for fill_rect/primitives ONLY, not text!)
    # Format: 0bRRRRRGGGGGGBBBBB (5 red, 6 green, 5 blue bits)
    BLACK = 0x0000           # Black
    WHITE = 0xFFFF           # White
    DARK_GRAY = 0x4208       # Dark gray for subtle borders
    LIGHT_GRAY = 0xC618      # Light gray for UI elements
    ORANGE = 0xFC00          # Bright orange for warnings
    LIME = 0x07E0            # Bright lime green
    PINK = 0xF81F            # Bright pink/magenta
    PURPLE = 0x8010          # Purple
    LIGHT_BLUE = 0x051F      # Light blue/cyan
    DARK_GREEN = 0x0320      # Dark green
    BRIGHT_RED = 0xF800      # Bright red
    BRIGHT_BLUE = 0x001F     # Bright blue
    BRIGHT_YELLOW = 0xFFE0   # Bright yellow
    TRUE_GREEN = 0x07E0      # True green (RGB 0,255,0)
    TRUE_CYAN = 0x07FF       # True cyan (RGB 0,255,255)
    TRUE_MAGENTA = 0xF81F    # True magenta (RGB 255,0,255)



    @staticmethod
    def from_rgb( r, g, b ):
        # Ensure the RGB values are within the 0-255 range
        r = int( max(0, min(255, r)) / 255.0 * 31.0 )
        g = int( max(0, min(255, g)) / 255.0 * 63.0 )
        b = int( max(0, min(255, b)) / 255.0 * 31.0 )

        # Convert to RGB565
        rgb565 = (r << 11) | (g << 5) | b
        return rgb565

class RGB_VT100:

    # ============ Color Definitions ============
    # VT100 color indices (0-7) - USE THESE FOR TEXT RENDERING
    # The PicoCalc text renderer only supports these 8 palette indices
    BLACK        = 0   # 0x0000 - Black
    BLUE         = 1   # 0x0080 - Dark Blue
    RED          = 2   # 0x0004 - Dark Red
    TEAL         = 3   # 0x0084 - Dark Green/Teal (what VT100 calls "green")
    BRIGHT_GREEN = 4   # 0x1000 - Bright Green (what VT100 calls "cyan")
    BLUE_GREEN   = 5   # 0x1080 - Blue-Green (what VT100 calls "magenta")
    BROWN        = 6   # 0x1004 - Dark Yellow/Brown (what VT100 calls "yellow")
    WHITE        = 7   # 0x18C6 - Light Gray/White

# Aliases for VT100 indices (for text compatibility)
#COLOR_GREEN = COLOR_BRIGHT_GREEN  # Use index 4 for "green" text (displays bright green)
#COLOR_CYAN = COLOR_TEAL           # Use index 3 for "cyan" text (displays teal)
#COLOR_YELLOW = COLOR_BROWN        # Use index 6 for "yellow" text (displays brown)
#COLOR_MAGENTA = COLOR_BLUE_GREEN  # Use index 5 for "magenta" text (displays blue-green)
