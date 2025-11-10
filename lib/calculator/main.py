
from calculator.ui import App_Runner
import sys
import turtle


def main_app():

    #  Build the main application
    app = App_Runner()

    #  Launch
    app.run()


def main():

    try:
        main_app()
    except Exception as e:
        try:
            f = open('error.log', 'a')
            f.write('--- APPLICATION CRASH ---\n')
            sys.print_exception(e, f)
            f.write('\n')
            f.close()
        except Exception as _:
            # Fallback to console if file write fails
            sys.print_exception(e)
        # Attempt to reset display to neutral state
        try:
            turtle.reset()
        except Exception:
            pass

if __name__ == "__main__":
    main()
