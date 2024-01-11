from ..support.Optionnal import Optionnal
from threading import Lock
from pathlib import Path
import subprocess
import sys
import os

load_lock = Lock()

class Options:
    def __init__( self, parent = None, desactivated_options: list[str] = None ) -> None:
        self.desactivated_options = desactivated_options or [] # notably for options defined in parent(s)
        self.extra_args = []
        self.options = [] # list of tuple( name, value )
        self.parent = parent

        # cached variables
        self.cpp_compiler_ = None
        self.build_dir_ = None

        # context
        self.cwd = None

    def parents( self ):
        """ recursive list of parents including self """
        res = []
        p = self
        while p is not None:
            res.append( p )
            p = p.parent
        return res

    def cwd_parent( self, n ):
        p = self.cwd
        for i in range( n ):
            p = os.path.dirname( p )
        return p

    def __getitem__( self, option_name: str ) -> Optionnal:
        """ get first appearance of option by name """
        
        for p in self.parents():
            for option in p.options:
                if option[ 0 ] == option_name:
                    return Optionnal( option[ 1 ] )
            if option_name in p.desactivated_options:
                return Optionnal()
        return Optionnal()

    def all_the_options( self ):
        """ recursive list of options """

        res = []
        desactivated = []
        for p in self.parents():
            for option in reversed( p.options ):
                if option[ 0 ] not in desactivated:
                    res.append( option )
            desactivated += p.desactivated_options
        return list( reversed( res ) )

    def add_option( self, name: str, value: str = '', unique = False ):
        if unique:
            for option in self.all_the_options():
                if option[ 0 ] == name and option[ 1 ] == value:
                    return
        self.options.append( ( name, value ) )

    def single_letter_option_correspondance( self, letter ):
        if letter == 'I':
            return 'inc-path'
        if letter == 'L':
            return 'lib-path'
        if letter == 'l':
            return 'lib-name'
        if letter == 'o':
            return 'output'
        if letter == 'D':
            return 'define'
        self.error( f"there's no option correspondance for letter `{ letter }`" )

    # helper to add specific options --------------------------------------------------------------
    def add_lib_path( self, lib_path : str | Path ):
        self.add_option( "lib-path", str( self.resolved( lib_path ) ), unique = True )

    def add_lib_name( self, lib_name : str ):
        self.add_option( "lib-name", lib_name, unique = True )

    def add_inc_path( self, inc_path : str | Path ):
        self.add_option( "inc-path", str( self.resolved( inc_path ) ), unique = True )

    def add_cpp_flag( self, cpp_flag : str ):
        self.add_option( "cpp-flag", cpp_flag, unique = True )

    def add_lib_flag( self, lib_flag : str ):
        self.add_option( "lib-flag", lib_flag, unique = True )

    def add_define( self, value : str ):
        self.add_option( "define", value, unique = True )

    # vfs build config ---------------------------------------------------------------------------
    def load_lib( self, repository : str, lib_names ):
        if not repository.endswith( ".git" ):
            self.error( "currently, only git repositories are supported" )

        with load_lock:
            # base directory
            libname = repository[ repository.rfind( '/' ) + 1 : -4 ]
            lib_dir = self.build_dir( "ext", libname )

            lib_dir.mkdir( exist_ok = True, parents = True )

            # load the sources        
            sources = lib_dir / "sources"
            if not sources.exists():
                if subprocess.run( [ "git", "clone", repository, str( sources ) ] ).returncode:
                    sys.exit( 1 )
                
            # TODO: check for cmake
            install = lib_dir / "install"
            if not install.exists():
                # make a build dir
                build = lib_dir / "build"
                build.mkdir( exist_ok = True, parents = True )

                # configure and make
                cmds = [ 
                    [ "cmake", f"-DCMAKE_INSTALL_PREFIX={ install }", str( sources ) ],
                    [ "make" ],
                    [ "make", "install" ],
                ]
                for cmd in cmds:
                    if subprocess.run( cmd, cwd = build ).returncode:
                        install.unlink( missing_ok = True )
                        build.unlink( missing_ok = True )
                        sys.exit( 1 )

            # compilation flags
            self.add_inc_path( install / "include" )
            self.add_lib_path( install / "lib" )
            for lib_name in lib_names:
                self.add_lib_name( lib_name )

    # -------------------------------------------------------------------------------------------
    def build_dir( self, *args ) -> str:
        # self.build_dir_
        if self.build_dir_ is None:
            if p := self[ "build-dir" ]:
                self.build_dir_ = os.path.abspath( p.value )
            else:
                self.build_dir_ = os.path.join( os.path.expanduser('~'), '.vfs', "build" )
            os.makedirs( self.build_dir_, exist_ok = True )

        # if additional dirs in args
        if len( args ):
            res = os.path.join( self.build_dir_, *args )
            os.makedirs( res, exist_ok = True )
            return res
        
        # else, simply return build_dir_
        return self.build_dir_

    #  ------------------------------------------------------------------------------------
    def compiler_for( self, suffix ):
        if self.cpp_compiler_ is None:
            self.cpp_compiler_ = "g++"
        return self.cpp_compiler_

    def linker_for( self, suffixes: list[str] ):
        return self.compiler_for( '.cpp' )

    def resolved( self, path: Path ) -> Path:
        if not isinstance( path, Path ):
            return self.resolved( Path( path ) )
        if path.is_absolute():
            return path.resolve()
        return ( self.cwd / path ).resolve()

