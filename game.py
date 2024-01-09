'''
kolory:
S (Spades) - 400
H (hearts) - 300
D (diamonds) - 200
C (clubs) - 100
NA (non alert) - 000

Karty:
A -14
K -13 
Q -12
W -11
T -10
9 -09
8 -08
7 -07
6 -06
5 -05
4 -04
3 -03
2 -02

np. S9 - 409 , HT - 310

kontrakty:
kolor + ilosc
np H6 - 306
'''
import copy,time,random,math
import ai 

def draw_encoded(encoded):
    print(encoded[0:2])
    print(encoded[2:15])
    print(encoded[15:28])
    print(encoded[28:41])
    print(encoded[41:54])

def convert_cards_to_num(cards):
    res=[]
    for card in cards:
        r=0
        if card[0]=='S':
            r+=400
        elif card[0]=='H':
            r+=300
        elif card[0]=='D':
            r+=200
        else:#card[0]=='C':
            r+=100
        
        if card[1]=='A':
            r+=14
        elif card[1]=='K':
            r+=13
        elif card[1]=='Q':
            r+=12
        elif card[1]=='W':
            r+=11
        elif card[1]=='T':
            r+=10
        else:    
            r+=int(card[1])%100
        res.append(r)
    return res

class Player:
    def __init__ (self, card=[]):
        card.sort(reverse=True)
        self.hand=card.copy()

    #wypisuje karty
    def print_hand(self):
        for i in self.hand:
            print(i, end= " ")
        print()

    def add_card(self,card):
        self.hand.append(card)
        
    
    #zwraca liste możliwych ruchow
    def possible_moves(self, color=0):
        res=[]
        for i in self.hand:
            if i//100 == color//100:
                res.append(i)
        if res:
            return res
        return self.hand

#klasa zawierająca aktualną pozycje gry 
class Game:
    def __init__(self, north=copy.copy(Player()), west=copy.copy(Player()), south=copy.copy(Player()), east=copy.copy(Player()), on_move=0, alert=0, score=0):
        self.players =[north, east, south, west]    
        self.on_move = on_move  # kto jest na ruchu
        self.alert = alert      # atut
        self.score = score      # aktualny wynik - ilosc wygranych NS
        self.mid = []           # karty na srodku 
        self.to_end = len(north.hand)+len(west.hand)+len(south.hand)+len(east.hand)       # ilosc rund do konca
        self.main_color=0       # kolor 1. karty na srodku


    
    #ustawia losowa pozycje
    def setrandom(self,alert=-1, onmove=-1):
        if alert==-1:
            self.alert= random.randint(0,4)*100
        elif alert<=4 and alert>=0:
            self.alert=alert*100
        elif alert==100 or alert==200 or alert==300 or alert==400:
            self.alert-alert
        else:
            return
            
        if onmove==-1:
            self.on_move=random.randint(0,3)
        elif onmove<=3 and onmove>=0:
            self.on_move=onmove
        else:
            return
        left=[]
        for i in range(1,5):
            for j in range(2,15):
                left.append(i*100 + j)
        for j in range(0,4):
            for i in range(0,13):
                card = left[random.randint(0,len(left)-1)] 
                self.players[j].hand.append(card)
                left.remove(card)
        self.to_end=52
        
            
    
    #zwraca pozycje jako input do sieci neuronowej
    def encoded_position(self):
        table= [[self.alert//100],[self.on_move]]

        for k in range(1,5):
            for i in range(2,15):
                found=False
                card= k*100 + i
                for j in range(0,4):
                    if card in self.players[j].hand:
                        table.append([j])
                        found=True
                        break
                if card in self.mid:
                    table.append([5])
                    found=True
                if not found:
                    table.append([-1])
                
        return table
        
        
    #sprawdza kto wygral rozdanie zwraca gracza wygranego i aktualizuje wynik
    def eval_mid(self):
        self.main_color=0
        first = (self.on_move+1)%4
        possible_winners = []
        main_color = self.mid[0]//100

        ## sprawdzenie atutu
        for card in self.mid:
            if card//100 == self.alert//100:
                possible_winners.append(card)
        if len(possible_winners)!=0:
            best = max(possible_winners)
            winner = (self.mid.index(best)+first)%4
            self.on_move=winner
            if winner%2 == 0:
                self.score += 1
            return winner
        
        ## jesli nie ma atutu
        for card in self.mid:
            if card//100 == main_color:
                possible_winners.append(card)
        best = max(possible_winners)
        winner = (self.mid.index(best)+first)%4
        self.on_move=winner
        if winner%2 == 0:
            self.score += 1
        return winner
    
    
    # wykonuje ruch zwraca -1 jeśli się nie udało wykonać 0 jeśli ruch został wykonany 1 jeśli gra po ruchu się zakończyła 
    def make_move(self,index):
        moves = self.players[self.on_move].possible_moves(self.main_color)
        if index>=len(moves):
            return -1
        move = moves[index]
        self.mid.append(move)
        self.players[self.on_move].hand.remove(move)
        
        if len(self.mid)==4:
            self.eval_mid()
            self.mid.clear()
        else:
            self.on_move = (self.on_move+1)%4
        if len(self.mid)==1:
            self.main_color = (self.mid[0]//100)*100 
        self.to_end -=1
        if self.to_end ==0:
            return 1
        return 0
    
    def match(self,player1, player2):#player1 - NS player2 - WE
        while self.to_end>0:
            if self.on_move%2==0:
                player1.get_input(self.encoded_position())
                player1.eval()
                moves = self.players[self.on_move].possible_moves(self.main_color)
                move = player1.pick_best(len(moves))
                #print(move,moves[move])
                self.make_move(move)
            else:
                player2.get_input(self.encoded_position())
                player2.eval()
                moves = self.players[self.on_move].possible_moves(self.main_color)
                move = player2.pick_best(len(moves))
                #print(move,moves[move])
                self.make_move(move)
            #print(self.encoded_position())
            #self.info()
        return self.score

        
    
    def info(self):
        print("na_ruchu", self.on_move,"do konca:", self.to_end,"  aktualny wynik:", self.score)
        print("----------")
        
        
#----------------------------------------------------------------------





## min max wolne dobre do 4 kart xD
def simul(game): 
    moves = game.players[game.on_move].possible_moves(game.main_color)
    results = []
    i = 1
    for move in moves:
        game_copy = copy.deepcopy(game)
        game_copy.mid.append(move)
        prev=game_copy.on_move
        if len(game_copy.mid) == 4:
            game_copy.eval_mid()
            game_copy.mid.clear()
        else:
            game_copy.on_move = (game_copy.on_move+1)%4
        if len(game_copy.mid) == 1:
            game_copy.main_color =(game_copy.mid[0]//100)*100
        game_copy.players[prev].hand.remove(move)
        game_copy.to_end -= 1
        if game_copy.to_end == 0:
            results.append(game_copy.score)
        else:
            results.append(simul(game_copy))
        i+=1
    if game.on_move%2 ==0:
        return max(results)
    else:
        return min(results)
