from ..support.import_source_file import import_source_file
import sys
import os

class Actor:
    def __init__( self, desactivated_options = None ) -> None:
        self.desactivated_options = desactivated_options or []
        self._seen_build_configs = {}
        self._output_files = {}
        self._input_files = {}

        # attributes filled by ActorSystem
        self._dependancy_file = None
        self._parameter_repr = None
        self.actor_system = None
        self.options = None
        self.end_cb = None
        self.parent = None

    def on_end( self, *args, **kwargs ):
        # save output
        self.actor_system._save_cache( self, args, kwargs )

        # next callback
        self.end_cb( *args, **kwargs )

    def launch( self, cb, actor, *args, **kwargs ):
        return self.actor_system.launch( self, cb, actor, *args, **kwargs )

    def is_idempotent( self ):
        return True

    def parents( self ):
        res = [ self ]
        while res[ -1 ].parent:
            res.append( res[ -1 ].parent )
        return res
    
    def short_name( self, *args, **kwargs ):
        def try_to_add_arg( res ):
            for arg in args:
                if type( arg ) == str:
                    arg = arg[ arg.rfind( '/' ) + 1 : ]
                    p = arg.find( '.' )
                    if p >= 0:
                        arg = arg[ : p ]
                    return res + "." + arg
            return res

        return try_to_add_arg( type( self ).__name__ )

    # --------------------------------------------------------------------------------
    def make_output_filename( self, ext, stem, sub_dirs = [] ) -> str:
        # make name
        if o := self.options[ "output" ]:
            # if output is specified in options
            os.makedirs( os.path.parent( os.abspath( o.value ) ), exist_ok = True )
            res = os.abspath( o.value )
        else:
            # else, use self.options.build_dir( ... )
            dep_name, _ = os.path.splitext( os.path.basename( self._dependancy_file ) )
            name = f"{ stem }.{ dep_name }.{ ext }"
            res = os.path.abspath( os.path.join( self.options.build_dir( *sub_dirs ), name ) )
        
        self._output_files[ res ] = 0
        return res

    def add_source_dep( self, source: str ):
        self.load_config_from( source )
        self.check_file( source )

    def load_config_from( self, source: str ):
        while True:
            source, tail = os.path.split( source )

            f = os.path.abspath( os.path.join( source, "vfs_build_config.py" ) )
            if f in self._seen_build_configs:
                break
            self._seen_build_configs[ f ] = True

            if self.check_file( f ):
                self.options.cwd = os.path.abspath( source )
                module = import_source_file( f )
                module.config( self.options )

            if not tail:
                break

    def check_file( self, source: str ):
        # if it exists
        source = os.path.abspath( source )
        if os.path.exists( source ):
            for p in self.parents():
                p._input_files[ source ] = os.path.getmtime( source )
            return True
        
        # else
        for p in self.parents():
            p._input_files[ source ] = -1
        return False

    def relative_name( self, filename: str ):
        try:
            return os.path.relpath( os.path.abspath( filename ) )
        except ValueError:
            return filename

    # --------------------------------------------------------------------------------
    def info( self, msg ):
        def prLightGray( skk ):
            print( "\033[38;5;242m{}\033[00m" .format( skk ) )
        prLightGray( msg )

    def error( self, msg ):
        print( msg, file = sys.stderr )
        sys.exit( 1 )

