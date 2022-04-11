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

    #zobere pohyb ako parameter a pusti ho (proste funkcia na pohyb)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move, takze vieme dat naspat (neskor)
        self.whiteToMove = not self.whiteToMove #prehodime hracov
    
    #funkcia na vratenie pohybu spat
    def undoMoves(self):
        if len(self.moveLog) != 0:          #ujistim sa ze tam nieco je
            move = self.moveLog.pop()      #pop je funkcia ktora zobere poslednu vec v liste a otoci ju
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaputer
            self.whiteToMove = not self.whiteToMove #prehodi na cierneho

    #vsetky tahy s ohladom na kontrolu
    def getValiddMoves(self):
        return self.allMoves()
    
    #vsetky tahy bezohladom na kontrolu
    def allMoves(self):
        moves = []
        for r in range(len(self.board)):        #pocet riadkov
            for c in range(len(self.board[r])): #pocet stplcov
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':            #ak je to pesiak
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
        return moves

    #def 
    #funkcia pre pesiakov, ziska vsetky moze pohyby pre nich
    def getPawnMoves(self, r,c,moves):
        if self.whiteToMove:    #ak je biela na rade
            if self.board[r-1][c] == "--":  #1 stvorcek
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 stvorceky dopredu
                    moves.append(Move((r,c), (r-2,c), self.board)) 

            if c-1 >= 0:                            #lava strana
                if self.board[r-1][c-1][0] == 'b':  #ak je tam enemy cierny
                    moves.append(Move((r, c), (r-1,c-1), self.board))
            if c+1 <= 7:                            #prava strana
                if self.board[r-1][c+1][0] == 'b':  #ak je tam enemy cierny
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else:
            #black pawns
            if self.board[r+1][c] == "--":  #ak je prednim przdno
                moves.append(Move((r, c), (r+1, c), self.board))    #jeden krok vpred
                
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))  #dva pred
            
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':                      #lava strana
                    moves.append(Move((r,c), (r-1, c+1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':                      #prava strana
                    moves.append(Move((r,c), (r+1, c+1), self.board))
        
    def getRookMoves(self, r,c, moves):
        pass

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
        self.moveID = self.startRow * 1000 + self.startCol * 10000 + self.endRow / 10 + self.endCol
        print(self.moveID)

    #overriding the equals methods
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol);

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]