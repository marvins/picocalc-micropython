#  Calculator Dependencies
from calculator.apps.main_menu import Main_Menu

class App_Runner:

    def __init__( self ):

        #  Initialize internal state parameters
        self.okay_to_run = False

        #  Add each application in app folder (start with Main Menu only)
        self.apps = { 0: Main_Menu() }

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
