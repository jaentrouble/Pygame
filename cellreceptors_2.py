class CellReceptor():
    """
    Here, cell means body cell
    """
    pass

class Heparansulfate (CellReceptor) :
    pass

class CD4(CellReceptor) :
    pass

class CD8(CellReceptor) :
    pass

class MHC2(CellReceptor) :
    pass

class MHC1(CellReceptor) :
    def __init__(self):
        """
        .antigen : list of classes
        """
        self.antigen = []