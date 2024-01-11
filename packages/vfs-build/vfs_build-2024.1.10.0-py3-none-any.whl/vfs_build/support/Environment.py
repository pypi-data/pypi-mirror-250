from importlib.machinery import SourceFileLoader
from pathlib import Path 
import subprocess, sys, os
import hashlib, json

from Dependancies import Dependancies
from Optionnal import Optionnal
from File import File

class Environment:
    def __init__( self, func = None, inputs = None, parent = None, options: list[tuple[str,str]] = None, desactivated_options: list[str] = None ) -> None:
        self.desactivated_options = desactivated_options or [] # notably for options defined in parent(s)
        self.extra_args = []
        self.options = options or [] # list of tuple( name, value )
        self.inputs = inputs or []
        self.parent = parent
        self.func = func

        # cached variables
        self.cpp_compiler_ = None
        self.build_dir_ = None

        # context
        self.cwd = None

    # cache -------------------------------------------------------------------------------------------------------------------
    def load_or_execute( self, func, input_files: list[File], desactivated_options: list[str] = [] ) -> tuple[list[File],Dependancies]:
        # try to load the dep file. If no dep has changed, one can return data from this file
        dep_file = self.dep_file_for( func, input_files )

        class DependancyDate(Exception):
            pass
        try:
            with open( dep_file ) as fin:
                js = json.load( fin )

                # check inputs
                for p in js[ "inputs" ]:
                    f = File( p[ 0 ] )
                    if f.modification_date != p[ 1 ]:
                        raise DependancyDate

                # dependancies
                dependancies = Dependancies()
                for p in js[ "dependancies" ]:
                    f = File( p[ 0 ] )
                    if f.modification_date != p[ 1 ]:
                        raise DependancyDate
                    dependancies.add_file( f )

                return [ File( output ) for output in js[ "outputs" ] ], dependancies
        except ( DependancyDate, FileNotFoundError ):
            pass

        # else, make a new Environment, read configs
        env = Environment( func = func, parent = self, desactivated_options = desactivated_options )
        for input_file in input_files:
            env.read_config_for( input_file.input_path )
        output_paths = env.output_paths_for( func, input_files )
        dependancies = Dependancies()

        # execute
        func.exec( env, dependancies, output_paths, input_files )

        # save
        with open( dep_file, 'w' ) as fout:
            obj = {
                "inputs": [ ( input_file.input_name, input_file.modification_date ) for input_file in input_files ],
                "outputs": [ str( output_path ) for output_path in output_paths ],
                "dependancies": [ ( f.input_name, f.modification_date ) for f in dependancies.files ]
            }
            json.dump( obj, fout )

        return [ File( output_path ) for output_path in output_paths ], dependancies

    def dep_file_for( self, func, inputs: list[File] ) -> Path:
        # make a "base" hash
        th = hashlib.md5( str( {
            'options': list( func.relevant_options( self, [ input.suffix for input in inputs ] ) ),
            'inputs': [ input.input_name for input in inputs ]
        } ).encode() ).hexdigest()

        # test availability
        for h in range( 100000 ):
            name_items = [ type( func ).__name__, th, str( h ), 'dep' ]
            if len( inputs ):
                name_items.insert( 0, inputs[ 0 ].stem )
            proposal = self.build_dir() / Path( '.'.join( name_items ) )
            # TODO: check if file is the result for another execution
            available = True
            if available:
                return proposal

    def output_paths_for( self, func, inputs: list[File] ) -> list[Path]:
        if o := self[ 'output' ]:
            return o.value.split( ',' )
        output_paths = []
        for suffix in func.output_suffixes( self, inputs ):
            op = str( list( func.relevant_options( self, [ input.suffix for input in inputs ] ) ) )
            th = hashlib.md5( op.encode() ).hexdigest()
            for h in range( 10000 ):
                proposal = ''
                if len( inputs ):
                    proposal = self.build_dir() / Path( f'{ inputs[ 0 ].stem }.{ th }_{ h }.{ suffix }' )
                else:
                    proposal = self.build_dir() / Path( f'{ th }_{ h }.{ suffix }' )

                # TODO: check if file is the result for another execution
                if False:
                    continue

                output_paths.append( proposal )
                break
        return output_paths

    # config ------------------------------------------------------------------------------------------------------------------
    def read_config_from( self, dir ):
        """ read environment config for dir `files` using .vbc.py files or vfs_build_config.py in parent directories """
        dirs = [ dir ]
        for p in Path( dir ).parents:
            if not dirs.count( p ):
                dirs.append( p )
        
        for dir in dirs:
            cf = dir / 'vfs_build_config.py'
            if cf.exists():
                loader = SourceFileLoader( "vfs_build_config", str( cf ) )
                imp = loader.load_module()

                self.cwd = dir

                imp.config( self )

    def read_config_for( self, file: str | Path ):
        """ read environment config for files `files` using .vbc.py files or vfs_build_config.py in parent directories """
        self.read_config_from( Path( file ).parent )

    # ---------------------------------------------------------------------------
    def cmd( self, args, cwd = None, authorized_fail = False, parallel = False ):
        # print( args )
        if cwd is None:
            cwd = Path.cwd()

        # use popen ?
        if parallel:
            class SubProcess:
                def __init__( self, args, cwd, authorized_fail ) -> None:
                    self.fout = os.tmpfile()
                    self.ferr = os.tmpfile()
                    self.p = subprocess.Popen( args, cwd = cwd, stdout = self.fout, stderr = self.ferr )

                def wait( self ):
                    if cp.stderr or cp.stdout:
                        if cp.stderr:
                            print( " ".join( args ), file = sys.stderr )
                            sys.stderr.write( cp.stderr )
                            if cp.stdout:
                                sys.stderr.write( cp.stdout )
                        else:
                            print( " ".join( args ) )
                            sys.stdout.write( cp.stdout )
                    if cp.returncode:
                        if not authorized_fail:
                            sys.exit( cp.returncode )

            return SubProcess( args, cwd, authorized_fail )

        # cp = subprocess.run( args,  )
        cp = subprocess.Popen( args, cwd = cwd, capture_output = True )

        if cp.stderr or cp.stdout:
            if cp.stderr:
                print( " ".join( args ), file = sys.stderr )
                sys.stderr.write( cp.stderr )
                if cp.stdout:
                    sys.stderr.write( cp.stdout )
            else:
                print( " ".join( args ) )
                sys.stdout.write( cp.stdout )

        if cp.returncode:
            if not authorized_fail:
                sys.exit( cp.returncode )

        return cp.returncode

    def resolved( self, path : Path ):
        if path.is_absolute():
            return path.resolve()
        return ( self.cwd / path ).resolve()

    def relative_name( self, file: File ):
        if not isinstance( file, File ):
            return self.relative_name( File( file ) )
        try:
            return str( Path.relative_to( file.input_path, Path.cwd() ) )
        except ValueError:
            return file.input_name
        # try:
        #     return str( Path.relative_to( file.input_path, self.build_dir() ) )
        # except ValueError:
        #     return self.input_name

