class CellNotEmptyError(ValueError):
    pass

class CellOutOfBoundError(IndexError):
   
    def __init__(self,  msg = 'Cell out of boud'):
        self.msg = msg
  
