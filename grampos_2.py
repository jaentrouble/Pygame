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

#############################################

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

#############################################

class Streptococcus(Coccus) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 7) :
        Coccus.__init__(self,startpos,speed, imgnum)
        self.properties[bp.Catalase] = False

class Pyogenes(Streptococcus) :
    """
    Streptococcus Pyogenes
    Beta-hemolysis, Group A (bacitracin sensitive)
    Diseases =  pharyngitis,
                scarlet fever(성홍열) : only which has toxin by Phage
                pyoderma,
                cellulitis
                necrotizing fascitis : 피하조직 감염, fascial plane 번짐, life threatening
                streptococcal toxic shoc syndrome : M protein & speA, speC
                ----- non pyogenic disease
                rheumatic fever
    Diagnosis = Bacitracin A disk susceptible test -> only pyogenes is sensitive
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Pyogenes'] = cell.Cell.imgs[7]
    LAYERDICT['Pyogenes'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Streptococcus.__init__(self,startpos,speed, 7)
        self.receptor.extend([bp.MProtein,
                              bp.FProtein])
        self.toxin.extend([bp.DicksToxin])

class Agalactiae(Streptococcus) :
    """
    Streptococcus Agalactiae
    Beta-hemolysis, Group B
    Distribution =  vagina : 산후 패혈증, new born infection
    Identification =    Bacitracin resistant,
                        CAMP factor test (+)
    Antibiotics =   Penicillin sensitive -> primary selection
                    Penicillin + Aminoglycoside or Vancomycin
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Agalactiae'] = cell.Cell.imgs[7]
    LAYERDICT['Agalactiae'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Streptococcus.__init__(self,startpos,speed, 7)
        self.properties[bp.Capsule] = True
        self.receptor.extend([bp.Capsule])

class Viridans(Streptococcus) :
    """
    Viridans Streptococcus
    Alpha-hemolysis
    - S.mutans : 충치 원인균
    - S.sanguis
    - S.intermedius
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Viridans'] = cell.Cell.imgs[7]
    LAYERDICT['Viridans'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Streptococcus.__init__(self,startpos,speed, 7)

class Pneumoniae(Streptococcus) :
    """
    Streptococcus Pneumoniae
    Alpha-hemolysis
    Toxic factor =  Capsule,
                    IgA protease : attacs mucus
    Distribution = normal flora of nasopharynx
    Disease =   Meningitis
                중이염
                Pneumonia
                Paranasal sinusitis
                Sepsis : over 80% of meningitis patient
    Diagnosis = Bile salt test (담즙 용해 시험) : The only way to identify s.pneumoniae
                Optochin 감수성 시험
                Quellung reaction : 항혈청이 일치할 경우 협막 팽화
    Prevention = Anti-Capsule vaccine : 23가 협막다당체 백신, 2세 이상
                 13가 접합백신 : 2세 이하, Polysaccharide + diphtheria toxoid - 단백접합
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Pneumoniae'] = cell.Cell.imgs[7]
    LAYERDICT['Pneumoniae'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Streptococcus.__init__(self,startpos,speed, 7)
        self.properties[bp.Capsule] = True
        self.receptor.extend([bp.Capsule])

#############################################

class Enterococcus(Coccus):
    """
    Enterococcus
    Infection = Usually start from Normal flora in Colon
                Transmitted by contaminated food or water
    Cure = Aminoglycoside + Ampicillin, Vancomycin
    """
    def __init__(self, startpos : list, speed : list, imgnum : int = 7) :
        Coccus.__init__(self,startpos,speed, imgnum)
        self.properties[bp.Catalase] = False

class Faecalis(Enterococcus) :
    """
    Enterococcus Faecalis
    6.5% NaCl, 40% 담즙에서 생존가능 -> 소독 어려움
    Vancomycin Resistant Enterococci : Vancomycin, Ampicillin 포함 다재내성
    Diagnosis = 6.5% NaCl 배지 성장
                40% 담즙 생존가능
                PYR test
    Cure = Ampicillin or Vancomycin + Amynoglycoside
    """
    rect = cell.Cell.imgs[7].get_rect()
    IMGDICT['Faecalis'] = cell.Cell.imgs[7]
    LAYERDICT['Faecalis'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list) :
        Streptococcus.__init__(self,startpos,speed, 7)

####################################################################################

class Bacillus(prokaryote.GramPositive) :
    def __init__(self, startpos : list, speed : list, imgnum : int = 8) :
        prokaryote.GramPositive.__init__(self,startpos,speed,imgnum)
        self.properties[bp.Spore] = True
        self.properties[bp.Catalase] = True

class Anthracis(Bacillus) :
    """
    Bacillus Anthracis(탄저균)

    Infection = Skin injury : 침입조직에서 발아, 증식, 혈류로 들어가 sepsis
                                -> 피부탄저, eschar 형성, mortality 20%
                Respiratory : 폐, 기관지 lymph node -> sepsis -> mostly die, Woolsorter's disease
                Infected animal meat : 장염 동반, high mortality, very rare

    Cure = many antibiotics work, but need to be quick
            Penicillin : low effect on respiratory anthrax
            Penicillin G, Amoxicillin 조기투여
            Ciproflaxacin : 경험적

    Vaccine is effective
    """
    rect = cell.Cell.imgs[8].get_rect()
    IMGDICT['Anthracis'] = cell.Cell.imgs[8]
    LAYERDICT['Anthracis'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list,) :
        Bacillus.__init__(self,startpos,speed, 8)
        self.properties[bp.Capsule] = True #However, it's protein; cannot induce meningitis
                                           #Still, evades phagocytosis
        self.toxin[bp.PA,
                   bp.EF,
                   bp.LF]

class Cereus(Bacillus) :
    """
    Bacillus Cereus
    Disease = 'Fried Rice Syndrome', 식중독
    Resistance = Penicillin
                 Highly resistant to heat (Spores)
    Disease = 구토형 식중독 : contaminated rice
              설사형 식중독 : contaminated meat, vegitable
              외상 : infection at eyes
    """
    rect = cell.Cell.imgs[8].get_rect()
    IMGDICT['Cereus'] = cell.Cell.imgs[8]
    LAYERDICT['Cereus'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list,) :
        Bacillus.__init__(self,startpos,speed, 8)
        self.properties[bp.Capsule] = False
        self.properties[bp.Catalase] = True

###########################################################

class Listeria(prokaryote.GramPositive) :
    pass

class Monocytogenes(Listeria) :
    """
    Listeria Monocytogenes
    Beta-hemolysis
    Mobility (+) : Tumbling (end over end)
    세포내 기생세균 : Macrophage, Epithelium
                        -> breaks phagolysosome
    Epidemiology :  Can cross placenta
                    Able to multiplicate at refrigerate temperature
                    Latent 7~28 days
    Diseases : 신생아 리스테리아증
                    => Early Onset = 유산, 조산, 사산, 출산 후 사망, Granulomatosis Infantiseptica
                    => Late Onset = Sepsis & Meningitis
               성인 감염
                    => Asymptomatic or light cold
                    => Meningitis if immune deficiency
                Primary Bacteraemia
    Cure = Penicillin, Ampicillin, Vancomycin
    """
    rect = cell.Cell.imgs[8].get_rect()
    IMGDICT['Monocytogenes'] = cell.Cell.imgs[8]
    LAYERDICT['Monocytogenes'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list,) :
        Listeria.__init__(self,startpos,speed, 8)
        self.properties[bp.Spore] = False
        self.properties[bp.Catalase] = True

############################################################

class Corynebacterium(prokaryote.GramPositive) :
    """
    Corynebacterium
    그람양성막대균
    곤봉모양
    """

class Diphtheriae(Corynebacterium) :
    """
    Corynebacterium Diphtheriae
    Respiratory Diphtheria
        => 2~5 days latent phase
        => Pseudomembrane : blocks upper respiratory tract
        => Diphthera Toxin : Organ destruction (including heart)
    Skin Diphtheria

    Cure = Anti-toxin : Problem of toxin, so anti-toxin is needed
           Airway secured

    Prevention = Vaccination : Diphtheria Toxoid (Formalin) -> DTP
    """
    rect = cell.Cell.imgs[8].get_rect()
    IMGDICT['Diphtheriae'] = cell.Cell.imgs[8]
    LAYERDICT['Diphtheriae'] = PATHOGENLAYER

    def __init__(self, startpos : list, speed : list,) :
        Corynebacterium.__init__(self,startpos,speed, 8)
        self.toxin.extend([bp.DiphtheriaToxin])
        