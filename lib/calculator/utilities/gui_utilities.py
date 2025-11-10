
from picocalc.colors import ( RGB_565,
                              RGB_VT100 )

import turtle


def draw_battery_icon(x, y, percentage, usb_power=False):
    """
    Draw a battery icon with percentage fill and terminal bump.

    Args:
        x, y: Top-left corner of battery body
        percentage: 0-100 (None if USB powered)
        usb_power: True if on USB power

    Icon size: 24x12 pixels (body) + 2px terminal = 26x12 total
    """
    # Battery dimensions
    body_w = 24
    body_h = 12
    terminal_w = 2
    terminal_h = 6

    # Determine battery color based on charge level
    if usb_power:
        outline_color = RGB_VT100.BRIGHT_GREEN
        fill_color = RGB_VT100.BRIGHT_GREEN
        fill_percentage = 100
    elif percentage is None:
        outline_color = RGB_VT100.WHITE
        fill_color = RGB_VT100.WHITE
        fill_percentage = 0
    else:
        # Color coding: Green (>50%), Yellow (20-50%), Red (<20%)
        if percentage > 50:
            outline_color = RGB_VT100.GREEN
            fill_color    = RGB_VT100.GREEN
        elif percentage > 20:
            outline_color = RGB_VT100.YELLOW
            fill_color    = RGB_VT100.YELLOW
        else:
            outline_color = RGB_VT100.RED
            fill_color    = RGB_VT100.RED
        fill_percentage = max( 0, min( 100, percentage ) )

    # Draw battery body outline
    turtle.draw_rect( x, y, body_w, body_h, outline_color )

    # Draw positive terminal (small bump on right side)
    terminal_y = y + (body_h - terminal_h) // 2
    turtle.fill_rect( x + body_w,
                      terminal_y,
                      terminal_w,
                      terminal_h,
                      outline_color)

    # Draw battery fill level
    if fill_percentage > 0:
        # Leave 2px margin inside battery
        fill_w = int((body_w - 4) * fill_percentage / 100)
        if fill_w > 0:
            turtle.fill_rect( x + 2,
                               y + 2,
                               fill_w,
                               body_h - 4,
                               fill_color)

def draw_battery_status(x, y, battery_status):
    """
    Draw battery icon with percentage text.

    Args:
        x, y: Top-left position
        battery_status: Dict from battery.get_status()

    Layout: [ICON] 99%
    Total width: ~60 pixels
    """
    percentage = battery_status.get("percentage")
    usb_power = battery_status.get("usb_power", False)

    # Draw icon
    draw_battery_icon(x, y, percentage, usb_power)

    # Draw percentage text
    if usb_power:
        text = "USB"
        color = RGB_VT100.BRIGHT_GREEN
    elif percentage is not None:
        text = f"{int(percentage)}%"
        # Match icon color
        if percentage > 50:
            color = RGB_VT100.GREEN
        elif percentage > 20:
            color = RGB_VT100.YELLOW
        else:
            color = RGB_VT100.RED
    else:
        text = "--"
        color = RGB_VT100.WHITE

    # Position text to the right of icon (icon is ~26px wide)
    text_x = x + 30
    text_y = y + 2  # Vertically center with icon
    draw_text(text, text_x, text_y, color)