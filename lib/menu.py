# menu.py - Main Dashboard Menu for PicoCalc
import sys
import time
import gc
try:
    import picocalc  # type: ignore  # noqa
except Exception:
    # Provide minimal stubs for development environments without hardware
    class _DummyTerm:
        def wr(self, _):
            pass
    class _DummyPC:
        terminal = _DummyTerm()
    picocalc = _DummyPC()
from ui import *
from battery import get_status as get_battery_status

# Hide terminal cursor for clean UI (no-op on stub)
try:
    picocalc.terminal.wr("\x1b[?25l")
except Exception:
    pass

# ============ Menu Pages ============

def show_main_menu(battery_status):
    """
    Display main menu and handle selection.
    
    Returns:
        Selected option code (str) or None
    """
    menu_items = [
        ("Open REPL", "repl"),
        ("Memory Stats", "memory"),
        ("Battery Status", "battery"),
        ("Servo Control", "servo"),
        ("GPIO Control", "gpio"),
        ("File Manager", "files"),
        ("Run App", "app"),
        ("Edit File", "edit"),
        ("Play Music", "music"),
        ("Power Off / Reset", "power"),
    ]
    
    selected = 0
    
    while True:
        clear()
        
        # Draw title bar with battery indicator
        draw_title_bar("PicoCalc Dashboard", battery_status)
        
        # Draw menu items
        y_start = 40
        line_height = 20
        
        for i, (label, _) in enumerate(menu_items):
            y = y_start + i * line_height
            draw_menu_item(label, 12, y, selected=(i == selected))
        
        # Draw help text at bottom
        draw_text("UP/DOWN: Navigate | ENTER: Select", 12, 290, COLOR_YELLOW)
        
        # Wait for input
        key = wait_key_raw()
        
        if key == 'A':  # Up
            selected = (selected - 1) % len(menu_items)
        elif key == 'B':  # Down
            selected = (selected + 1) % len(menu_items)
        elif key in ('\r', '\n'):  # Enter
            return menu_items[selected][1]
        elif key in ('q', 'Q'):  # Quick quit
            return "power"
        
        # Update battery status for next iteration
        try:
            battery_status = get_battery_status()
        except:
            pass

def show_memory_stats():
    """Display memory statistics with visual representation."""
    clear()
    
    # Get battery status for title bar
    try:
        battery_status = get_battery_status()
    except:
        battery_status = None
    
    draw_title_bar("Memory Statistics", battery_status)
    
    # Get memory info
    free_bytes = gc.mem_free()
    alloc_bytes = gc.mem_alloc()
    total_bytes = free_bytes + alloc_bytes
    
    if total_bytes > 0:
        free_pct = int(100 * free_bytes / total_bytes)
        alloc_pct = 100 - free_pct
    else:
        free_pct = alloc_pct = 0
    
    # Display text info
    y = 50
    draw_text(f"Total:     {total_bytes:>10} bytes", 20, y, COLOR_WHITE)
    y += 20
    draw_text(f"Free:      {free_bytes:>10} bytes", 20, y, COLOR_GREEN)
    y += 20
    draw_text(f"Allocated: {alloc_bytes:>10} bytes", 20, y, COLOR_RED)
    y += 20
    draw_text(f"Free:      {free_pct:>10}%", 20, y, COLOR_CYAN)
    
    # Draw visual bar
    y += 30
    bar_x = 20
    bar_w = 280
    bar_h = 30
    
    draw_rect(bar_x, y, bar_w, bar_h, COLOR_WHITE, fill=False)
    
    # Calculate bar widths
    free_bar_w = int((bar_w - 2) * free_pct / 100)
    alloc_bar_w = (bar_w - 2) - free_bar_w
    
    # Draw free memory (green)
    if free_bar_w > 0:
        fb.fill_rect(bar_x + 1, y + 1, free_bar_w, bar_h - 2, COLOR_GREEN)
    
    # Draw allocated memory (red)
    if alloc_bar_w > 0:
        fb.fill_rect(bar_x + 1 + free_bar_w, y + 1, alloc_bar_w, bar_h - 2, COLOR_RED)
    
    # Labels below bar
    y += bar_h + 8
    draw_text("Free", bar_x + 4, y, COLOR_GREEN)
    draw_text("Used", bar_x + bar_w - 40, y, COLOR_RED)
    
    # Additional info
    y += 30
    center_text("Detailed info available in REPL:", y, COLOR_CYAN)
    y += 16
    center_text(">>> import gc", y, COLOR_WHITE)
    y += 16
    center_text(">>> gc.mem_free()", y, COLOR_WHITE)
    
    # Wait for key
    draw_text("Press any key to return...", 12, 290, COLOR_YELLOW)
    wait_key_raw()

def show_battery_details():
    """Display detailed battery information."""
    clear()
    
    # Get battery status
    try:
        battery_status = get_battery_status()
    except Exception as e:
        clear()
        center_text("Battery Module Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()
        return
    
    draw_title_bar("Battery Status", battery_status)
    
    # Display battery info
    y = 50
    voltage = battery_status.get("voltage", 0)
    voltage_mv = battery_status.get("voltage_mv", 0)
    percentage = battery_status.get("percentage")
    usb_power = battery_status.get("usb_power", False)
    status_text = battery_status.get("status", "Unknown")
    
    # Voltage
    draw_text(f"Voltage:    {voltage:.2f} V  ({voltage_mv} mV)", 20, y, COLOR_WHITE)
    y += 24
    
    # USB Power detection
    if usb_power:
        draw_text(f"Power:      USB Connected", 20, y, COLOR_CYAN)
        y += 24
        draw_text(f"Status:     Charging/Powered", 20, y, COLOR_CYAN)
        y += 24
        draw_text(f"Percentage: Not calculated (USB)", 20, y, COLOR_YELLOW)
    else:
        draw_text(f"Power:      Battery", 20, y, COLOR_WHITE)
        y += 24
        
        # Status
        if percentage is not None:
            if percentage > 50:
                status_color = COLOR_GREEN
            elif percentage > 20:
                status_color = COLOR_YELLOW
            else:
                status_color = COLOR_RED
            
            draw_text(f"Percentage: {int(percentage)}%", 20, y, status_color)
            y += 24
            draw_text(f"Status:     {status_text}", 20, y, status_color)
        else:
            draw_text(f"Percentage: Unknown", 20, y, COLOR_WHITE)
            y += 24
            draw_text(f"Status:     {status_text}", 20, y, COLOR_WHITE)
    
    # Draw large battery icon
    if not usb_power and percentage is not None:
        y += 30
        
        # Large progress bar showing battery level
        bar_x = 40
        bar_w = 240
        bar_h = 40
        
        # Determine color
        if percentage > 50:
            bar_color = COLOR_GREEN
        elif percentage > 20:
            bar_color = COLOR_YELLOW
        else:
            bar_color = COLOR_RED
        
        draw_progress_bar(bar_x, y, bar_w, bar_h, percentage, bar_color)
        
        # Percentage text inside bar
        pct_text = f"{int(percentage)}%"
        text_x = 160 - len(pct_text) * 4  # Center in 320px screen
        text_y = y + 16  # Center in bar
        draw_text(pct_text, text_x, text_y, COLOR_WHITE)
    
    # Technical info at bottom
    y = 240
    draw_text("Battery: 2x 18650 Li-ion (7600mAh)", 20, y, COLOR_CYAN)
    y += 16
    draw_text("Range: 3.0V - 4.2V per cell", 20, y, COLOR_CYAN)
    
    # Wait for key
    draw_text("Press any key to return...", 12, 290, COLOR_YELLOW)
    wait_key_raw()

def run_app_selector():
    """Launch app selector and runner."""
    try:
        from loadapp import run_app
        run_app()
        
        # Show completion message
        clear()
        center_text("App Finished", 140, COLOR_GREEN)
        center_text("Press any key to return...", 290, COLOR_YELLOW)
        wait_key_raw()
    except Exception as e:
        clear()
        center_text("App Loader Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()

def run_file_editor():
    """Launch file selector and editor."""
    try:
        from fileselect import select_file
        
        # Select file to edit
        path = select_file(
            path="/sd",
            exts=(".py", ".txt", ".json", ".csv", ".log"),
            title="Select File to Edit",
            return_full_path=True
        )
        
        if not path:
            return  # User cancelled
        
        # Show opening message
        clear()
        filename = path.split("/")[-1]
        center_text(f"Opening {filename}...", 140, COLOR_YELLOW)
        time.sleep(0.3)
        
        # Use built-in editor if available on this firmware
        import builtins as _bi
        ed = getattr(_bi, "edit", None)
        if not ed:
            raise RuntimeError("Built-in edit() is not available on this firmware")
        ed(path)
        
        # Show completion message
        clear()
        center_text("Editor Closed", 140, COLOR_GREEN)
        center_text("Press any key to return...", 290, COLOR_YELLOW)
        wait_key_raw()
        
    except Exception as e:
        clear()
        center_text("Editor Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()

def run_music_player():
    """Launch music file selector and player."""
    try:
        from play import play_music_file
        play_music_file()
    except Exception as e:
        clear()
        center_text("Music Player Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()

def run_gpio_control():
    """Open the graphical GPIO configuration UI."""
    try:
        from gpio_control import show_gpio_control
        show_gpio_control()
    except Exception as e:
        clear()
        center_text("GPIO Control Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()

def run_file_manager():
    """Open the file manager for browsing and managing files."""
    try:
        from fileselect import select_file
        select_file(
            path="/sd",
            exts=None,
            title="File Manager",
            return_full_path=True,
            mode="manage"
        )
    except Exception as e:
        clear()
        center_text("File Manager Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()

def show_power_menu():
    """Show power options (reset/shutdown)."""
    clear()
    
    draw_text("Power Options", 8, 8, COLOR_WHITE)
    draw_line_horizontal(24, 0, 320, COLOR_WHITE)
    
    options = [
        ("Reset Device", "reset"),
        ("Cancel", "cancel"),
    ]
    
    selected = 0
    
    while True:
        # Draw options
        y_start = 80
        line_height = 24
        
        for i in range(len(options)):
            y = y_start + i * line_height
            # Clear line first
            fb.fill_rect(0, y, 320, line_height, COLOR_BLACK)
        
        for i, (label, _) in enumerate(options):
            y = y_start + i * line_height
            draw_menu_item(label, 12, y, selected=(i == selected))
        
        center_text("Warning: Unsaved data will be lost!", 160, COLOR_RED)
        draw_text("UP/DOWN: Navigate | ENTER: Select", 12, 290, COLOR_YELLOW)
        
        # Wait for input
        key = wait_key_raw()
        
        if key == 'A':  # Up
            selected = (selected - 1) % len(options)
        elif key == 'B':  # Down
            selected = (selected + 1) % len(options)
        elif key in ('\r', '\n'):  # Enter
            return options[selected][1]
        elif key in ('q', 'Q'):  # Quick cancel
            return "cancel"

def run_servo_control():
    """Open the multi-servo control dashboard."""
    try:
        from servo_control import show_servo_control
        show_servo_control()
    except Exception as e:
        clear()
        center_text("Servo Control Error", 100, COLOR_RED)
        center_text(str(e), 130, COLOR_WHITE)
        center_text("Press any key...", 290, COLOR_YELLOW)
        wait_key_raw()

# ============ Main Loop ============

def main():
    """Main dashboard loop."""
    
    # Get initial battery status
    try:
        battery_status = get_battery_status()
    except:
        battery_status = None
    
    while True:
        # Show main menu and get selection
        choice = show_main_menu(battery_status)
        
        if choice == "repl":
            # Exit to REPL
            picocalc.terminal.wr("\x1b[?25h")  # Show cursor
            clear()
            center_text("Exiting to REPL...", 140, COLOR_CYAN)
            time.sleep(0.3)
            return  # Exit to REPL
            
        elif choice == "memory":
            show_memory_stats()
            
        elif choice == "battery":
            show_battery_details()
            
        elif choice == "servo":
            run_servo_control()
            
        elif choice == "gpio":
            run_gpio_control()
            
        elif choice == "files":
            run_file_manager()
            
        elif choice == "sudoku":
            run_sudoku()
            
        elif choice == "app":
            run_app_selector()
            
        elif choice == "edit":
            run_file_editor()
            
        elif choice == "music":
            run_music_player()
            
        elif choice == "power":
            power_choice = show_power_menu()
            if power_choice == "reset":
                clear()
                center_text("Resetting Device...", 140, COLOR_RED)
                time.sleep(0.5)
                try:
                    import machine
                    machine.reset()
                except:
                    sys.exit()
        
        # Update battery status for next menu display
        try:
            battery_status = get_battery_status()
        except:
            pass

# ============ Entry Point ============

if __name__ == "__main__":
    main()
