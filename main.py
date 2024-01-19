import game,GUI
import pygame
from pygame.locals import *
import sys
import time
import copy




pygame.init()
lewa = 1
lewa_done = 0
atut_kwadrat = pygame.rect.Rect((198, 68), (104, 104))
bridge = pygame.rect.Rect((700, 250), (400, 400))
bridgev2 = pygame.rect.Rect((703, 253), (394, 394))
if_clicked = 1
clicked = 1
gra_active = 0
button_not_clicked = 0
font = pygame.font.Font('freesansbold.ttf', 18)
GREEN = (23, 117, 20)
DISPLAYSURF = pygame.display.set_mode((1800,900))
DISPLAYSURF.fill(GREEN)
FPS = pygame.time.Clock()
FPS.tick(10)

N = GUI.player_draw((710,150), 0, (100, 140), (850, 260), "N")
S = GUI.player_draw((710,750), 0, (100, 140), (850, 500), "S")
E = GUI.player_draw((1225, 640), 90, (140, 100), (940, 400), "E")
W = GUI.player_draw((560, 280), 90, (140, 100), (720, 400), "W")


f = 0
N_place = (0, 0)
change1 = (30,0)
change2 = (0,30)

#N.sort_hand()
#S.sort_hand()
#E.sort_hand()
#W.sort_hand()

#N_player = game.Player(game.convert_cards_to_num(["SA","SK","SQ","SW","ST","S9","S8","S7","S6","S5","S4","S3","S2"]))
#W_player = game.Player(game.convert_cards_to_num(["HA","HK","HQ","HW","HT","H9","H8","H7","H6","H5","H4","H3","H2"]))
#S_player = game.Player(game.convert_cards_to_num(["DA","DK","DQ","DW","DT","D9","D8","D7","D6","D5","D4","D3","D2"]))
#E_player = game.Player(game.convert_cards_to_num(["CA","CK","CQ","CW","CT","C9","C8","C7","C6","C5","C4","C3","C2"]))



main_game = game.Game(N_player=copy.copy(game.Player()),W_player=copy.copy(game.Player()),S_player=copy.copy(game.Player()),E_player=copy.copy(game.Player()))
main_game.setrandom()
N.update_hand(main_game.players[0].hand)
S.update_hand(main_game.players[2].hand)
E.update_hand(main_game.players[1].hand)
W.update_hand(main_game.players[3].hand)
my_button = GUI.Button('Rozdaj karty', 830, 420, True, (150,30), 18, 3, 3)
diamonds_button = GUI.Button('Diamonds', 715, 450, True, (75,75), 9,  15 ,63)
diamonds_icon = GUI.picture((50,50), (753, 480), "znaki\diamonds.png",0)
atut_diamonds_icon = GUI.picture((100,100), (250, 120), "znaki\diamonds.png",0)

hearts_button = GUI.Button('Hearts', 815, 450, True, (75,75), 9,  23, 63)
hearts_icon = GUI.picture((50,50), (853, 480), "znaki\hearts.png",0)
atut_hearts_icon = GUI.picture((100,100), (250, 120), "znaki\hearts.png",0)

spades_button = GUI.Button('Spades', 915, 450, True, (75,75), 9,  20 ,63)
spades_icon = GUI.picture((50,50), (953, 480), "znaki\spades.png",0)
atut_spades_icon = GUI.picture((100,100), (250, 120), "znaki\spades.png",0)


clubs_button = GUI.Button('Clubs', 1015, 450, True, (75,75), 9, 25 ,63)
clubs_icon = GUI.picture((50,50), (1053, 480), "znaki\clubs.png",0)
atut_clubs_icon = GUI.picture((100,100), (250, 120), "znaki\clubs.png",0)

komunikat_text = GUI.text(22, "Rozgrywajacy to South", (780, 300))
choose_text = GUI.text(22, "Wybierz z jakim atutem zagrasz: ", (720, 350))
atut = GUI.text(30, "Atut:", (100,100))

koncowy_komunikat = GUI.picture((250, 100), (900, 450), "komunikaty\komunikat.png", 0)

turn_arrow_N = GUI.picture((25,13), (900, 235), "znaki\strzalka.png", 90 )
turn_arrow_E = GUI.picture((25,13), (1120, 450), "znaki\strzalka.png", 0 )
turn_arrow_S = GUI.picture((25,13), (900, 665), "znaki\strzalka.png", 270 )
turn_arrow_W = GUI.picture((25,13), (680, 450), "znaki\strzalka.png", 180 )

main_game.on_move = 3



while True:
    lewy_text = GUI.text(20, f"Lewy S/N: {main_game.score} ", (715, 600))
    koncowy_wynik_EW = 13 - main_game.score
    koncowy_stan_gry = GUI.text(20, f"Lewy S/N: {main_game.score}, lewy W/E: {koncowy_wynik_EW}", (778,448))
    
    if gra_active == 1:
        lewy_text.write_text()
        if main_game.on_move == 0: #N
            pygame.draw.rect(DISPLAYSURF, GREEN , ((667, 444), (26,13)) , 0, 0) #W
            pygame.draw.rect(DISPLAYSURF, GREEN , ((1107, 444), (26,13)) , 0, 0) #E
            pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 652), (14,26)) , 0, 0) #S
            turn_arrow_N.draw_image() 
        if main_game.on_move == 1: #E
            pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 222), (14,26)) , 0, 0) #N
            pygame.draw.rect(DISPLAYSURF, GREEN , ((667, 444), (26,13)) , 0, 0) #W
            pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 652), (14,26)) , 0, 0) #S
            turn_arrow_E.draw_image()
        if main_game.on_move == 2: #S
            pygame.draw.rect(DISPLAYSURF, GREEN , ((1107, 444), (26,13)) , 0, 0) #E
            pygame.draw.rect(DISPLAYSURF, GREEN , ((667, 444), (26,13)) , 0, 0) #W
            pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 222), (14,26)) , 0, 0) #N
            turn_arrow_S.draw_image()
        if main_game.on_move == 3: #W
            pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 652), (14,26)) , 0, 0) #S
            pygame.draw.rect(DISPLAYSURF, GREEN , ((1107, 444), (26,13)) , 0, 0) #E
            pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 222), (14,26)) , 0, 0) #N
            turn_arrow_W.draw_image() 

    mx, my = pygame.mouse.get_pos()
    
    pygame.draw.rect(DISPLAYSURF, 'black' , bridge , 2, 5)
    
    if button_not_clicked == 0:
        komunikat_text.write_text()
        choose_text.write_text()
        diamonds_button.draw_button()
        diamonds_icon.draw_image()
        hearts_button.draw_button()
        hearts_icon.draw_image()
        spades_button.draw_button()
        spades_icon.draw_image()
        clubs_button.draw_button()
        clubs_icon.draw_image()
        atut.write_text()
        pygame.draw.rect(DISPLAYSURF, 'black' , atut_kwadrat , 0, 0)
        if diamonds_button.check_click():
            atut_diamonds_icon.draw_image()
            pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
            button_not_clicked = 1
            main_game.alert = 200
            time.sleep(0.2)
        elif clubs_button.check_click():
            atut_clubs_icon.draw_image()
            pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
            button_not_clicked = 1
            main_game.alert = 100
            time.sleep(0.2)
        elif hearts_button.check_click():
            atut_hearts_icon.draw_image()
            pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
            button_not_clicked = 1
            main_game.alert = 300
            time.sleep(0.2)
        elif spades_button.check_click():
            atut_spades_icon.draw_image()
            time.sleep(0.2)
            pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
            main_game.alert = 400
            button_not_clicked = 1

        


    if ((N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn)%4) == 0 and (N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn) > 3 and lewa_done == 1:
        print(winner)
        lewa_done = 0
        time.sleep(1)
        if winner == 2:
            S.winning_display()
        elif winner == 3:
            W.winning_display()
        elif winner == 1:
            E.winning_display()
        elif winner == 0:
            N.winning_display()
        pygame.display.update()
        time.sleep(2)
        pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
    if ((N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn)%52) == 0 and (N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn) > 51: 
        pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
        koncowy_komunikat.draw_image()
        koncowy_stan_gry.write_text()
        pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 652), (14,26)) , 0, 0) #S
        pygame.draw.rect(DISPLAYSURF, GREEN , ((1107, 444), (26,13)) , 0, 0) #E
        pygame.draw.rect(DISPLAYSURF, GREEN , ((894, 222), (14,26)) , 0, 0) #N
        pygame.draw.rect(DISPLAYSURF, GREEN , ((667, 444), (26,13)) , 0, 0) #W
        pygame.display.update()
        time.sleep(3)
        pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
        N = GUI.player_draw((710,150), 0, (100, 140), (850, 260), "N")
        S = GUI.player_draw((710,750), 0, (100, 140), (850, 500), "S")
        E = GUI.player_draw((1225, 640), 90, (140, 100), (940, 400), "E")
        W = GUI.player_draw((560, 280), 90, (140, 100), (720, 400), "W")
        main_game = game.Game(N_player=copy.copy(game.Player()),W_player=copy.copy(game.Player()),S_player=copy.copy(game.Player()),E_player=copy.copy(game.Player()))
        main_game.setrandom()
        N.update_hand(main_game.players[0].hand)
        S.update_hand(main_game.players[2].hand)
        E.update_hand(main_game.players[1].hand)
        W.update_hand(main_game.players[3].hand)
        if_clicked = 1
        gra_active = 0
        button_not_clicked = 0
        main_game.on_move = 3
        
        


        
        #N.hand()
        #S.hand()
        #E.hand()
        #W.hand()
        #N.sort_hand()
        #S.sort_hand()
        #E.sort_hand()
        #W.sort_hand()
    
    
    if button_not_clicked == 1:
        my_button.draw_button()
        if (my_button.check_click()) and if_clicked == 1:
            pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
            gra_active = 1
            for g in main_game.players[0].hand:
                
                N.card(g, tuple(x - y for x, y in zip(N.position, N_place)), "N")
                N.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change1))
                
            N_place = (0, 0)
            
            for g in main_game.players[2].hand:
        
                S.card(g, tuple(x - y for x, y in zip(S.position, N_place)), "S")
                S.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change1))
                
            N_place = (0, 0)
            
            for g in main_game.players[1].hand:
        
                E.card(g, tuple(x + y for x, y in zip(E.position, N_place)), "E")
                E.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change2))
            
            N_place = (0, 0)
            
            for g in main_game.players[3].hand:
        
                W.card(g, tuple(x - y for x, y in zip(W.position, N_place)), "W")
                W.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change2))
            time.sleep(0.2)   
            N_place = (0, 0)
            button_not_clicked = 2
    if main_game.on_move == 0 and gra_active == 1:
        possible = main_game.players[0].possible_moves(main_game.main_color)
        
        if N.card_click_check((660,80), (len(main_game.players[0].hand)*30)+70, 140):
            
            time.sleep(0.3)
            card_clicked = N.which_card_clicked(main_game.on_move) 
           
            if card_clicked in possible:
                N.cards_pos = []
                N.cards_drawn += 1
                #for card_drawn in main_game.players[0].hand:    
                    #if card_clicked == card_drawn:
                        
                N.draw_on_table(card_clicked, main_game.on_move)
                pygame.draw.rect(DISPLAYSURF, GREEN , N.card_hitbox , 0, 0)

                winner = main_game.make_move(main_game.players[0].hand.index(card_clicked))
                print(winner)
                
                

                
                for karta in main_game.players[0].hand: #to rysuje nowa reke
                    N.card(karta, tuple(x - y for x, y in zip(N.position, N_place)), "N")
                    N.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change1))
                N_place = (0, 0)
                
                time.sleep(0.2)
                
                lewa_done = 1
                #GUI.player_draw.CURRENTLY_PLAYING = "E"
            
            
    elif main_game.on_move == 2 and gra_active == 1: 
        possible = main_game.players[2].possible_moves(main_game.main_color)  
        if S.card_click_check((660,680), (len(main_game.players[2].hand)*30)+70, 140):
            
            
            card_clicked = S.which_card_clicked(main_game.on_move)
           
            time.sleep(0.3)

            if card_clicked in possible:
                S.cards_pos = []
                S.cards_drawn += 1
                #for card_drawn in main_game.players[2].hand:    
                    #if card_clicked == card_drawn:
                        
                S.draw_on_table(card_clicked, main_game.on_move)
                pygame.draw.rect(DISPLAYSURF, GREEN , S.card_hitbox , 0, 0)
                winner = main_game.make_move(main_game.players[2].hand.index(card_clicked))
                print(winner)
               
                #tutaj update renki
                
                for karta in main_game.players[2].hand:
                    S.card(karta, tuple(x - y for x, y in zip(S.position, N_place)), "S")
                    S.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change1))
                N_place = (0, 0)
                time.sleep(0.2)
                
                #GUI.player_draw.CURRENTLY_PLAYING = "W"
                lewa_done = 1
           
    elif main_game.on_move == 3 and gra_active == 1:
        possible = main_game.players[3].possible_moves(main_game.main_color)
        if W.card_click_check((490, 230), 140, (len(main_game.players[3].hand)*30)+70) :
            time.sleep(0.3)
            card_clicked = W.which_card_clicked(main_game.on_move)
            
            
            if card_clicked in possible:
                W.cards_pos = []
                W.cards_drawn += 1
                
                #for card_drawn in main_game.players[3].hand:    
                    #if card_clicked == card_drawn:
                        
                W.draw_on_table(card_clicked, main_game.on_move)
                pygame.draw.rect(DISPLAYSURF, GREEN , W.card_hitbox , 0, 0)
                winner = main_game.make_move(main_game.players[3].hand.index(card_clicked))
                print(winner)
                
                #tutaj update renki
                
                for karta in main_game.players[3].hand:
                    W.card(karta, tuple(x - y for x, y in zip(W.position, N_place)), "W")
                    W.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change2))
                N_place = (0, 0)
                time.sleep(0.2)
                
                #GUI.player_draw.CURRENTLY_PLAYING = "N"
                lewa_done = 1
            
    elif main_game.on_move == 1 and gra_active == 1:
        possible = main_game.players[1].possible_moves(main_game.main_color)
        if E.card_click_check((1155, 230+(E.cards_drawn*30)), 140, (len(main_game.players[1].hand)*30)+70):
            
            time.sleep(0.3)
            card_clicked = E.which_card_clicked(main_game.on_move)
            
            if card_clicked in possible:
                E.cards_pos = []
                E.cards_drawn += 1
                #for card_drawn in main_game.players[1].hand:    
                    #if card_clicked == card_drawn:
                        
                E.draw_on_table(card_clicked, main_game.on_move)
                pygame.draw.rect(DISPLAYSURF, GREEN , E.card_hitbox , 0, 0)
                winner = main_game.make_move(main_game.players[1].hand.index(card_clicked))
                print(winner)
               
                #tutaj update renki
                
                for karta in main_game.players[1].hand:
                    E.card(karta, tuple(x + y for x, y in zip(E.position, N_place)), "E")
                    E.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change2))
                N_place = (0, 0)
                time.sleep(0.2)
                
                #GUI.player_draw.CURRENTLY_PLAYING = "S"
                lewa_done = 1
        
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()      
    
          
    pygame.display.update()
