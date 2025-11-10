


class App_Base:

    def __init__( self ):
        self.runner = None
        self.dirty = False


    def render( self ):

        self.render_header()
        self.render_body()
        self.render_footer()

    def render_header( self ):
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

