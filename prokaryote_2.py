import pygame
import random
import os
import math
import cells_2 as cell
import bacterialparticles_2 as bp
from layerconst_2 import *

class Bacteria(cell.Prokaryote) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 6) :
        cell.Prokaryote.__init__(self, startpos, speed, imgnum)
        self.properties[bp.CellWall] = None
        self.properties[bp.OuterMembrane] = None
        self.toxin = []

class GramPositive(Bacteria):
    def __init__(self, startpos : list, speed : list, imgnum : int = 6) :
        Bacteria.__init__(self, startpos, speed, imgnum)
        self.properties[bp.CellWall] = True
        self.properties[bp.OuterMembrane] = None
