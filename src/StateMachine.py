"""
   @file
   @brief Python module supporting the representation of a state
          machine
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

class StateMachineRaw:
    """
    This class supports the internal represention of the state machine
    """
    def __init__(self):
        self.states = []
        self.events = []
        self.transitions = {}

class StateMachine:

    def __init__(self, p_src = None, parent = None ):
        self.states = {}
        self.events = []
        self.transitions = {}
        self.state_mapping = {}
        self.transitions_to = 0
        self.parent = parent
        if( self.parent is not None ):
            self.root = parent.root
        else:
            self.root = None
        self.name = "UNNAMED"

        if( p_src is not None ):
            self.root = self
            # TODO: Handle nests at a greater depth than 1
            for state in p_src.states:
                comps = state.split(",")
                if( len( comps ) > 1):
                    target_state = self
                    for depth in range( 0, len( comps ) ):
                        state_name = comps[depth].strip()
                        if( state_name in target_state.states ):
                            if( not isinstance( target_state.states[ state_name ], StateMachine)):
                                print "ERROR %s %s!"%(target_state.states[ state_name ], type( target_state.states[ state_name ]))
                        else:
                            target_state.states[ state_name ] = StateMachine( parent = target_state )
                            target_state.states[ state_name ].name = state_name

                        sm = target_state.states[ state_name ]
                        target_state = sm
                else:
                    self.states[ state ] = StateMachine( parent = self )
                    target_state = self.states[ state ]
                    target_state.name = state
                self.state_mapping[ state ] = target_state
            for state in p_src.states:
                for trans in p_src.transitions[ state ]:
                    if( len( p_src.transitions[ state ][ trans ] )):
                        target = self.state_mapping[ p_src.transitions[ state ][ trans ] ]
                        self.state_mapping[ state ].transitions[ trans ] = target
                        target.transitions_to = target.transitions_to + 1

    def getTransitionsTo(self):
        count = self.transitions_to
        for state in self.states.values():
            count = count + state.getTransitionsTo()

        return count

    def resolveNesting(self):
        # Post-order depth-first traversal of the tree
        # Do this to ensure that we resolve the nesting on
        # child nodes so that any commonality in transitions
        # 'bubbles' up the tree and can be considered in the
        # routine below
        for state in self.states.values():
            state.resolveNesting()

        # Needs to have > 1 sub-state for use to do nesting
        if( len( self.states ) > 1 ):
            # Copy the transition list for the first state (could be any state)
            transitions = self.states[ self.states.keys()[0] ].transitions.copy()
            # Visit all the states
            for state in self.states.values():
                # Check to see if the transitions match those in the snapshot we
                # took - remove from the snapshot if not
                for transition in transitions.keys():
                    if(( transition in state.transitions ) and
                       ( state.transitions[ transition ] == transitions[ transition ] )):
                        pass
                    else:
                        transitions.pop( transition )
            # At this point we've effectively filtered the snapshot of
            # transitions and any that are left are common to all
            # sub-states
            for transition in transitions:
                # Add the transition to our list ...
                self.transitions[ transition ] = transitions[ transition ]
                # And remove it from the child states ..
                for state in self.states.values():
                    state.transitions.pop( transition )
