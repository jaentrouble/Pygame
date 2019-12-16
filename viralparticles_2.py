## empty classes to represent some proteins or particles etc.
class ViralProtein() :
    pass

class Capsid(ViralProtein) :
    pass

class HIVCapsid(Capsid) :
    pass

class EpiCapsid(Capsid) :
    pass

class ViralNucleicAcid() :
    pass

class ViralDNA(ViralNucleicAcid) :
    pass