"""
The state management module for the editor.

This module contains the `MainEditorStateManager` which is a custom
`StateManager` that holds the globals for the editor, and `State` 
which is based on `game_state.State` and has extra functionality such as
`jump_to_state`, `window` getter that would get the window from the manager

"""

from utils.helper import AttrDict
from game_state import State as orgState, StateManager

class MainEditorStateManager(StateManager):
    """
    The main state manager for the editor.
    holds the globals so it's accessible to all state
    """
    globals: AttrDict = AttrDict(slot=0)
    def __init__(self, window):
        super().__init__(window)
        self.window = window

class State(orgState):
    """ The main state class for the editor. """
    manager: MainEditorStateManager
    focused: bool = True

    @property
    def globals(self) ->  AttrDict:
        """ get the globals dict from manager """
        return self.manager.globals

    def jump_to_state(self, name: str):
        """ jump to a state """
        self.manager.change_state(name) # Change our state to Editor
        self.manager.update_state()  # Updates / resets the state.
