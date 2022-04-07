#toto je file kde budeme tieto data ukladat, tiez ma nastarosti robit LEN validne pohyby
#tiez moove log

class GameState():
    def __init__(self):
        #mozno pouzit numpy array neskor, pre rychlost
        #board je 8*8 a kazdy list ma 2 charakterov, prvy reprezentuje farbu b - black, w-white
        #druhy charakter prezentuje o aku figurku ide
        # "--" reprezentuje prazdnu poziciu
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []

    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move, takze vieme dat naspat (neskor)
        self.whiteToMove = not self.whiteToMove #prehodime hracov


class Move():            
    #MAPA KLUCOV K HODNOTAM
    #pomocou tohto mapy sa daje zistit ci je mozne tahnutie na poziciu
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0} 
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
  
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]                                  #zistime ktory riadok
        self.endCol = endSq[1]                                  #zistime ktory stlpec

        self.pieceMoved = board[self.startRow][self.startCol]   #tu bude figurka ktoru bude menit
        self.pieceCaputer = board[self.endRow][self.endCol]     #tu bude ukladat co sa vyhodilo

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol);

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]