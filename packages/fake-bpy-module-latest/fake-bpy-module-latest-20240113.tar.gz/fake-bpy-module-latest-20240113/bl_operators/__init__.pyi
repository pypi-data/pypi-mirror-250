import sys
import typing
from . import add_mesh_torus
from . import uvcalc_lightmap
from . import image
from . import presets
from . import object_quick_effects
from . import object_randomize_transform
from . import bmesh
from . import spreadsheet
from . import uvcalc_follow_active
from . import clip
from . import mesh
from . import object_align
from . import assets
from . import wm
from . import file
from . import screen_play_rendered_anim
from . import view3d
from . import console
from . import geometry_nodes
from . import constraint
from . import userpref
from . import freestyle
from . import anim
from . import vertexpaint_dirt
from . import sequencer
from . import uvcalc_transform
from . import node
from . import object
from . import rigidbody

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...
