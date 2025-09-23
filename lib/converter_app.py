#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#*                                                                                    *#
#*                           Copyright (c) 2025 Terminus LLC                          *#
#*                                                                                    *#
#*                                All Rights Reserved.                                *#
#*                                                                                    *#
#*          Use of this source code is governed by LICENSE in the repo root.          *#
#*                                                                                    *#
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#

#  Python Libraries
import time

#  Project Libraries
import turtle

from ui import Button, Check_Box, HBoxLayout, Header, Label, Page, Text_Input, VBoxLayout

#  Configuration Values
max_loops = 20

def build_main_menu():

    page = Page()

    #  Add Header
    #page.add_widget( Header( title = 'Converter',
    #                         show_time = True ) )

    #  Add Labels for options
    #page.add_widget( Button( title   = '1) Coordinate Conversions',
    #                         hotkey  = '1',
    #                         retcode = 'coord' ) )
    #page.add_widget( Button( title = '2) Time Conversions' ) )

    return page

def main_menu():

    start_time = time.time()
    try:
        turtle.init()
        page = build_main_menu()

        #  Run Primary Menu
        exit_app = False
        while not exit_app:

            #  Draw the UI
            page.draw()

            #  Check keyboard input
            #action = page.check_keyboard()

            #if not action is None:
            #    if action == 'exit':
            #        exit_app = True
            #        break
            #    elif action == 'coord':
            #        page.draw( force_draw=True )
            #else:
            #    sleep(0.1)

            time.sleep(5)

    except Exception as e:
        print( e )

    #finally:
    #    turtle.reset()

