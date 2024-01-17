import pygame
from pygame.locals import *
import sys
import random
import time
pygame.init()
bridge = pygame.rect.Rect((700, 250), (400, 400))
players_N_S = ['N', 'S']
players_E_W = ['E', 'W']
if_clicked = 1
clicked = 1
font = pygame.font.Font('freesansbold.ttf', 18)
GREEN = (23, 117, 20)
DISPLAYSURF = pygame.display.set_mode((1800,900))
DISPLAYSURF.fill(GREEN)
FPS = pygame.time.Clock()
FPS.tick(10)

class player:
    COLOR = ["H", "C", "D", "S"]
    VALUE = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    USED_CARDS = []
    
    def __init__(self, position, rotation, size, position_on_table):
        self.position = position
        self.position_on_table = position_on_table
        self.rotation = rotation
        self.size = size
        self.cards_pos = []
        self.cards_not_drawn = []
        
    
    def card(self, i, place, player_rn):
        self.image = pygame.image.load(f"E:\wstep_python\MMBS\karty\{i}.png")
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = place
        x, y = place
        print(player_rn)
        if player_rn == "N" or player_rn == "S":
            self.cards_pos = self.cards_pos + [x - 50]
        elif player_rn == "E":
            self.cards_pos = self.cards_pos + [y + 50]
        else:
            self.cards_pos = self.cards_pos + [y - 50]


    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(DISPLAYSURF, 'black' , self.rect , 1, 1)
    
    def hand(self):
        self.hand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0,13):
            flag = 0
            while flag == 0:
                self.hand[i] = player.COLOR[random.randint(0,3)] + player.VALUE[random.randint(0,12)]
                flag = 1
                for x in player.USED_CARDS:
                    if self.hand[i] == x:
                        flag = 0
            player.USED_CARDS.append(self.hand[i])
            self.cards_not_drawn.append(self.hand[i])
            
        
    
    def card_click_check(self, player_pos, hitbox_lengh, hitbox_width):
        global clicked
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        x_pos, y_pos = player_pos
        self.card_hitbox = pygame.rect.Rect((x_pos, y_pos), (hitbox_lengh, hitbox_width))
        if left_click and self.card_hitbox.collidepoint(mouse_pos):
            return True
        else:
            return False
        
        
    def which_card_clicked(self):
        
        mouse_pos = pygame.mouse.get_pos()
        
        x, y = mouse_pos
        h = 0
        for card_pos_x in self.cards_pos:
            if x - card_pos_x > 0 and x - card_pos_x < 30 :
                self.cards_pos = []
                
                return self.hand[h]
            
            h += 1

    def draw_on_table(self, card, h):
        image_on_table = pygame.image.load(f"E:\wstep_python\MMBS\karty\{card}.png")
        image_on_table = pygame.transform.scale(image_on_table, self.size)
        image_on_table = pygame.transform.rotate(image_on_table, self.rotation)
        rect = image_on_table.get_rect()
        rect.center = tuple(x + y for x, y in zip(self.position_on_table, (50,70)))
        DISPLAYSURF.blit(image_on_table, self.position_on_table)
        pygame.draw.rect(DISPLAYSURF, 'black' , rect , 1, 1)
        self.hand.remove(self.hand[h])
        
        




        
            
        

    

             



class Button:
    def __init__(self, text, x_pos, y_pos, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.draw_button()
        

    def draw_button(self):
        
        button_text = font.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150, 25))
        if self.check_click() or if_clicked == 0:
            pygame.draw.rect(DISPLAYSURF, GREEN , button_rect, 0, 5)
            pygame.draw.rect(DISPLAYSURF, GREEN , button_rect, 2, 5)
            button_text = font.render(self.text, True, GREEN)
            DISPLAYSURF.blit(button_text, (self.x_pos + 3, self.y_pos +3))

            
        else: 
            pygame.draw.rect(DISPLAYSURF, 'gray', button_rect, 0, 5)
            pygame.draw.rect(DISPLAYSURF, 'black', button_rect, 2, 5)
            

        DISPLAYSURF.blit(button_text, (self.x_pos + 3, self.y_pos +3))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150, 25))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False
        
    

                
                    
                        
                

            
            


N = player((710,150), 0, (100, 140), (850, 260))
S = player((710,750), 0, (100, 140), (850, 500))
E = player((1225, 640), 90, (140, 100), (900, 400))
W = player((560, 280), 90, (140, 100), (500, 400))


f = 0
N_place = (0, 0)
change1 = (30,0)
change2 = (0,30)
N.hand()

S.hand()
E.hand()
W.hand()




while True:
    my_button = Button('Rozdaj karty', 100, 100, True)
    mx, my = pygame.mouse.get_pos()
    
    pygame.draw.rect(DISPLAYSURF, 'black' , bridge , 2, 5)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if (my_button.check_click()) and if_clicked == 1:
            for g in N.hand:
                
                N.card(g, tuple(x - y for x, y in zip(N.position, N_place)), "N")
                N.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change1))
                
            N_place = (0, 0)
            
            for g in S.hand:
        
                S.card(g, tuple(x - y for x, y in zip(S.position, N_place)), "S")
                S.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change1))
                
            N_place = (0, 0)
            
            for g in E.hand:
        
                E.card(g, tuple(x + y for x, y in zip(E.position, N_place)), "E")
                E.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change2))
               
            N_place = (0, 0)
            
            for g in W.hand:
        
                W.card(g, tuple(x - y for x, y in zip(W.position, N_place)), "W")
                W.draw(DISPLAYSURF)
                N_place = tuple(x - y for x, y in zip(N_place, change2))
               
            N_place = (0, 0)
    
    if N.card_click_check((660,80), (len(N.hand)*30)+70, 140) and clicked == 1 :
        clicked = 0
        card_clicked = N.which_card_clicked() 
        for card_drawn in N.hand:    
            if card_clicked == card_drawn:
                print(N.hand.index(card_drawn))
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
    if S.card_click_check((660,680), (len(S.hand)*30)+70, 140) and clicked == 1 :
        clicked = 0
        card_clicked = S.which_card_clicked() 
        for card_drawn in S.hand:    
            if card_clicked == card_drawn:
                print(S.hand.index(card_drawn))
                S.draw_on_table(card_drawn, S.hand.index(card_drawn))
                pygame.draw.rect(DISPLAYSURF, GREEN , S.card_hitbox , 0, 0)
                N_place = (0, 0)
                for karta in S.hand:
                    S.card(karta, tuple(x - y for x, y in zip(S.position, N_place)), "S")
                    S.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change1))
                N_place = (0, 0)
        time.sleep(0.2)
        clicked = 1
    #fix the fucking W and E and u are good to go
    if W.card_click_check((430, 350), 100, (len(W.hand)*30)+70) and clicked == 1 :
        clicked = 0
        card_clicked = W.which_card_clicked() 
        for card_drawn in W.hand:    
            if card_clicked == card_drawn:
                print(W.hand.index(card_drawn))
                W.draw_on_table(card_drawn, W.hand.index(card_drawn))
                pygame.draw.rect(DISPLAYSURF, GREEN , W.card_hitbox , 0, 0)
                N_place = (0, 0)
                for karta in W.hand:
                    W.card(karta, tuple(x - y for x, y in zip(W.position, N_place)), "W")
                    W.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change1))
                N_place = (0, 0)
        time.sleep(0.2)
        clicked = 1
    if E.card_click_check((830, 350), 100, (len(E.hand)*30)+70) and clicked == 1 :
        clicked = 0
        card_clicked = E.which_card_clicked() 
        for card_drawn in E.hand:    
            if card_clicked == card_drawn:
                print(E.hand.index(card_drawn))
                E.draw_on_table(card_drawn, E.hand.index(card_drawn))
                pygame.draw.rect(DISPLAYSURF, GREEN , E.card_hitbox , 0, 0)
                N_place = (0, 0)
                for karta in E.hand:
                    E.card(karta, tuple(x - y for x, y in zip(E.position, N_place)), "E")
                    E.draw(DISPLAYSURF)
                    N_place = tuple(x - y for x, y in zip(N_place, change1))
                N_place = (0, 0)
        time.sleep(0.2)
        clicked = 1
        
    
                
                
                
    pygame.display.update()