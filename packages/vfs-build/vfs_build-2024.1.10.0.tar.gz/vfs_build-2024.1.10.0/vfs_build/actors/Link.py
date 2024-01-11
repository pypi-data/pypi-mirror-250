from ..support.Options import Options 
from .Compiler import Compiler
from .Command import Command
from .Actor import Actor

from pathlib import Path
import os

class Link( Actor ):
    def on_start( self, link_type: str, sources: list[ str ] ) -> None:
        self.nb_sources_to_compile = 0
        self.link_type = link_type
        self.seen_includes = []
        self.seen_sources = []
        self.objects = []

        for source in sources:
            self.add_source( os.path.abspath( source ) )
        self.check_if_ended()

    def add_source( self, source: str ):
        if source in self.seen_sources:
            return 
        self.seen_sources.append( source )

        self.add_source_dep( source )

        compiler = Compiler()
        compiler.desactivated_options.append( "output" )

        self.nb_sources_to_compile += 1
        self.launch( self.on_compile, compiler, source )

    def on_compile( self, obj: str, deps: list[ str ] ):
        self.nb_sources_to_compile -= 1
        self.objects.append( obj )

        for dep in deps:
            if dep.endswith( ".h" ):
                self.add_include( os.path.abspath( dep ) )
        self.check_if_ended()

    def add_include( self, include: str ):
        if include in self.seen_includes:
            return 
        self.seen_includes.append( include )

        self.add_source_dep( include )

        cpp = str( Path( include ).with_suffix( ".cpp" ) )
        if self.check_file( cpp ):
            self.add_source( cpp )

    def check_if_ended( self ):
        if self.nb_sources_to_compile:
            return

        ext = None
        if self.link_type == 'exe':
            ext = "exe"
        elif self.link_type == 'lib':
            from distutils import sysconfig
            ext = sysconfig.get_config_var('SHLIB_SUFFIX')
            print( ext )
        else:
            self.error( f"`{ self.link_type }` is not a known link type" )

        self.output_filename = self.make_output_filename( sub_dirs = [ 'obj' ], ext = ext, stem = Path( self.seen_sources[ 0 ] ).stem )

        self.info( f"Link of { self.relative_name( self.output_filename ) }" )

        self.launch( self.on_link, Command(), link_flags( 
            self.link_type,
            self.options.linker_for( ["cpp"] ), 
            self.output_filename,
            self.objects,
            self.options
        ) )
        
    def on_link( self ):
        self.on_end( self.output_filename )


def link_flags( link_type: str, linker: str, output_path: Path, obj_files: list[ str ] , options: Options ) -> list[str]:
    res = [ linker, '-o', str( output_path ) ]
    for obj_file in obj_files:
        res.append( obj_file )
    for option in options.all_the_options():
        if option[ 0 ] == 'lib-path':
            res.append( f'-L{ option[ 1 ] }' )
            continue
        if option[ 0 ] == 'lib-name':
            res.append( f'-l{ option[ 1 ] }' )
            continue
        if option[ 0 ] == 'lib-flag':
            res.append( str( option[ 1 ] ) )
            continue
    return res

