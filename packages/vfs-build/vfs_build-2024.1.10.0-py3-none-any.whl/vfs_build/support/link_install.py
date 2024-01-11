import stat
import os

def write_executable( name, cb ):
    with open( name, "w" ) as fout:
        cb( fout )

    # get full permission spectrum
    os.umask( 0 )
    st = os.stat( name )
    os.chmod( name, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH )

def write_vfs_build( fout ):
    py_name = os.path.abspath( os.path.join( os.path.dirname( __file__ ), "vfs_build" ) )

    fout.write( f"#!/bin/sh\n" )
    fout.write( f"python { py_name }\n" )

def install_directory():
    return os.path.expanduser( "~/.local/bin" )

write_executable( os.path.join( install_directory(), "vfs_build" ), write_vfs_build )
