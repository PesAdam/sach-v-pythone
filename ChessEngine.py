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
        self.whiteKingLocation = (7,4)  #pozicia krala bielych
        self.blackKingLocation = (0,4)  #pozicia krala ciernych

    #zobere pohyb ako parameter a pusti ho (proste funkcia na pohyb)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move, takze vieme dat naspat (neskor)
        self.whiteToMove = not self.whiteToMove #prehodime hracov
        #pozreme sa ci sa kral pohol
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
    
    #funkcia na vratenie pohybu spat
    def undoMoves(self):
        if len(self.moveLog) != 0:          #ujistim sa ze tam nieco je
            move = self.moveLog.pop()      #pop je funkcia ktora zobere poslednu vec v liste a otoci ju
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaputer
            self.whiteToMove = not self.whiteToMove #prehodi na cierneho
            #update king pozicia
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    #vsetky tahy s ohladom na kontrolu
    def getValidMoves(self):
        #1.) gerenujem vsetky mozne tahy
        moves = self.allMoves()
        #2.) pre kazdy tah, urobim tah
        for i in range(len(moves)-1, -1, -1): #ked vymazavam z listu tak chod zo zadu toho listu
            self.makeMove(moves[i])
            
        #3.) generujem vsetky protihracove tahy
        #4.) pre kazdy protihracov tah, pozeram ci vie zautocit na krala
        self.whiteToMove = not self.whiteToMove                                 #switch
        if self.inCheck():
            moves.remove(moves[i])                                       #5.) ak ano, tento tah nieje validny
        self.whiteToMove = not self.whiteToMove
        self.undoMoves()


        return moves

    #zisti ci je hrac v sachu
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #zisti ci enemy moze zautocit na krala
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch 
        oppMoves = self.allMoves()
        self.whiteToMove = not self.whiteToMove #switch back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:       #stvorec je pod utokom
                self.whiteToMove = not self.whiteToMove     #switch 
            return True
        return False

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
                    elif piece == 'N':
                        self.getKingMoves(r,c,moves)
                    elif piece == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)
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
        
    #veza
    def getRookMoves(self, r,c, moves):
        direction = ((-1,0), (1,0) , (0,1), (0,-1))             #vsetky smery kam moze veza ist, up, left, down, right
        enemy = 'b' if self.whiteToMove else 'w'                #enemy je cierny #noracism
        for d in direction:                                     #pre direct v direction
            for i in range(1, 8):                               #moze tiez chodit 7 policok
                endRow = r + d[0] * i                           #posledny riadok
                endCol = c + d[1] * i                           #posledny stplec
                if 0 <= endRow < 8 and 0 <= endCol < 8:         #ak 0 je viac ako posledny riadok a neni menej ako 8 a to iste aj so stlpcami
                    endPiece = self.board[endRow][endCol]       #posledny
                    if endPiece == "--":                        #ak je posledny prazdne pole
                        moves.append(                           #urob pohyb
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:                  #ak je to enemy tak ho zabi
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break
                    else:                                       #ak je to kamos tak ukonci
                        break
                else:                                           #ak je mimo pola
                    break

    #kon
    def getKnightMoves(self, r, c, moves):
        direction = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in direction:
            endRow = r + d[0]                           
            endCol = c + d[1] 
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != enemy:
                    moves.append(Move((r, c), (endRow, endCol), self.board))  

    #strelec
    def getBishopMoves(self, r, c, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))                #vsetky smery kam moze strelec ist, up, left, down, right
        enemy = 'b' if self.whiteToMove else 'w'                        #enemy je cierny ak je na rade biela tak sa prehodia  
        for d in direction:                                             #pre direct v direction
            for i in range(1, 8):                                       #moze ist maximalne 7 policok
                endRow = r + d[0] * i                                   #posledny riadok
                endCol = c + d[1] * i                                   #posledny stplec
                if 0 <= endRow < 8 and 0 <= endCol < 8:                 #ak 0 je viac ako posledny riadok a neni menej ako 8 a to iste aj so stlpcami
                    endPiece = self.board[endRow][endCol]               #posledny
                    if endPiece == "--":                                #ak je posledny prazdne pole
                        moves.append(Move((r, c), (endRow, endCol), self.board))  #urob pohyb
                    elif endPiece[0] == enemy:                          #ak je to enemy tak ho zabi
                        moves.append(Move((r, c), (endRow, endCol), self.board)) #urob pohyb
                        break                                   #ukonci
                    else:                                       #ak je to kamos tak ukonci
                        break
                else:                                           #ak je mimo pola
                    break       

    #kralovna
    def getQueenMoves(self, r, c, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1),
                    (-1, 0), (1, 0), (0, -1), (0, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in direction:
            for i in range(1, 8):
                endRow = r + d[0] * i                           #posledny riadok
                endCol = c + d[1] * i                           #posledny stplec
                if 0 <= endRow < 8 and 0 <= endCol < 8:         #ak 0 je viac ako posledny riadok a neni menej ako 8 a to iste aj so stlpcami
                    endPiece = self.board[endRow][endCol]       #posledny
                    if endPiece == "--":                        #ak je posledny prazdne pole
                        moves.append(Move((r, c), (endRow, endCol), self.board))
    
    #kral
    def getKingMoves(self, r, c, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1),
                    (-1, 0), (1, 0), (0, -1), (0, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in direction:
            endRow = r + d[0]                           #posledny riadok
            endCol = c + d[1] 
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemy:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    break
                else:
                    break
    
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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow / 10 + self.endCol
        print(self.moveID)

    #overriding the equals methods
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]