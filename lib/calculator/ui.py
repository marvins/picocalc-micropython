#  Calculator Dependencies
from calculator.apps.main_menu import Main_Menu
from calculator.apps.calculator import Calculator

class App_Runner:

    def __init__( self ):

        #  Initialize internal state parameters
        self.okay_to_run = False

        # Initialize display/cursor state once
        try:
            import turtle
            turtle.init()
            try:
                from picocalc.core import display
                display.switchPredefinedLUT('vt100')
            except Exception:
                # Fall back to default LUT reset
                try:
                    from picocalc.core import display
                    display.resetLUT()
                except Exception:
                    pass
        except Exception:
            pass

        #  Add each application in app folder (Main Menu + Calculator)
        self.apps = { 0: Main_Menu(),
                      1: Calculator() }

        #  Wire runner back-reference
        for app in self.apps.values():
            app.set_runner(self)

        #  Track which app is active
        self.current_app_id = 0
        
        # Ensure initial render
        self.apps[self.current_app_id].invalidate()


    def find_apps( self ):
        pass

    def run( self ):

        self.okay_to_run = True

        while self.okay_to_run:

            #  Check for state changes

            #  Update display
            current = self.apps.get(self.current_app_id)
            if current:
                try:
                    import turtle
                    keys = turtle.check_keyboard(False)
                except Exception:
                    keys = []
                current.handle_input(keys)
                if current.is_dirty():
                    current.render()
                    current.clear_dirty()
            else:
                self.quit()

    def quit(self):
        self.okay_to_run = False

    def switch_to(self, app_id):
        # Change current app and force a full redraw on that app
        if app_id in self.apps:
            self.current_app_id = app_id
            try:
                # If the app uses a background_drawn flag, reset it
                if hasattr(self.apps[app_id], 'background_drawn'):
                    setattr(self.apps[app_id], 'background_drawn', False)
                # If the app has any selection tracking that impacts redraw, clear common ones
                if hasattr(self.apps[app_id], 'prev_selected'):
                    setattr(self.apps[app_id], 'prev_selected', None)
            except Exception:
                pass
            try:
                self.apps[app_id].invalidate()
            except Exception:
                pass
