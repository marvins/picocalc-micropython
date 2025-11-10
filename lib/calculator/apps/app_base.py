
from picocalc.colors import RGB_565, RGB_VT100, GS4
import turtle
from calculator.utilities.gui_utilities import draw_battery_status
import battery as _battery
try:
    from picocalc.core import keyboard as _pc_keyboard
except Exception:
    _pc_keyboard = None

# Layout constants
HEADER_H = 24
FOOTER_H = 24


class App_Base:

    def __init__( self ):
        self.runner = None
        self.dirty = False
        self.title = "Window"


    def render( self ):

        self.render_header()
        self.render_body()
        self.render_footer()

    def render_header( self ):
        try:
            w, h = turtle.screensize()
        except Exception:
            w, h = (320, 320)

        # Background bar
        try:
            turtle.fill_rect(0, 0, w, HEADER_H, GS4.LIGHT_GRAY)
        except Exception:
            try:
                turtle.draw_rect(0, 0, w, HEADER_H, line_color=GS4.LIGHT_GRAY)
            except Exception:
                pass

        # Title text (left)
        try:
            turtle.draw_text(self.title, 6, 6, RGB_VT100.WHITE)
        except Exception:
            pass

        # Battery (right)
        try:
            # Prefer hardware-level reading from picocalc.core (level 0-127; charging flag)
            battery_status = None
            if _pc_keyboard is not None:
                hw = _pc_keyboard.battery_status()
                level = hw.get('level', 0)
                charging = hw.get('charging', False)
                # Map 0..127 to 0..100
                percentage = int((min(max(level, 0), 127) * 100) / 127)
                battery_status = { 'percentage': percentage,
                                   'usb_power': charging }
            else:
                # Fallback to voltage-based module if available
                battery_status = _battery.get_status()

            # place about ~90px from right edge
            draw_battery_status(w - 90, 6, battery_status,
                                icon_color=GS4.CYAN,
                                text_color=RGB_VT100.BRIGHT_GREEN)
        except Exception:
            pass

    def render_body( self ):
        pass


    def render_footer( self ):
        pass

    def set_runner(self, runner):
        self.runner = runner

    def handle_input(self, keys):
        pass

    def invalidate(self):
        self.dirty = True

    def clear_dirty(self):
        self.dirty = False

    def is_dirty(self):
        return self.dirty

