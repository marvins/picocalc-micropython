
#  Micropython Libraries
import framebuf
import logging
import time

# PicoCalc Libraries
from picocalc.core import display, keyboard, terminal

#--------------------------------#
#-      Global Definitions      -#
#--------------------------------#
g_screen = display

class Key:
    '''
    This is a mapping of each key against it's "name"
    - Some keys use a formal name, specifically if it's not actual an ascii character
    - Some keys use a formal name, despite having an ascii character.  I don't really want space being a name
    '''

    UNKNOWN       =  'unknown'       #  This should be an error condition
    TAB           =  'tab'           #  Key:  Tab
    ENTER         =  'enter'         #  Key:  Enter / Carriage Return
    ESCAPE        =  'escape'        #  Key:  Escape / Esc
    INSERT        =  'insert'        #  Key:  Insert
    DELETE        =  'delete'        #  Key:  Delete
    END           =  'end'           #  Key:  End
    HOME          =  'home'          #  Key:  Home
    SPACE         =  'space'         #  Key:  Spacebar
    EXCLAM        =  '!'             #  Key:  Exclaimation Point / Bang
    DBL_QUOTE     =  'double_quote'  #  Key:  Double-Quote / "
    NUMBER_SIGN   =  '#'             #  Key:  Hash / Octothorpe
    DOLLAR        =  '$'             #  Key:  Dollar Sign
    PERCENT       =  '%'             #  Key:  Modulo / Percent
    AMPERSAND     =  '&'             #  Key:  Ampersand
    QUOTE         =  'single_quote'  #  Key:  Single-Quote
    PAREN_L       =  'left_paren'    #  Key:  (
    PAREN_R       =  'right_paren'   #  Key:  )
    ASTERISK      =  '*'             #  Key:  *
    PLUS          =  '+'             #  Key:  +
    COMMA         =  ','             #  Key:  ,
    MINUS         =  '-'             #  Key:  -
    PERIOD        =  '.'             #  Key:  .
    SLASH         =  'slash'         #  Key:  Slash
    DIGIT_0       =  '0'             #  Key:  Number 0
    DIGIT_1       =  '1'             #  Key:  Number 1
    DIGIT_2       =  '2'             #  Key:  Number 2
    DIGIT_3       =  '3'             #  Key:  Number 3
    DIGIT_4       =  '4'             #  Key:  Number 4
    DIGIT_5       =  '5'             #  Key:  Number 5
    DIGIT_6       =  '6'             #  Key:  Number 6
    DIGIT_7       =  '7'             #  Key:  Number 7
    DIGIT_8       =  '8'             #  Key:  Number 8
    DIGIT_9       =  '9'             #  Key:  Number 9
    COLON         =  ':'             #  Key:  Colon
    SEMICOLON     =  ';'             #
    LESS_THAN     =  '<'             #
    EQUAL         =  '='             #
    GREATER_THAN  =  '>'             #
    QUESTION      =  '?'             #
    AT            =  '@'             #
    LEFT_BRACKET  =  '['             #
    BACKSLASH     =  'backslash'     #
    RIGHT_BRACKET = ']'              #
    CARROT        = '^'              #
    UNDERSCORE    = '_'              #
    TICK          = '`'              #
    A_LOWER       = 'a'              #
    B_LOWER       = 'b'              #
    C_LOWER       = 'c'              #
    D_LOWER       = 'd'              #
    E_LOWER       = 'e'              #
    F_LOWER       = 'f'              #
    G_LOWER       = 'g'              #
    H_LOWER       = 'h'              #
    I_LOWER       = 'i'              #
    J_LOWER       = 'j'              #
    K_LOWER       = 'k'              #
    L_LOWER       = 'l'              #
    M_LOWER       = 'm'              #
    N_LOWER       = 'n'              #
    O_LOWER       = 'o'              #
    P_LOWER       = 'p'              #
    Q_LOWER       = 'q'              #
    R_LOWER       = 'r'              #
    S_LOWER       = 's'              #
    T_LOWER       = 't'              #
    U_LOWER       = 'u'              #
    V_LOWER       = 'v'              #
    W_LOWER       = 'w'              #
    X_LOWER       = 'x'              #
    Y_LOWER       = 'y'              #
    Z_LOWER       = 'z'              #
    A_UPPER       = 'A'              #
    B_UPPER       = 'B'              #
    C_UPPER       = 'C'              #
    D_UPPER       = 'D'              #
    E_UPPER       = 'E'              #
    F_UPPER       = 'F'              #
    G_UPPER       = 'G'              #
    H_UPPER       = 'H'              #
    I_UPPER       = 'I'              #
    J_UPPER       = 'J'              #
    K_UPPER       = 'K'              #
    L_UPPER       = 'L'              #
    M_UPPER       = 'M'              #
    N_UPPER       = 'N'              #
    O_UPPER       = 'O'              #
    P_UPPER       = 'P'              #
    Q_UPPER       = 'Q'              #
    R_UPPER       = 'R'              #
    S_UPPER       = 'S'              #
    T_UPPER       = 'T'              #
    U_UPPER       = 'U'              #
    V_UPPER       = 'V'              #
    W_UPPER       = 'W'              #
    X_UPPER       = 'X'              #
    Y_UPPER       = 'Y'              #
    Z_UPPER       = 'Z'              #
    LEFT_BRACE   =  '{'              #
    PIPE          =  '|'             #
    RIGHT_BRACE  =  '}'              #
    TILDE        =  '~'              #
    BACKSPACE    =  'backspace'      #
    F1           =  'F1'             #
    F2           =  'F2'             #
    F3           =  'F3'             #
    F4           =  'F4'             #
    F5           =  'F5'             #
    F6           =  'F6'             #
    F7           =  'F7'             #
    F8           =  'F8'             #
    F9           =  'F9'             #
    F10          =  'F10'            #
    CAPS_LOCK    =  'capslock'       #
    BREAK        =  'break'
    LEFT_ARROW   =  'left_arrow'
    RIGHT_ARROW  =  'right_arrow'
    UP_ARROW     =  'up_arrow'
    DOWN_ARROW   =  'down_arrow'

    @staticmethod
    def to_key( k ):

        value = None
        try:
            value = KEYMAP[k]
        except Exception:
            return Key.UNKNOWN
        return value

#  This provides a mapping between each key, and the ioctl values
#  which map.  Some of these are straight ASCII, whereas others are
#  more complex.
KEYMAP = { Key.UNKNOWN       : (   0, ) ,
           Key.TAB           : (   9, ) ,
           Key.ENTER         : (  13, ) ,
           Key.ESCAPE        : (  27,  27 ) ,             # Key:  Escape key
           Key.INSERT        : (  27,  73 ) ,             # Key:  Insert
           Key.DELETE        : (  27,  91,  51, 126 ) ,   # Key:  Delete
           Key.UP_ARROW      : (  27,  91,  65 ) ,        # Key:  Up Arrow
           Key.DOWN_ARROW    : (  27,  91,  66 ) ,        # Key:  Down Arrow
           Key.RIGHT_ARROW   : (  27,  91,  67 ) ,        # Key:  Right Arrow Key
           Key.LEFT_ARROW    : (  27,  91,  68 ) ,        # Key:  Left Arrow Key
           Key.END           : (  27,  91,  70 ) ,        # Key:  End
           Key.HOME          : (  27,  91,  72 ) ,        # Key:  Home
           Key.SPACE         : (  32, ) ,                 # Key:  " " (Spacebar)
           Key.EXCLAM        : (  33, ) ,                 # Key:  !   (Exclaimation-Point)
           Key.DBL_QUOTE     : (  34, ) ,                 # Key:  "   (Double-Quote)
           Key.NUMBER_SIGN   : (  35, ) ,                 # Key:  #   (Octothorpe)
           Key.DOLLAR        : (  36, ) ,                 # Key:  $   (Dollar-Sign)
           Key.PERCENT       : (  37, ) ,                 # Key:  %   (Percent)
           Key.AMPERSAND     : (  38, ) ,                 # Key:  &   (Ampersand)
           Key.QUOTE         : (  39, ) ,                # Key:  '   (Single-Quote)
           Key.PAREN_L       : (  40, ) ,                # Key:  (   (Left-Parenthesis)
           Key.PAREN_R       : (  41, ) ,                # Key:  )   (Right-Parenthesis)
           Key.ASTERISK      : (  42, ) ,                # Key:  *   (Star / Multiply)
           Key.PLUS          : (  43, ) ,                # Key:  +   (Plus-Sign)
           Key.COMMA         : (  44, ) ,                # Key:  ,   (Comma)
           Key.MINUS         : (  45, ) ,                # Key:  -   (Minus)
           Key.PERIOD        : (  46, ) ,                # Key:  .   (Period)
           Key.SLASH         : (  47, ) ,                # Key:
           Key.DIGIT_1       : (  49, ) ,                # Key:
           Key.DIGIT_0       : (  48, ) ,                # Key:
           Key.DIGIT_2       : (  50, ) ,                # Key:
           Key.DIGIT_3       : (  51, ) ,                # Key:
           Key.DIGIT_4       : (  52, ) ,                # Key:
           Key.DIGIT_5       : (  53, ) ,                # Key:
           Key.DIGIT_6       : (  54, ) ,                # Key:
           Key.DIGIT_7       : (  55, ) ,                # Key:
           Key.DIGIT_8       : (  56, ) ,                # Key:
           Key.DIGIT_9       : (  57, ) ,                # Key:
           Key.COLON         : (  58, ) ,                # Key:
           Key.SEMICOLON     : (  59, ) ,                # Key:
           Key.LESS_THAN     : (  60, ) ,                # Key:  < (Left Angle-Bracket)
           Key.EQUAL         : (  61, ) ,                # Key:  = (Equal Sign)
           Key.GREATER_THAN  : (  62, ) ,                # Key:  > (Right Angle-Bracket)
           Key.QUESTION      : (  63, ) ,                # Key:
           Key.AT            : (  64, ) ,                # Key:
           Key.A_UPPER       : (  65, ) ,
           Key.B_UPPER       : (  66, ) ,
           Key.C_UPPER       : (  67, ) ,
           Key.D_UPPER       : (  68, ) ,
           Key.E_UPPER       : (  69, ) ,
           Key.F_UPPER       : (  70, ) ,
           Key.G_UPPER       : (  71, ) ,
           Key.H_UPPER       : (  72, ) ,
           Key.I_UPPER       : (  73, ) ,
           Key.J_UPPER       : (  74, ) ,
           Key.K_UPPER       : (  75, ) ,
           Key.L_UPPER       : (  76, ) ,
           Key.M_UPPER       : (  77, ) ,
           Key.N_UPPER       : (  78, ) ,
           Key.O_UPPER       : (  79, ) ,
           Key.P_UPPER       : (  80, ) ,
           Key.Q_UPPER       : (  81, ) ,
           Key.R_UPPER       : (  82, ) ,
           Key.S_UPPER       : (  83, ) ,
           Key.T_UPPER       : (  84, ) ,
           Key.U_UPPER       : (  85, ) ,
           Key.V_UPPER       : (  86, ) ,
           Key.W_UPPER       : (  87, ) ,
           Key.X_UPPER       : (  88, ) ,
           Key.Y_UPPER       : (  89, ) ,
           Key.Z_UPPER       : (  90, ) ,
           Key.LEFT_BRACKET  : (  91, ) ,                # Key:
           Key.BACKSLASH     : (  92, ) ,                # Key:
           Key.RIGHT_BRACKET : (  93, ) ,                # Key: ] (Right-Bracket)
           Key.CARROT        : (  94, ) ,                # Key: ^ (Carrot)
           Key.UNDERSCORE    : (  95, ) ,                # Key:
           Key.TICK          : (  96, ) ,                # Key:
           Key.A_LOWER       : (  97, ) ,
           Key.B_LOWER       : (  98, ) ,
           Key.C_LOWER       : (  99, ) ,
           Key.D_LOWER       : ( 100, ) ,
           Key.E_LOWER       : ( 101, ) ,
           Key.F_LOWER       : ( 102, ) ,
           Key.G_LOWER       : ( 103, ) ,
           Key.H_LOWER       : ( 104, ) ,
           Key.I_LOWER       : ( 105, ) ,
           Key.J_LOWER       : ( 106, ) ,
           Key.K_LOWER       : ( 107, ) ,
           Key.L_LOWER       : ( 108, ) ,
           Key.M_LOWER       : ( 109, ) ,
           Key.N_LOWER       : ( 110, ) ,
           Key.O_LOWER       : ( 111, ) ,
           Key.P_LOWER       : ( 112, ) ,
           Key.Q_LOWER       : ( 113, ) ,
           Key.R_LOWER       : ( 114, ) ,
           Key.S_LOWER       : ( 115, ) ,
           Key.T_LOWER       : ( 116, ) ,
           Key.U_LOWER       : ( 117, ) ,
           Key.V_LOWER       : ( 118, ) ,
           Key.W_LOWER       : ( 119, ) ,
           Key.X_LOWER       : ( 120, ) ,
           Key.Y_LOWER       : ( 121, ) ,
           Key.Z_LOWER       : ( 122, ) ,
           Key.LEFT_BRACE    : ( 123, ) ,                # Key: { (Left-Squigly-Brace)
           Key.PIPE          : ( 124, ) ,                # Key:
           Key.RIGHT_BRACE   : ( 125, ) ,                # Key:
           Key.TILDE         : ( 126, ) ,                # Key:
           Key.BACKSPACE     : ( 127, ) ,                # Key:
           Key.F1            : ( 129, ) ,                # Key:
           Key.F2            : ( 130, ) ,                # Key:
           Key.F3            : ( 131, ) ,                # Key:
           Key.F4            : ( 132, ) ,                # Key:
           Key.F5            : ( 133, ) ,                # Key:
           Key.F6            : ( 134, ) ,                # Key:
           Key.F7            : ( 135, ) ,                # Key:
           Key.F8            : ( 136, ) ,                # Key:
           Key.F9            : ( 137, ) ,                # Key:
           Key.F10           : ( 144, ) ,                # Key:
           Key.CAPS_LOCK     : ( 193, ) ,                # Key:
           Key.BREAK         : ( 208, )                  # Key:
}

class Keyboard:
    '''
    Contains methods for querying keys.
    '''

    @staticmethod
    def is_lowercase_letter( key ):
        return key >= 97 and key <= 122

    @staticmethod
    def is_uppercase_letter( key ):
        return key >= 65 and key <= 90

    @staticmethod
    def is_number( key ):
        return key >= 48 and key <= 57


    @staticmethod
    def is_letter( key ):
        return Keyboard.is_uppercase_letter( key ) or Keyboard.is_lowercase_letter( key )

    @staticmethod
    def is_char( key ):
        if Key.is_letter( key ):
            return True
        return False

    def get_char( value ):
        '''
        Match the value against the table
        '''
        for key in KEYMAP.keys():
            if KEYMAP[key] == value:
                return key
        return None

    @staticmethod
    def name( value ):
        for key_type in dir(Key):
            if 'Key_' in str(key_type):
                if getattr(Key, str(key_type)) == value:
                    return key_type
        if Key.is_char():
            return chr(value)

    @staticmethod
    def pop_next( arr ):
        '''
        Given an array, pop the next key off, returning the key and the remainder of the array
        '''

        #  We only pop off one item at a time, so remaining items will be returned
        arr = list(arr)
        current = []

        while len( arr ) > 0:

            #  Get next entry from ioctl
            current.append( arr.pop(0) )

            #  Convert to tuple so we can compare against KEYMAP
            temp = tuple(current)

            #  Check value
            key = Keyboard.get_char( temp )

            if key is None:
                continue
            return key, arr

        return 'UNKNOWN[' + str(temp) + ']', arr


class TurtleScreen:

    def __init__(self):

        terminal.wr("\x1b[?25l")  # hide cursor
        terminal.stopRefresh()

    def reset( self ):
        '''
        This was lifted from the refresh.py example.
        Basically, put things back the way we found them.

        @todo:  Actually capture original values from init calls
                so it's actually a reset call.
        '''
        terminal.recoverRefresh()
        display.fill(0)
        display.resetLUT()
        terminal.wr("\x1b[2J\x1b[H")#move the cursor to the top, and clear the terminal buffer
        terminal.wr("\x1b[?25h")  # show cursor

    def wait_update_finished( self, max_iters = 1000 ):

        #  Make sure we are still not drawing
        counter = 0
        while display.isScreenUpdateDone():
            time.sleep(0.1)
            counter += 1
            if not max_iters is None:
                if counter >= max_iters:
                    logging.error( 'Screen update never finished')
                    break

        return

    def fill( self, color ):
        display.fill( color )
        display.show()

    def fill_rect( self, x, y, w, h, color ):
        display.fill_rect( x, y, w, h, color )

    def draw_line( self, x1, y1, x2, y2, color ):
        '''
        Draw a line from P1 (x1,y1) to P2 (x2,y2)
        '''
        if color is None:
            color = 15
        display.line( x1, y1, x2, y2, color )
        display.show()

    def draw_rect( self, x, y, w, h, c=None, line_color=None ):
        if c is None and not (line_color is None):
            c = line_color
        if c is None:
            c = 15
        display.rect( x, y, w, h, c )
        display.show()

    def draw_text( self, text, x, y, color=None ):
        if color is None:
            color = 15
        display.text( text, x, y, color )
        display.show()

    def show( self ):
        display.show()

    def log_info(self):

        print(display.getLUT())

def screensize():
    return (320,320)

def init():
    global g_screen
    g_screen = TurtleScreen()
    return g_screen

def reset():

    a = init()
    a.reset()

def fill( color ):
    display.fill( color )
    display.show()

def fill_rect( x, y, w, h, color ):
    display.fill_rect( x, y, w, h, color )
    display.show()

def draw_line( x1, y1, x2, y2, color=None ):
    if color is None:
        color = 15
    display.line( x1, y1, x2, y2, color )
    display.show()

def draw_rect( x, y, w, h, line_color=None ):
    c = 15 if line_color is None else line_color
    display.rect( x, y, w, h, c )
    display.show()

def draw_text( text, x, y, color=None ):
    if color is None:
        color = 15
    display.text( text, x, y, color )
    display.show()

def check_keyboard( verbose = False ):

    output = []
    temp = bytearray(1)
    while keyboard.readinto(temp):
        output.append( temp[0] )

    #  Log keyboard input
    if verbose:
        print( 'Keys Read: ', output )

    # Try to discern specific keys
    keys = []
    while len( output ) > 0:
        (k, output) = Keyboard.pop_next( output )
        keys.append( k )

    return keys
