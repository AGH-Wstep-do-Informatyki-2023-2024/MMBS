import game,GUI
import pygame
from pygame.locals import *
import sys
import random
import time





pygame.init()
lewa = 1
lewa_done = 0
bridge = pygame.rect.Rect((700, 250), (400, 400))
bridgev2 = pygame.rect.Rect((703, 253), (394, 394))
if_clicked = 1
clicked = 1
gra_active = 0
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
N.hand()
S.hand()
E.hand()
W.hand()
N.sort_hand()
S.sort_hand()
E.sort_hand()
W.sort_hand()




N_player = game.Player(game.convert_cards_to_num(["SA","SK","SQ","SW","ST","S9","S8","S7","S6","S5","S4","S3","S2"]))
W_player = game.Player(game.convert_cards_to_num(["HA","HK","HQ","HW","HT","H9","H8","H7","H6","H5","H4","H3","H2"]))
S_player = game.Player(game.convert_cards_to_num(["DA","DK","DQ","DW","DT","D9","D8","D7","D6","D5","D4","D3","D2"]))
E_player = game.Player(game.convert_cards_to_num(["CA","CK","CQ","CW","CT","C9","C8","C7","C6","C5","C4","C3","C2"]))
main_game = game.Game(N_player,W_player,S_player,E_player)



while True:
    my_button = GUI.Button('Rozdaj karty', 100, 100, True)
    mx, my = pygame.mouse.get_pos()
    
    pygame.draw.rect(DISPLAYSURF, 'black' , bridge , 2, 5)
    
    if ((N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn)%4) == 0 and (N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn) > 3 and lewa_done == 1:
        lewa_done = 0
        time.sleep(1)
        #wyswietlanie wygranego do zrobienia tutaj i licznik punktow, gui gotowe
        winner = GUI.player_draw.PLAYERS[random.randint(0,3)]
        if winner == "S":
            S.winning_display()
        if winner == "W":
            W.winning_display()
        if winner == "E":
            E.winning_display()
        if winner == "N":
            N.winning_display()
        pygame.display.update()
        time.sleep(2)
        pygame.draw.rect(DISPLAYSURF, GREEN , bridgev2 , 0, 0)
    if ((N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn)%52) == 0 and (N.cards_drawn + W.cards_drawn + E.cards_drawn + S.cards_drawn) > 51: 
        GUI.player_draw.USED_CARDS = []
        N = GUI.player_draw((710,150), 0, (100, 140), (850, 260), "N")
        S = GUI.player_draw((710,750), 0, (100, 140), (850, 500), "S")
        E = GUI.player_draw((1225, 640), 90, (140, 100), (940, 400), "E")
        W = GUI.player_draw((560, 280), 90, (140, 100), (720, 400), "W")
        if_clicked = 1
        gra_active = 0
        N.hand()
        S.hand()
        E.hand()
        W.hand()
        N.sort_hand()
        S.sort_hand()
        E.sort_hand()
        W.sort_hand()
    
    
    
    if (my_button.check_click()) and if_clicked == 1:
            gra_active = 1
            for g in N_player.hand:
                
                N.card(g, tuple(x - y for x, y in zip(N.position, N_place)), "N")
                N.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change1))
                
            N_place = (0, 0)
            
            for g in S_player.hand:
        
                S.card(g, tuple(x - y for x, y in zip(S.position, N_place)), "S")
                S.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change1))
                
            N_place = (0, 0)
            
            for g in E_player.hand:
        
                E.card(g, tuple(x + y for x, y in zip(E.position, N_place)), "E")
                E.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change2))
               
            N_place = (0, 0)
            
            for g in W_player.hand:
        
                W.card(g, tuple(x - y for x, y in zip(W.position, N_place)), "W")
                W.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change2))
            time.sleep(0.2)   
            N_place = (0, 0)
    if GUI.player_draw.CURRENTLY_PLAYING == "N" and gra_active == 1:
        if N.card_click_check((660,80), (len(N.hand)*30)+70, 140) and clicked == 1 :
            
            clicked = 0
            card_clicked = N.which_card_clicked() 
            for card_drawn in N.hand:    
                if card_clicked == card_drawn:
                    
                    N.draw_on_table(card_drawn, N.hand.index(card_drawn))
                    pygame.draw.rect(DISPLAYSURF, GREEN , N.card_hitbox , 0, 0)
                    N_place = (0, 0)
                    for karta in N.hand:
                        N.card(karta, tuple(x - y for x, y in zip(N.position, N_place)), "N")
                        N.draw(DISPLAYSURF)
                        N_place = tuple(x - y for x, y in zip(N_place, change1))
                    N_place = (0, 0)
            time.sleep(0.2)
            clicked = 1
            GUI.player_draw.CURRENTLY_PLAYING = "E"
            lewa_done = 1
            
    elif GUI.player_draw.CURRENTLY_PLAYING == "S" and gra_active == 1:   
        if S.card_click_check((660,680), (len(S.hand)*30)+70, 140) and clicked == 1 :
            
            clicked = 0
            card_clicked = S.which_card_clicked() 
            for card_drawn in S_player.hand:    
                if card_clicked == card_drawn:
                    
                    S.draw_on_table(card_drawn, S.hand.index(card_drawn))
                    pygame.draw.rect(DISPLAYSURF, GREEN , S.card_hitbox , 0, 0)
                    N_place = (0, 0)
                    for karta in S_player.hand:
                        S.card(karta, tuple(x - y for x, y in zip(S.position, N_place)), "S")
                        S.draw(DISPLAYSURF)
                        N_place = tuple(x - y for x, y in zip(N_place, change1))
                    N_place = (0, 0)
            time.sleep(0.2)
            clicked = 1
            GUI.player_draw.CURRENTLY_PLAYING = "W"
            lewa_done = 1
           
    elif GUI.player_draw.CURRENTLY_PLAYING == "W" and gra_active == 1:
        if W.card_click_check((490, 230), 140, (len(W.hand)*30)+70) and clicked == 1 :
            clicked = 0
            
            card_clicked = W.which_card_clicked() 
            for card_drawn in W.hand:    
                if card_clicked == card_drawn:
                    
                    W.draw_on_table(card_drawn, W.hand.index(card_drawn))
                    pygame.draw.rect(DISPLAYSURF, GREEN , W.card_hitbox , 0, 0)
                    N_place = (0, 0)
                    for karta in W.hand:
                        W.card(karta, tuple(x - y for x, y in zip(W.position, N_place)), "W")
                        W.draw(DISPLAYSURF)
                        N_place = tuple(x - y for x, y in zip(N_place, change2))
                    N_place = (0, 0)
            time.sleep(0.2)
            clicked = 1
            GUI.player_draw.CURRENTLY_PLAYING = "N"
            lewa_done = 1
            
    elif GUI.player_draw.CURRENTLY_PLAYING == "E" and gra_active == 1:
        if E.card_click_check((1155, 230+(E.cards_drawn*30)), 140, (len(E.hand)*30)+70) and clicked == 1 :
            
            clicked = 0
            card_clicked = E.which_card_clicked()
             
            for card_drawn in E.hand:    
                if card_clicked == card_drawn:
                    
                    E.draw_on_table(card_drawn, E.hand.index(card_drawn))
                    pygame.draw.rect(DISPLAYSURF, GREEN , E.card_hitbox , 0, 0)
                    N_place = (0, 0)
                    for karta in E.hand:
                        E.card(karta, tuple(x + y for x, y in zip(E.position, N_place)), "E")
                        E.draw(DISPLAYSURF)
                        N_place = tuple(x - y for x, y in zip(N_place, change2))
                    N_place = (0, 0)
            time.sleep(0.2)
            clicked = 1
            GUI.player_draw.CURRENTLY_PLAYING = "S"
            lewa_done = 1
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()      
    
          
    pygame.display.update()
