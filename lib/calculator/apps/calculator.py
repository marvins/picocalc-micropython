from calculator.apps.app_base import App_Base
from picocalc.colors import RGB_VT100, RGB_565, GS4
import turtle


class Calculator(App_Base):

    def __init__(self):
        super().__init__()
        self.title = "Calculator"
        self.background_drawn = False
        self.modal_id = None  # None or 1..5 for F1..F5

    def render_body(self):
        if not self.background_drawn:
            # Fill only the body area below header
            try:
                w, h = turtle.screensize()
            except Exception:
                w, h = (320, 320)
            header_h = 24
            body_y = header_h
            body_h = h - body_y
            try:
                turtle.fill_rect(0, body_y, w, body_h, GS4.LIGHT_GRAY)
            except Exception:
                try:
                    turtle.fill(0)
                except Exception:
                    pass
            self.background_drawn = True

        # Draw two stacked panes: history (top) and console (bottom)
        try:
            w, h = turtle.screensize()
        except Exception:
            w, h = (320, 320)
        header_h = 24
        footer_h = 24
        body_x = 0
        body_y = header_h
        body_w = w
        body_h = h - header_h - footer_h

        # Split ratio: 60% history top, 40% console bottom
        history_h = (body_h * 3) // 5
        console_h = body_h - history_h

        inset = 3
        # History box
        hist_x = body_x + inset
        hist_y = body_y + inset
        hist_w = body_w - 2 * inset
        hist_h = history_h - 2 * inset

        # Console box
        cons_x = body_x + inset
        cons_y = body_y + history_h + inset
        cons_w = body_w - 2 * inset
        cons_h = console_h - 2 * inset

        # Draw helper: 2px black border + white fill
        def draw_box(x, y, w_, h_):
            if w_ <= 6 or h_ <= 6:
                return
            try:
                turtle.draw_rect(x, y, w_, h_, line_color=GS4.BLACK)
                turtle.draw_rect(x+1, y+1, w_-2, h_-2, line_color=GS4.BLACK)
                # white-like fill in GS4 is LIGHT_GRAY
                turtle.fill_rect(x+2, y+2, w_-4, h_-4, GS4.LIGHT_GRAY)
            except Exception:
                pass

        draw_box(hist_x, hist_y, hist_w, hist_h)
        draw_box(cons_x, cons_y, cons_w, cons_h)

        # Render modal popup if active
        if self.modal_id is not None:
            mw = body_w - 40
            mh = body_h - 60
            mx = (w - mw) // 2
            my = header_h + (body_h - mh) // 2
            draw_box(mx, my, mw, mh)
            # Title inside modal
            try:
                turtle.draw_text(f"F{self.modal_id} Panel", mx + 8, my + 8, RGB_VT100.WHITE)
            except Exception:
                pass

        # Draw centered text box over the body area with 3px inset and 2px black border
        try:
            w, h = turtle.screensize()
        except Exception:
            w, h = (320, 320)
        header_h = 24
        footer_h = 24
        body_x = 0
        body_y = header_h
        body_w = w
        body_h = h - header_h  # footer is drawn on top; we still reserve visual space

        inset = 3
        box_x = body_x + inset
        box_y = body_y + inset
        box_w = body_w - 2 * inset
        box_h = body_h - 2 * inset - footer_h  # keep space for footer

        if box_w > 6 and box_h > 6:
            # Border 2px: draw two rectangles
            try:
                turtle.draw_rect(box_x, box_y, box_w, box_h, line_color=RGB_565.BLACK)
                turtle.draw_rect(box_x + 1, box_y + 1, box_w - 2, box_h - 2, line_color=RGB_565.BLACK)
                # Fill interior white
                turtle.fill_rect(box_x + 2, box_y + 2, box_w - 4, box_h - 4, RGB_565.WHITE)
            except Exception:
                pass

    def render_footer(self):
        try:
            w, h = turtle.screensize()
        except Exception:
            w, h = (320, 320)

        footer_h = 24
        y = h - footer_h

        try:
            turtle.fill_rect(0, y, w, footer_h, RGB_565.DARK_GRAY)
        except Exception:
            try:
                turtle.draw_rect(0, y, w, footer_h, line_color=RGB_565.DARK_GRAY)
            except Exception:
                pass

        labels = ["ESC", "F1", "F2", "F3", "F4", "F5"]
        btn_w = w // len(labels)
        btn_h = footer_h - 4
        btn_y = y + 2

        for i, label in enumerate(labels):
            x = i * btn_w + 2
            w_inner = btn_w - 4
            try:
                turtle.draw_rect(x, btn_y, w_inner, btn_h, line_color=RGB_565.LIGHT_GRAY)
                turtle.fill_rect(x+1, btn_y+1, w_inner-2, btn_h-2, RGB_565.BLACK)
                # crude center: place text a bit inside
                tx = x + (w_inner // 2) - 8
                ty = btn_y + (btn_h // 2) - 4
                turtle.draw_text(label, tx, ty, RGB_VT100.WHITE)
            except Exception:
                pass

    def handle_input(self, keys):
        if not keys:
            return
        for k in keys:
            if k == 'escape':
                # If modal is open, close it; else return to Main Menu
                if self.modal_id is not None:
                    self.modal_id = None
                    self.invalidate()
                else:
                    if self.runner:
                        self.runner.switch_to(0)

            elif k in ('F1','F2','F3','F4','F5'):
                idx = int(k[1])  # 1..5
                if self.modal_id == idx:
                    # toggle off
                    self.modal_id = None
                else:
                    # switch to new modal
                    self.modal_id = idx
                self.invalidate()
