
#  Micropython Libraries
import logging
import os
import sys
import time

#  Project Libraries
from colorer import Back
import picocalc.colors as pcolors
import turtle

class Folder:

    def __init__(self, cdir):
        self.cdir = cdir

        self.contents = []

        # Get the contents
        entries = os.listdir( self.cdir )
        for e in entries:

          #  Get file type
          tp = 2
          
          if os.path.isdir( e ):
            tp = 1

          self.contents.append( Node( self.cdir,
                                      e,
                                      tp ) )

    def current_path( self ):
        return self.cdir

    def navigate_info( self, selected ):

        #  If the selected is the back item
        self.cdir = self.cdir + '/' + self.contents[selected]

class State:
    '''
    Manages prmary state variables independent of the UI.
    '''

    def __init__(self, cdir):

        self.screen  = None

        self.header  = True
        self.entries = True

        self.selected = 0

        #  Other settings
        self.start_drawing_row = 50
        self.end_drawing_row   = 300
        self.text_row_height   = 20

        #  Get the contents of the current folder
        self.folder = Folder( cdir )

    def get_selected( self ):
        '''
        '''
        return self.folder.contents[self.selected]

    def notify_update( self, draw_type ):

        if draw_type == 'full':
            self.header = True

        if draw_type == 'full' or draw_type == 'entries':
            self.entries = True

    def draw_background( self ):

        #  Full Redraw
        if self.entries:
            self.screen.fill_rect( 10, 10, 300, 300,
                                   pcolors.GS4.GRAY )

    def draw_entries( self ):

        #  Only update if we can draw it
        if self.entries:
            cnt = 0
            for x in range( self.start_drawing_row,
                            self.end_drawing_row,
                            self.text_row_height ):

                file_list = self.folder.contents

                if cnt < len(file_list):

                    file_path = file_list[cnt].path
                    file_type = file_list[cnt].node_type

                    if file_type == 1:
                        file_path += '/'

                    if self.selected == cnt:
                        self.screen.draw_rect(  20, x - 9,
                                               280,    18,
                                               pcolors.GS4.BLUE )

                    self.screen.draw_text( f'{file_path}',
                                           20, x,
                                           pcolors.GS4.CYAN )

                cnt += 1
                self.entries = False

    def draw_footer( self ):

        # Draw Footer
        self.screen.fill_rect(   0, 300,
                               320,  20,
                              pcolors.GS4.LIGHT_GRAY )

        self.screen.draw_text( '{}'.format( self.folder.current_path() ),
                               20, 320,
                               pcolors.GS4.LIGHT_GRAY )

class Node:

    def __init__( self, dname, path, node_type ):
        '''
        node_type = 1=folder, 2=file
        '''
        self.dname     = dname
        self.path      = path
        self.node_type = node_type

def run_full( cdir = '.', log_level = logging.DEBUG, log_path = './browser.log' ):

    #  Setup Logger
    if not log_path is None:
        logging.basicConfig( level    = log_level,
                             filename = log_path )
    else:
        logging.basicConfig( level = log_level )
    logging.info( 'Logging initialized' )

    #  Drawing State
    state = State( cdir )

    #  Setup the Turtle Display
    state.screen = turtle.init()
    state.screen.fill( pcolors.GS4.BLACK )
    state.screen.wait_update_finished()

    stime = time.time()


    okay_to_run = True
    while okay_to_run:

        state.draw_background()

        #  Populate Header
        state.screen.draw_text( "PicoCalc Filesystem Browser",
                                10, 20, pcolors.GS4.GREEN )
        state.screen.wait_update_finished()

        #  Get content
        state.draw_footer()
        state.draw_entries()

        # Check for keyboard input
        keys = turtle.check_keyboard()

        for key in keys:
            if key == turtle.Key.ESCAPE:
                state.screen.fill( pcolors.GS4.BLACK )
                state.screen.draw_text("Exiting!", 10, 310, pcolors.GS4.GREEN )
                okay_to_run = False
                break

            elif key == turtle.Key.DOWN_ARROW:
                state.selected = ( state.selected + 1 ) % len( state.folder.contents )
                state.notify_update( draw_type = 'entries' )

            elif key == turtle.Key.UP_ARROW:
                if state.selected == 0:
                    state.selected = len( state.folder.contents ) - 1
                else:
                    state.selected -= 1
                state.notify_update( draw_type = 'entries' )


            elif key == turtle.Key.ENTER:

                #  If the selected value is a folder (ie: 1), navigate inside
                if state.get_selected().node_type == 1:

                    state.folder.navigate_into(state.selected)
                    state.notify_update( draw_type = 'full' )

        time.sleep(0.1)

        if (time.time() - stime) > 20:
            okay_to_run = False

    #  Put everything back
    state.screen.reset()

    logging.debug( 'Exiting Application' )


#----------------------------------------#
#-          Run The Application         -#
#----------------------------------------#
def file_browser( cdir      = '.',
                  log_level = logging.DEBUG,
                  log_path  = './browser.log'  ):

    try:
        run_full( cdir, log_level, log_path )

    except Exception as e:
        turtle.reset()
        print('EXCEPTION')
        sys.print_exception( e )
        logging.error( 'Exception caught: {}'.format(e) )
        sys.print_exception( e )

