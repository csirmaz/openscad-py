
from typing import Union as TUnion
from typing import List


class Header:
    """Render a header (setting global values) of an OpensCAD file"""


    def __init__(self, quality: str = 'draft'):
        # See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Circle_resolution:_$fa,_$fs,_and_$fn
        self.quality = quality


    def render(self):
        """Return OpenSCAD code"""
        if self.quality == 'draft':
            return ""
        if self.quality == 'mid':
            return "$fa=12;$fs=0.2;"
        if self.quality == 'best':
            return "$fa=6;$fs=0.1;"
        raise ValueError("Unknown quality")

