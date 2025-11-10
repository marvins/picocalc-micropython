# fileselect.py - File selector for PicoCalc Dashboard
import os
import time
import ui_temp as ui

# ============ Helper Functions for File Management ============

def _simple_input(prompt, default="", max_len=30):
    """Simple text input using keyboard. Returns None if cancelled."""
    text = default
    cursor_pos = len(text)

    while True:
        ui.clear()
        ui.draw_text(prompt, 8, 60, ui.COLOR_CYAN)
        ui.draw_line_horizontal(80, 0, 320, ui.COLOR_WHITE)

        # Draw text with cursor
        display_text = text if len(text) <= 36 else text[:36]
        ui.draw_text(display_text, 8, 100, ui.COLOR_WHITE)

        # Draw cursor
        cursor_x = 8 + cursor_pos * 8
        if cursor_x < 320:
            fb.fill_rect(cursor_x, 108, 8, 2, ui.COLOR_YELLOW)

        ui.draw_text("Type to edit | ENTER: OK | Q: Cancel", 8, 290, ui.COLOR_YELLOW)
        ui.draw_text("Use BACKSPACE to delete", 8, 306, ui.COLOR_YELLOW)

        key = ui.wait_key_raw()

        if key in ('\r', '\n'):
            return text if text else None
        elif key in ('q', 'Q'):
            return None
        elif key == '\x7f' or key == '\x08':  # Backspace/Delete
            if cursor_pos > 0:
                text = text[:cursor_pos-1] + text[cursor_pos:]
                cursor_pos -= 1
        elif len(key) == 1 and 32 <= ord(key) <= 126:  # Printable ASCII
            if len(text) < max_len:
                text = text[:cursor_pos] + key + text[cursor_pos:]
                cursor_pos += 1
        elif key == 'C':  # Right arrow
            cursor_pos = min(len(text), cursor_pos + 1)
        elif key == 'D':  # Left arrow
            cursor_pos = max(0, cursor_pos - 1)

        time.sleep(0.01)

def _confirm_dialog(message, item_name=""):
    """Show yes/no confirmation dialog. Returns True if confirmed."""
    while True:
        ui.clear()
        ui.draw_text("Confirm Action", 8, 60, ui.COLOR_RED)
        ui.draw_line_horizontal(80, 0, 320, ui.COLOR_WHITE)

        ui.center_text(message, 120, ui.COLOR_WHITE)
        if item_name:
            # Truncate if needed
            display_name = item_name if len(item_name) <= 36 else item_name[:33] + "..."
            ui.center_text(display_name, 140, ui.COLOR_YELLOW)

        ui.center_text("Are you sure?", 180, ui.COLOR_RED)

        ui.draw_text("Y: Yes | N: No", 8, 290, ui.COLOR_YELLOW)

        key = ui.wait_key_raw()
        if key in ('y', 'Y'):
            return True
        elif key in ('n', 'N', 'q', 'Q'):
            return False

def _show_message(title, message, color= ui.COLOR_WHITE, wait_time=1.5):
    """Show a temporary message."""
    ui.clear()
    ui.center_text(title, 120, color)
    ui.center_text(message, 150, ui.COLOR_WHITE)
    time.sleep(wait_time)

def _action_menu(item_name, is_dir):
    """Show action menu for file/directory. Returns action or None."""
    actions = [
        ("Rename", "rename"),
        ("Delete", "delete"),
        ("Cancel", "cancel"),
    ]

    selected = 0

    while True:
        ui.clear()
        ui.draw_text("File Actions", 8, 8, ui.COLOR_CYAN)
        ui.draw_text(item_name if len(item_name) <= 38 else item_name[:35] + "...", 8, 24, ui.COLOR_YELLOW)
        ui.draw_line_horizontal(40, 0, 320, ui.COLOR_WHITE)

        y = 80
        for i, (label, _) in enumerate(actions):
            ui.draw_menu_item(label, 12, y + i * 24, selected=(i == selected))

        ui.draw_text("UP/DOWN: Navigate | ENTER: Select", 8, 290, ui.COLOR_YELLOW)

        key = ui.wait_key_raw()
        if key == 'A':
            selected = (selected - 1) % len(actions)
        elif key == 'B':
            selected = (selected + 1) % len(actions)
        elif key in ('\r', '\n'):
            return actions[selected][1]
        elif key in ('q', 'Q'):
            return "cancel"

def select_file(path="/sd", exts=None, title="Select File", return_full_path=True, max_visible=10, mode="select"):
    """
    Display a file selector and return the selected file, or manage files.

    Args:
        path: Directory to browse
        exts: Tuple of allowed extensions (e.g., (".py", ".txt")) or None for all
        title: Title to display
        return_full_path: If True, return full path; if False, return filename only
        max_visible: Maximum number of visible items
        mode: 'select' for file selection, 'manage' for file management

    Returns:
        Selected file path/name, or None if cancelled (in select mode)
        None when exiting (in manage mode)

    Controls:
        Up/Down arrows: Navigate
        Enter: Select file/enter directory (select mode) or show actions (manage mode)
        Left arrow: Go up to parent directory
        Q: Cancel/Exit
        N: New folder (manage mode only)
    """
    current_path = path

    while True:
        try:
            # Get list of files and directories
            all_items = os.listdir(current_path)
        except Exception as e:
            ui.clear()
            ui.center_text("Error reading directory", 100, ui.COLOR_RED)
            ui.center_text(str(e), 120, ui.COLOR_RED)
            ui.center_text("Press any key...", 280, ui.COLOR_YELLOW)
            ui.wait_key_raw()
            return None

        # Separate directories and files
        dirs = []
        files = []

        for item in all_items:
            item_path = current_path + ('/' if not current_path.endswith('/') else '') + item
            try:
                # Check if it's a directory
                os.listdir(item_path)
                dirs.append(item)
            except:
                # It's a file
                if exts:
                    for ext in exts:
                        if item.endswith(ext):
                            files.append(item)
                            break
                else:
                    files.append(item)

        # Sort and combine: directories first, then files
        dirs.sort()
        files.sort()
        items = [(d, True) for d in dirs] + [(f, False) for f in files]

        if not items:
            ui.clear()
            ui.center_text("No files found", 100, ui.COLOR_YELLOW)
            if exts:
                ext_text = ", ".join(exts)
                ui.center_text(f"Extensions: {ext_text}", 120, ui.COLOR_WHITE)
            ui.center_text("Press LEFT to go back or Q to cancel", 280, ui.COLOR_YELLOW)
            ui.wait_key_raw()
            # Don't return, allow navigation back
            if current_path != path and current_path != "/sd":
                # Go up one level
                current_path = '/'.join(current_path.rstrip('/').split('/')[:-1])
                if not current_path:
                    current_path = "/sd"
                continue
            return None

        # Selection state
        selected = 0
        scroll_offset = 0

        while True:
            ui.clear()

            # Draw title bar with current path
            ui.draw_text(title, 8, 8, ui.COLOR_WHITE)
            # Show current path (truncated if needed)
            path_display = current_path
            if len(path_display) > 38:
                path_display = "..." + path_display[-35:]
            ui.draw_text(path_display, 8, 20, ui.COLOR_CYAN)
            ui.draw_line_horizontal(32, 0, 320, ui.COLOR_WHITE)

            # Calculate visible range
            if selected < scroll_offset:
                scroll_offset = selected
            elif selected >= scroll_offset + max_visible:
                scroll_offset = selected - max_visible + 1

            # Draw file/directory list
            y_start = 40
            line_height = 16

            for i in range(max_visible):
                idx = scroll_offset + i
                if idx >= len(items):
                    break

                y = y_start + i * line_height
                is_selected = (idx == selected)

                # Get item name and type
                item_name, is_dir = items[idx]

                # Truncate long filenames
                display_name = item_name
                prefix = "[DIR] " if is_dir else ""
                max_chars = 33 if is_dir else 36
                if len(item_name) > max_chars:
                    display_name = item_name[:max_chars-3] + "..."

                ui.draw_menu_item(prefix + display_name, 8, y, is_selected)

            # Draw scroll indicator if needed
            if len(items) > max_visible:
                scroll_text = f"{selected + 1}/{len(items)}"
                ui.draw_text(scroll_text, 8, 270, ui.COLOR_CYAN)

            # Draw help text
            help_y = 290
            if mode == "manage":
                ui.draw_text("UP/DN: Nav | ENTER: Actions | RIGHT: In | Q: Exit", 8, help_y, ui.COLOR_YELLOW)
                ui.draw_text("LEFT: Out | N: New Folder", 8, help_y + 12, ui.COLOR_YELLOW)
            else:
                ui.draw_text("UP/DN: Nav | ENTER: Select | LEFT: Up | Q: Quit", 8, help_y, ui.COLOR_YELLOW)

            # Wait for input
            key = ui.wait_key_raw()

            if key == 'A':  # Up
                selected = (selected - 1) % len(items)
            elif key == 'B':  # Down
                selected = (selected + 1) % len(items)
            elif key in ('\r', '\n'):  # Enter
                item_name, is_dir = items[selected]

                if mode == "manage":
                    # In manage mode, show action menu for both files and folders
                    action = _action_menu(item_name, is_dir)

                    if action == "rename":
                        new_name = _simple_input("Rename to:", default=item_name)
                        if new_name and new_name != item_name:
                            try:
                                old_path = current_path + ('/' if not current_path.endswith('/') else '') + item_name
                                new_path = current_path + ('/' if not current_path.endswith('/') else '') + new_name
                                os.rename(old_path, new_path)
                                _show_message("Success", f"Renamed to {new_name}", ui.COLOR_GREEN, 1.0)
                                break  # Refresh listing
                            except Exception as e:
                                _show_message("Error", str(e), ui.COLOR_RED, 2.0)

                    elif action == "delete":
                        if _confirm_dialog("Delete this item?", item_name):
                            try:
                                item_path = current_path + ('/' if not current_path.endswith('/') else '') + item_name
                                if is_dir:
                                    os.rmdir(item_path)
                                else:
                                    os.remove(item_path)
                                _show_message("Success", "Item deleted", ui.COLOR_GREEN, 1.0)
                                break  # Refresh listing
                            except Exception as e:
                                _show_message("Error", str(e), ui.COLOR_RED, 2.0)

                else:
                    # Select mode
                    if is_dir:
                        # Navigate into directory
                        current_path = current_path + ('/' if not current_path.endswith('/') else '') + item_name
                        break  # Break inner loop to refresh listing
                    else:
                        # Return selected file
                        if return_full_path:
                            # Ensure proper path separator
                            if current_path.endswith('/'):
                                return current_path + item_name
                            else:
                                return current_path + '/' + item_name
                        else:
                            return item_name
            elif key == 'C' and mode == "manage":  # Right arrow - navigate into folder
                item_name, is_dir = items[selected]
                if is_dir:
                    # Navigate into directory
                    current_path = current_path + ('/' if not current_path.endswith('/') else '') + item_name
                    break  # Refresh listing
            elif key == 'D':  # Left arrow - go up one directory
                if current_path != path and current_path != "/sd":
                    # Go up one level
                    current_path = '/'.join(current_path.rstrip('/').split('/')[:-1])
                    if not current_path:
                        current_path = "/sd"
                    break  # Break inner loop to refresh listing
            elif key in ('n', 'N') and mode == "manage":  # New folder
                folder_name = _simple_input("New folder name:")
                if folder_name:
                    try:
                        new_folder_path = current_path + ('/' if not current_path.endswith('/') else '') + folder_name
                        os.mkdir(new_folder_path)
                        _show_message("Success", f"Created folder: {folder_name}", ui.COLOR_GREEN, 1.0)
                        break  # Refresh listing
                    except Exception as e:
                        _show_message("Error", str(e), ui.COLOR_RED, 2.0)
            elif key in ('q', 'Q'):  # Cancel
                return None

    return None
