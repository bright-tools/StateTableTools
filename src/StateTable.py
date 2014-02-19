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

if __name__ == '__main__':
    machine = StateMachine.StateMachine()
    first = True
    for line in fileinput.input():
        components = line.split( '|' )
        if first:
            for event in components[1:]:
                evt = event.strip()
                machine.events.append( evt )
#                print "Added Event: "+evt
            first = False
        else:
            state = components[0].strip()
            machine.states.append( state )
            if( state in machine.transitions ):
                print "Error: Repeated state %s"(state)
            else:
                machine.transitions[ state ] = {}
            trans_ctr = 0
            for transition in components[1:]:
                trans = transition.strip()
                machine.transitions[ state ][ machine.events[ trans_ctr ] ] = trans 
                trans_ctr = trans_ctr + 1

    # TODO: Check referential integrity of machine
    # TODO: Change transitions to be in tuples

    print "digraph G {"
    for state in machine.states:
        for trans in machine.transitions[ state ]:
            dest = machine.transitions[ state ][trans]
            if( len( dest )):
                # TODO: deal with escaping of the label & node names
                print "\""+state + "\"->\"" + dest + "\" [ dir=forward label=\""+trans+"\"]"
    print "}"


