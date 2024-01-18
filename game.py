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


import copy
import time
import random
import math
import ai


# wypisuje w "ładnej formie" pozycje w postaci tablicy (encoded)
def draw_encoded(encoded):
    print(encoded[0:2])
    print(encoded[2:15])
    print(encoded[15:28])
    print(encoded[28:41])
    print(encoded[41:54])


# pozwala wpisywać karty za pomocą normalnej konwencji i zamienia to na kod podany na początku
def convert_cards_to_num(cards):
    res = []
    for card in cards:
        r = 0
        if card[0] == 'S':
            r += 400
        elif card[0] == 'H':
            r += 300
        elif card[0] == 'D':
            r += 200
        else:  # card[0]=='C':
            r += 100

        if card[1] == 'A':
            r += 14
        elif card[1] == 'K':
            r += 13
        elif card[1] == 'Q':
            r += 12
        elif card[1] == 'W':
            r += 11
        elif card[1] == 'T':
            r += 10
        else:
            r += int(card[1]) % 100
        res.append(r)
    return res


class Player:
    # klasa gracza
    # hand - tablica zawierajaca karty na ręce gracza

    def __init__(self, card=[]):
        card.sort(reverse=True)
        self.hand = card.copy()

    # wypisuje karty
    def print_hand(self):
        for i in self.hand:
            print(i, end=" ")
        print()

    def add_card(self, card):
        self.hand.append(card)

    # zwraca liste możliwych ruchow gdzie "color" ozncza kolor pierwszej karty, która była zagrana w danej lewie

    def possible_moves(self, color=0):
        res = []
        for i in self.hand:
            if i//100 == color//100:
                res.append(i)
        if res:
            return res
        return self.hand


# klasa zawierająca aktualną pozycje gry
class Game:
    # players - lista graczy (obiektów klasy Player) kolejne indeksy to north, east, south, west
    # on_move - kto jest na ruchu
    # alert - atutowy kolor w postaci 0/100/200/300/400
    # score - aktualny wynik pary NS (wynik pary EW po skonczonej grze to 13 - score)
    # mid - tablica przechowujaca karty ktore zostały zagrane w tej lewie
    # to_end - ilosc kart która nie zostały jeszcze zagrane
    # main_color - kolor 1. karty na środku
    def __init__(self, N_player=copy.copy(Player()), W_player=copy.copy(Player()), S_player=copy.copy(Player()), E_player=copy.copy(Player()), on_move=0, alert=0, score=0):
        self.players = [N_player, W_player, S_player, E_player]
        self.on_move = on_move  # kto jest na ruchu
        self.alert = alert      # atut
        self.score = score      # aktualny wynik - ilosc wygranych NS
        self.mid = []           # karty na srodku
        self.to_end = len(N_player.hand)+len(W_player.hand)+len(S_player.hand) + len(E_player.hand)       # ilosc rund do konca
        self.main_color = 0       # kolor 1. karty na srodku

    # ustawia losowa pozycje

    def setrandom(self, alert=-1, onmove=-1):
        if alert == -1:
            self.alert = random.randint(0, 4)*100
        elif alert <= 4 and alert >= 0:
            self.alert = alert*100
        elif alert == 100 or alert == 200 or alert == 300 or alert == 400:
            self.alert-alert
        else:
            return

        if onmove == -1:
            self.on_move = random.randint(0, 3)
        elif onmove <= 3 and onmove >= 0:
            self.on_move = onmove
        else:
            return
        left = []
        for i in range(1, 5):
            for j in range(2, 15):
                left.append(i*100 + j)
        for j in range(0, 4):
            for i in range(0, 13):
                card = left[random.randint(0, len(left)-1)]
                self.players[j].hand.append(card)
                left.remove(card)
        self.to_end = 52
        for k in range(0,4):
            self.players[k].hand = sorted(self.players[k].hand, reverse=True)

    # zamienia pozycje w postaci klasy Game do tablicy postaci [atut/100, on_move, i położenie 52 kart ( -1 została zagrana, 0-N, 1-E, 2-S, 3-W, 5- na środku ) w kolejnosci 2-A i C->D->H->S]

    def encoded_position(self):
        table = [[self.alert//100], [self.on_move]]

        for k in range(1, 5):
            for i in range(2, 15):
                found = False
                card = k*100 + i
                for j in range(0, 4):
                    if card in self.players[j].hand:
                        table.append([j])
                        found = True
                        break
                if card in self.mid:
                    table.append([5])
                    found = True
                if not found:
                    table.append([-1])

        return table

    # sprawdza kto wygral rozdanie zwraca gracza wygranego i aktualizuje wynik

    def eval_mid(self):
        self.main_color = 0
        first = (self.on_move+1) % 4
        possible_winners = []
        main_color = self.mid[0] // 100
        

        # sprawdzenie atutu
        """
        for card in self.mid:
            if card//100 == self.alert//100:
                possible_winners.append(card)
        if len(possible_winners) != 0:
            best = max(possible_winners)
            winner = (self.mid.index(best)+first) % 4
            self.on_move = winner
            if winner % 2 == 0:
                self.score += 1
            return winner
        """

        # jesli nie ma atutu
        for card in self.mid:
            if card//100 == main_color:
                possible_winners.append(card)
        best = max(possible_winners)
        winner = (self.mid.index(best)+first) % 4
        
        self.on_move = winner
        if winner % 2 == 0:
            self.score += 1
        return winner

    # wykonuje ruch zwraca -1 jeśli się nie udało wykonać 0 jeśli ruch został wykonany 1 jeśli gra po ruchu się zakończyła
    #najwazniejsza funkcja (grajaca)

    def make_move(self, index):
        moves = self.players[self.on_move].possible_moves(self.main_color)
        print(moves)
        #if index >= len(moves):
            #return -1
        move = self.players[self.on_move].hand[index] #move = moves[index]
        
        self.mid.append(move)
        
        self.players[self.on_move].hand.remove(move)

        if len(self.mid) == 4:
            winner = self.eval_mid()
            self.mid.clear()
            return winner
        else:
            self.on_move = (self.on_move+1) % 4
        if len(self.mid) == 1:
            self.main_color = (self.mid[0]//100)*100
        self.to_end -= 1
        if self.to_end == 0:
            return 1
        return 0

    # rozgrywa aktualną pozycje za pomocą 2 sieci neuronowych
    def match(self, player1, player2):  # player1 - NS player2 - WE
        while self.to_end > 0:
            if self.on_move % 2 == 0:
                player1.get_input(self.encoded_position())
                player1.eval()
                moves = self.players[self.on_move].possible_moves(
                    self.main_color)
                move = player1.pick_best(len(moves))
                # print(move,moves[move])
                self.make_move(move)
            else:
                player2.get_input(self.encoded_position())
                player2.eval()
                moves = self.players[self.on_move].possible_moves(
                    self.main_color)
                move = player2.pick_best(len(moves))
                # print(move,moves[move])
                self.make_move(move)
            # print(self.encoded_position())
            # self.info()
        return self.score

    # wypisuje basic info o danej pozycji

    def info(self):
        print("na_ruchu", self.on_move, "do konca:",
              self.to_end, "  aktualny wynik:", self.score)
        print("----------")


# ----------------------------------------------------------------------


# min max wolne dobre do 4 kart xD
def simul(game):
    moves = game.players[game.on_move].possible_moves(game.main_color)
    results = []
    i = 1
    for move in moves:
        game_copy = copy.deepcopy(game)
        game_copy.mid.append(move)
        prev = game_copy.on_move
        if len(game_copy.mid) == 4:
            game_copy.eval_mid()
            game_copy.mid.clear()
        else:
            game_copy.on_move = (game_copy.on_move+1) % 4
        if len(game_copy.mid) == 1:
            game_copy.main_color = (game_copy.mid[0]//100)*100
        game_copy.players[prev].hand.remove(move)
        game_copy.to_end -= 1
        if game_copy.to_end == 0:
            results.append(game_copy.score)
        else:
            results.append(simul(game_copy))
        i += 1
    if game.on_move % 2 == 0:
        return max(results)
    else:
        return min(results)


'''
losowy kod który jest useless ale pokazuje jak można używać niektórych funkcji
s = Player(convert_cards_to_num(['HK','HT','H6','H3']))
w = Player(convert_cards_to_num(['HQ','H7','H4','H2']))
n = Player(convert_cards_to_num(['H9','CW','C6','C4']))
e = Player(convert_cards_to_num(['HA','HW','H8','H5']))

#draw_encoded(game3.encoded_position())

game = copy.deepcopy(Game(n,e,s,w,0,0))
game2= copy.deepcopy(Game(n,e,s,w,0,0))
agent = copy.deepcopy(ai.Neural_network())
agent.setrandom(54,13)
agent2 = copy.deepcopy(ai.Neural_network())
agent2.setrandom(54,13)

#print(game.match(agent,agent2))
#print(game2.match(agent,agent2))
'''
'''
scores=0
N=10
watch=time.time()
to_update=3
for i in range(0,N):
    game3=copy.deepcopy(Game())
    game3.setrandom()
    game4=copy.deepcopy(game3)
    s1=game3.match(agent,agent2)
    s2=game4.match(agent2,agent)
    res = s1-s2 # jesli s1 > s2 to agent1>agent2
    scores+=res
    if time.time()-watch>to_update:
        print('%.1f'%(i*100/N),end="%\n" )
        to_update+=3
print(scores, " time: ", '%.3f'%(time.time()-watch,) )
'''
'''
gen = ai.Generation(100)
gen.draw()
'''
