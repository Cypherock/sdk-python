from . import command
from . import constants
from . import radix

# Version configurations
v1 = {
    'commands': command.v1,
    'constants': constants.v1,
    'radix': radix.v1,
}

v2 = {
    'commands': command.v1,
    'constants': constants.v2,
    'radix': radix.v2,
}

v3 = {
    'commands': command.v3,
    'constants': constants.v3,
    'radix': radix.v3,
}

# Export individual modules
from .command import *
from .constants import *
from .radix import *

__all__ = ["v1", "v2", "v3"]

