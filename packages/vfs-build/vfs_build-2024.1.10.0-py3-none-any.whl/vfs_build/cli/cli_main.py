#!/usr/bin/env python

from ..actors.LinkAndLaunch import LinkAndLaunch
from ..actors.Link import Link

from ..support.ActorSystem import ActorSystem
from ..support.Options import Options

import sys

def cli_main():
    # parse args. Simplified format where options are next (no space) to the flags
    # words:
    #   --flag
    #   --flag=...
    # single letter:
    #    -f
    #    -f...
    mission = ''
    sources = []
    options = Options()
    for num_arg in range( 1, len( sys.argv ) ):
        arg = sys.argv[ num_arg ]

        # extra arg
        if arg == '--':
            options.extra_args = sys.argv[ num_arg + 1: ]
            break

        # --flag
        if arg.startswith( '--' ):
            i = arg.find( '=' )
            if i >= 0:
                options.add_option( arg[ 2:i ], arg[ i+1: ] )
            else:
                options.add_options( arg[ 2: ] )
            continue

        # -f
        if arg.startswith( '-' ):
            if len( arg ) == 1:
                print( 'In arguments for vfs_build, `-` must be followed by a character', file=sys.stderr )
                sys.exit( 1 )
            options.add_options( options.single_letter_option_correspondance( arg[ 1 ] ), arg[ 2: ] )
            continue

        # mission
        if mission == '':
            mission = arg
            continue 

        # positionnal arg
        sources.append( arg )

    #

    # call the builder
    # # make and run executable
    # if mission == 'run':
    #     output_files, _ = build( env, "exe", sources )

    #     cp = subprocess.run( [ output_files[ 0 ].input_name, *env.extra_args ] )
    #     sys.exit( cp.returncode )

    # # make executable
    # if mission == 'exe':
    #     return env.load_or_execute( Exe(), [ File( source ) for source in sources ] )

    # # make object
    # if mission == 'obj':
    #     return env.load_or_execute( Obj(), [ File( source ) for source in sources ] )
    def do_mission( asy ):
        if mission == 'run':
            return asy.launch( None, sys.exit, LinkAndLaunch(), sources )

        if mission == 'lib':
            return asy.launch( None, sys.exit, Link(), 'lib', sources )

        if not mission:
            print( 'Please specify a mission', file = sys.stderr )
            sys.exit( 1 )
            
        print( f'`{ mission }` is not a known mission', file = sys.stderr )
        sys.exit( 2 )

    asy = ActorSystem( options )
    do_mission( asy )
    asy.wait()
