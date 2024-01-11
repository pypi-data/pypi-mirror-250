from ..support.Options import Options
from threading import Thread
from queue import Queue
import hashlib
import json
import sys
import os


class ActorSystem:
    """ ad hoc actor system to handle thread, callback, dependancies... """

    def __init__( self, options: Options ) -> None:
        self.exception_queue = Queue()
        self.cmd_queue = Queue()
        self.options = options
        # self.actors = []

        self.threads = []
        for _ in range( os.cpu_count() ):
            th = Thread( target = self._worker, daemon = True )
            self.threads.append( th )
            th.start()

    def launch( self, parent_actor, cb, actor, *args, **kwargs ):
        self.cmd_queue.put( { 
            "parent_actor": parent_actor, 
            "kwargs": kwargs,
            "actor": actor, 
            "args": args, 
            "cb": cb, 
        } )

    def _worker( self ):
        try:
            while True:
                dict = self.cmd_queue.get()
                self._start_actor( 
                    dict[ "actor" ],
                    dict[ "args" ], 
                    dict[ "kwargs" ],
                    dict[ "cb" ],
                    dict[ "parent_actor" ]
                )
                self.cmd_queue.task_done()        
        except KeyboardInterrupt as exception:
            self.exception_queue.put( SystemExit( 1 ) )
        except SystemExit as exception:
            self.exception_queue.put( exception )
        except Exception as exception:
            self.exception_queue.put( exception )

    def _start_actor( self, actor, args, kwargs, cb, parent_actor ):
        # check if already done. Else, get `dependancy_file` to save the output
        if actor.is_idempotent():
            short_name = actor.short_name( *args, **kwargs )
            parameter_repr = repr( { "type": type( actor ).__name__, "args": args, "kwargs": kwargs } )
            is_cached, dependancy_file, output_args, output_kwargs = self._from_cache( short_name, parameter_repr )
            if is_cached:
                return cb( *output_args, **output_kwargs )
            
            actor._dependancy_file = dependancy_file
            actor._parameter_repr = parameter_repr

        # data for the new actor
        actor.options = Options( desactivated_options = actor.desactivated_options, parent = parent_actor and parent_actor.options )
        actor.parent = parent_actor
        actor.actor_system = self
        actor.end_cb = cb

        # call on_start
        actor.on_start( *args, **kwargs )

    def _from_cache( self, short_name, parameter_repr ):
        th = hashlib.md5( parameter_repr.encode() ).hexdigest()
        bd = self.options.build_dir( 'db' )
        for n in range( 10000 ):
            dependancy_file = os.path.join( bd, f'{ short_name }.{ th }.{ n }.json' )
            if os.path.exists( dependancy_file ):
                with open( dependancy_file ) as fin:
                    js = json.load( fin )
                if js[ "parameter_repr" ] == parameter_repr:
                    # check dependancies and output files
                    for n in [ "input_files", "output_files" ]:
                        for p in js[ n ].items():
                            if p[ 1 ] < 0:
                                if os.path.exists( p[ 0 ] ):
                                    return False, dependancy_file, None, None
                            elif not os.path.exists( p[ 0 ] ) or os.path.getmtime( p[ 0 ] ) != p[ 1 ]:
                                return False, dependancy_file, None, None

                    # => we can use the output(s)
                    return True, dependancy_file, js[ "output_args" ], js[ "output_kwargs" ]
                continue

            # => we can use dependancy_file to store the output we're going to compute
            return False, dependancy_file, None, None

    def _save_cache( self, actor, args, kwargs ):
        if actor.is_idempotent():
            # get mtime of output_files
            output_files = {}
            for name in list( actor._output_files.keys() ):
                if os.path.exists( name ):
                    output_files[ name ] = os.path.getmtime( name )
                else:
                    output_files[ name ] = -1

            # save deps + outputs
            with open( actor._dependancy_file, 'w' ) as fout:
                json.dump( {
                    "parameter_repr": actor._parameter_repr,
                    "input_files": actor._input_files,
                    "output_files": output_files,
                    "output_kwargs": kwargs,
                    "output_args": args,
                }, fout, indent=4 )

    def wait( self ):
        try:
            exception = self.exception_queue.get()
        except KeyboardInterrupt:
            sys.exit( 1 )
            
        raise exception
