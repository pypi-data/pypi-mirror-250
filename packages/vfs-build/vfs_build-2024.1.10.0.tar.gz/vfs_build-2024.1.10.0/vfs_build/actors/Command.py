from .Actor import Actor
import subprocess
import sys

class Command( Actor ):
    def on_start( self, cmd_args: list[ str ], cwd = None, check_return_code = True ) -> None:
        # print( cmd_args )
        cp = subprocess.run( cmd_args, cwd = cwd )

        if check_return_code:
            if cp.returncode:
                sys.exit( cp.returncode )
            self.on_end()
        else:
            self.on_end( cp.returncode )

    def is_idempotent( self ):
        return False
