import prokaryote_2 as prokaryote
import cells_2 as cell
import functions_2 as tool
import os
import math
import bacterialparticles_2 as bp
from layerconst_2 import *

IMGDICT = {}
LAYERDICT = {}

class Coccus(prokaryote.GramPositive) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 7) :
        prokaryote.GramPositive.__init__(self,startpos,speed,imgnum)
        self.properties[bp.Catalase] = None

class Staphylococcus(Coccus) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 7) :
        Coccus.__init__(self,startpos,speed, imgnum)
        self.properties[bp.Catalase] = True
        self.properties[bp.Coagulase] = None

class Aureus(Staphylococcus) :
    """
    Staphylococcus Aureus
    MRSA : Methicillin Resistant S.Aureus
    VRSA : Vancomycin Resistant S.Aureus
    diseases =  Food poisoning : recover in 12~24hr
                Toxic Shock Syndrome : problem of toxin, antibiotics don't work
                Scalded Skin Syndrome
                Skin infection : impetigy, folliculitis, furuncles, carbuncles
    cf) Does not induce meningitis
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Aureus'] = cell.Cell.imgs[7]
    LAYERDICT['Aureus'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Staphylococcus.__init__(self,startpos,speed, 7)
        self.properties[bp.Catalase] = True
        self.properties[bp.Coagulase] = True
        self.properties[bp.Capsule] = True
        self.receptor.extend([bp.Capsule,
                              bp.ProteinA])
        self.toxin.extend([bp.ProteinA,
                           bp.EFT,
                           bp.Enterotoxin,
                           bp.TSST])

class CNS(Staphylococcus) :
    """
    Coagulase Negative Staphylococcus
    Lives on the skin or mucus
    """
    def __init__(self, startpos : list, speed : list, imgnum : int = 7) :
        Staphylococcus.__init__(self,startpos,speed, imgnum)
        self.properties[bp.Catalase] = True
        self.properties[bp.Coagulase] = False

class Epidermidis(CNS) :
    """
    Staphylococcus Epidermidis
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Epidermidis'] = cell.Cell.imgs[7]
    LAYERDICT['Epidermidis'] = PATHOGENLAYER
    def __init__(self, startpos : list, speed : list) :
        CNS.__init__(self,startpos,speed, 7)
        self.properties[bp.Catalase] = True
        self.properties[bp.Coagulase] = False

class Saprophyticus(CNS) :
    """
    Staphylococcus Saprophyticus
    Skin or Urogenital mucus
    Novobiocin resistant
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Saprophyticus'] = cell.Cell.imgs[7]
    LAYERDICT['Saprophyticus'] = PATHOGENLAYER
    def __init__(self, startpos : list, speed : list) :
        CNS.__init__(self,startpos,speed, 7)
        self.properties[bp.Catalase] = True
        self.properties[bp.Coagulase] = False

class Streptococcus(Coccus) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 7) :
        Coccus.__init__(self,startpos,speed, imgnum)
        self.properties[bp.Catalase] = False

class Pyogenes(Streptococcus) :
    """
    Streptococcus Pyogenes
    Beta-hemolysis, Group A
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Pyogenes'] = cell.Cell.imgs[7]
    LAYERDICT['Pyogenes'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Streptococcus.__init__(self,startpos,speed, 7)
        self.receptor.extend([bp.MProtein,
                              bp.FProtein])
        