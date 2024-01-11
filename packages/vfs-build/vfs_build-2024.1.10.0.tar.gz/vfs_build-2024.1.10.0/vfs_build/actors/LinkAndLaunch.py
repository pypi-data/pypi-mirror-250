from .Command import Command
from .Actor import Actor
from .Link import Link

class LinkAndLaunch( Actor ):
    def on_start( self, sources: list[ str ] ):
        self.launch( self.on_link, Link(), 'exe', sources )

    def on_link( self, executable ):
        self.launch( self.on_end, Command(), executable, check_return_code = False )

    def is_idempotent( self ):
        return False
