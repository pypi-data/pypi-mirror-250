from uniws import *


def hardware() -> 'list[Hardware] | Hardware':
    '''
    Return a list of available Hardware to attach to, or the current Hardware.

    Returns:
     * Hardware, the current Hardware instance, if attached to any.
     * list[Hardware], the list of available Hardware, may be empty.
    '''
    # TODO: Determine if already attached.
    attached = False
    if attached:
        # TODO: Determine the current Hardware.
        result = None
        return result
    # TODO: Populate the list of available Hardware.
    result = []
    return result
