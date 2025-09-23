
def assert_true( value ):
    if not value:
        raise Exception( f'Input not true.' )

def assert_false( value ):
    if value:
        raise Exception( f'Input not false' )

