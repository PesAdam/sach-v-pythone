#toto je file kde budeme tieto data ukladat, tiez ma nastarosti robit LEN validne pohyby
#tiez moove log

class GameState():
    def __init__(self):
        #mozno pouzit numpy array neskor, pre rychlost
        #board je 8*8 a kazdy list ma 2 charakterov, prvy reprezentuje farbu b - black, w-white
        #druhy charakter prezentuje o aku figurku ide
        # "--" reprezentuje prazdnu poziciu
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"]
        ]

        self.whiteToMove = True
        self.moveLog = []