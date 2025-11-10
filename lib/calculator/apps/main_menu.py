 
from calculator.apps.app_base import App_Base
from picocalc.colors import RGB_VT100, RGB_565
import turtle

class Main_Menu( App_Base ):

    def __init__(self):
        super().__init__()
        self.selected = 0  # 0 = Calculator, 1 = Exit
        self.prev_selected = None
        self.items = [
            { 'name': 'Calc' },
            { 'name': 'Exit' }
        ]
        self.icon_w = 80
        self.icon_h = 80
        self.icon_y = 100
        self.icon_xs = [ 40, 200 ]  # positions for two icons
        self.background_drawn = False

    def render_body(self):
        # First-time full redraw with light background
        if not self.background_drawn:
            try:
                turtle.fill(RGB_565.LIGHT_GRAY)
            except Exception:
                try:
                    turtle.fill(0)
                except Exception:
                    pass
            indices = [0, 1]
            self.background_drawn = True
        else:
            # Determine which icons to redraw to avoid full-screen flicker
            if self.prev_selected is None or self.prev_selected == self.selected:
                indices = [0, 1]
            else:
                indices = [self.prev_selected, self.selected]

        for idx in indices:
            item = self.items[idx]
            x = self.icon_xs[idx]
            y = self.icon_y
            # Use RGB_565 for primitives (rectangles/fills)
            border_color = RGB_565.BRIGHT_YELLOW if idx == self.selected else RGB_565.DARK_GRAY
            fill_color = RGB_565.BRIGHT_BLUE if idx == self.selected else RGB_565.BLACK

            turtle.draw_rect(x, y, self.icon_w, self.icon_h, line_color=border_color)
            turtle.fill_rect(x+1, y+1, self.icon_w-2, self.icon_h-2, fill_color)

            # Draw label inside the icon (approx centered)
            label = item['name']
            text_x = x + (self.icon_w // 2) - 16
            text_y = y + (self.icon_h // 2) - 4
            turtle.draw_text(label, text_x, text_y, RGB_VT100.WHITE)

    def handle_input(self, keys):
        if not keys:
            return
        for k in keys:
            if k == 'left_arrow':
                old = self.selected
                self.selected = (self.selected - 1) % len(self.items)
                self.prev_selected = old
                self.invalidate()
            elif k == 'right_arrow':
                old = self.selected
                self.selected = (self.selected + 1) % len(self.items)
                self.prev_selected = old
                self.invalidate()
            elif k == 'enter':
                if self.selected == 1:  # Exit
                    if self.runner:
                        self.runner.quit()
                # Placeholder for Calculator selection; no-op for now

