#!/bin/python

"""
   @file
   @brief Utility to support the parsing and transformation of tabular
           representations of state machines into other formats
 
     Part of StateTableTools - https://github.com/bright-tools/StateTableTools

   @author John Bailey <dev@brightsilence.com>

   @copyright Copyright 2014 John Bailey

   @section LICENSE

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import fileinput
import StateMachine

from optparse import OptionParser

def output_dot_clusters( machine ):
    for state in machine.states.values():
        if( len( state.states )):
            # style = dashed; 
            print "subgraph \"cluster%s\" { label=\"%s\";"%(state.name,state.name)
            for sub_state in state.states.values():
                if( len( sub_state.states )):
                    output_dot_clusters( state )
                else:
                    print "  \"%s\""%(sub_state.name)
            print "}"

def output_dot_state( machine ):
    for state in machine.states.values():
        output_dot_state( state )
        if( len( state.states ) == 0):
            print "\"%s\" [ shape = box ];"%(state.name)
        for trans in state.transitions:
            src_name = state.name
            attrs = ""
            if( len( state.states )):
                src_name = state.states[ state.states.keys()[0] ].name
                attrs = " ltail=\"cluster%s\""%(state.name)
            dest = state.transitions[ trans ].name
            # TODO: deal with escaping of the label & node names
            print "\""+src_name + "\"->\"" + dest + "\" [ dir=forward label=\""+trans+"\"%s];"%(attrs)
            # decorate = true?
            # taillabel rather than label?

def output_dot( machine ):
    print "digraph G {"
    print "rankdir=LR;"
# USE THESE FOR DOT?
#    print "nodesep=1.2"
# END DOT
# USE THESE FOR FDP?
#    print "nodesep=2.0"
#    print "sep = 0.6;"
#    print "splines = ortho;"
# END FDP
#    print "K=0.2;"
#    print "overlap = vpsc;"
#    print "splines = curved;"
#    print "splines = true;"
    # This needs to be turned on to allow tails to be connected to sub-graphs
    print "compound=true;"
    output_dot_state( machine )
    output_dot_clusters( machine )
    print "}"

def parse_sem( p_input ):
    machine = StateMachine.StateMachineRaw()
    first = True
    for line in p_input:
        components = line.split( '|' )
        if first:
            for event in components[1:]:
                evt = event.strip()
                machine.events.append( evt )
#            print "Added Event: "+evt
            first = False
        else:
            state = components[0].strip()
            machine.states.append( state );
            if( state in machine.transitions ):
                print "Error: Repeated state %s"(state)
            else:
                machine.transitions[ state ] = {}
            trans_ctr = 0
            for transition in components[1:]:
                trans = transition.strip()
                machine.transitions[ state ][ machine.events[ trans_ctr ] ] = trans 
                trans_ctr = trans_ctr + 1
    return machine

input_formats= {"sem": parse_sem }
output_formats= {"dot": output_dot }

if __name__ == '__main__':
    parser = OptionParser()
    opts_ok = True
    parser.add_option("-s", "--source-format",
                      action="store",
                      metavar="FORMAT",
                      dest="sourceformat",
                      help="format of the table",
                      default="sem" )
    parser.add_option("-d", "--dest-format",
                      action="store",
                      metavar="FORMAT",
                      dest="destformat",
                      help="format of the output",
                      default="dot" )
    (options, args) = parser.parse_args()
    if( options.sourceformat not in input_formats.keys() ):
        print "ERROR: source format %s is not understood"
        opts_ok = False
    if( options.destformat not in output_formats.keys() ):
        print "ERROR: destination format %s is not understood"
        opts_ok = False

    if opts_ok:
        machine = input_formats[options.sourceformat]( fileinput.input(args) )

        abstractMachine = StateMachine.StateMachine( machine )
        # TODO: Check referential integrity of machine
        # TODO: Transition actions
        abstractMachine.resolveNesting()
        output_formats[options.destformat]( abstractMachine )
