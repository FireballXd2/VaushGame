import pygame
import math
import random
import sys
import os
import winsound
import time
import pickle
 
class enemy(object):
    def ishit(self):
        return person.get_rect(center =(self.x_pos+42.5,self.y_pos+42.5))
        
    def __init__(self,x,y):
        self.x_pos = x
        self.y_pos = y
    def spawn(self):
        screen.blit(person,(self.x_pos,self.y_pos))
              
pygame.init()

Width = 800
Height = 600
Background = (225,179,120)

vaush_xpos = 400
vaush_ypos = 300
vaush_size = 50

person = pygame.image.load("Timpoll.jpg")
vaush = pygame.image.load("Simple.png")
Gun   = pygame.image.load("Gun.png")
O_Gun = pygame.image.load("Gun.png")
Start = pygame.image.load("VaushPlay.png")
EndScreen = pygame.image.load("GameOver.png")
Gun_rect = Gun.get_rect(center=(vaush_xpos+50,vaush_ypos+55))
Bullet_Sound = pygame.mixer.Sound("Firing.wav")
ShotFired = -69420
current_time =0
vaush_speed = 0.5
EnemySpawned = -8000
pressedKeys = {"Left" : False, "Right" : False, "Up": False, "Down": False}
Alive_enemies = []
Diff = 8500
Kills = 0
myFont = pygame.font.SysFont("Times New Roman", 18)
GameStarted = False
pygame.display.set_caption("Vaush")
icon = pygame.image.load("Vaush.png")
pygame.display.set_icon(icon)


screen = pygame.display.set_mode((Width,Height))

game_over = False
clock = pygame.time.Clock()
angle = 1

def reload():
    pygame.draw.rect(screen,(0,255,0),[680,570,(current_time-ShotFired)/10,15])

def player():
    screen.blit(Gun,Gun_rect)
    screen.blit(vaush,(vaush_xpos-100,vaush_ypos-55))
#Draws the player

def Choose():
    screen.blit(Start,(200,228))
       
while not game_over:
    if GameStarted:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #Quiting the game 

            elif event.type == pygame.KEYDOWN:                       
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pressedKeys["Right"] = True                               
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:        
                    pressedKeys["Left"]  = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pressedKeys["Up"] = True                
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:        
                    pressedKeys["Down"]  = True                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pressedKeys["Right"] = False                
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:        
                    pressedKeys["Left"]  = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pressedKeys["Up"] = False                
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:        
                    pressedKeys["Down"]  = False 
            #Moving the guy   
                        
        if pressedKeys["Right"]:
            if vaush_xpos<770:
                vaush_xpos+=vaush_speed    
        if pressedKeys["Left"]:
            if vaush_xpos>-30:
                vaush_xpos-=vaush_speed           
        if pressedKeys["Up"]:
            if vaush_ypos>-30:
                vaush_ypos-=vaush_speed     
        if pressedKeys["Down"]:
            if vaush_ypos<560:
                vaush_ypos+=vaush_speed    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ShotFired < current_time-1000:
                Bullet_Sound.play()        
                if(len(Alive_enemies)>0):
                    x, y = pygame.mouse.get_pos() 
                    #print("works")
                    for i in range(0,len(Alive_enemies)):
                        if(Alive_enemies[i].ishit().collidepoint(x,y)):
                            Alive_enemies.pop(i)  
                            Kills +=1                                                         
                            break
                ShotFired = current_time         
    
        Gun_rect = Gun.get_rect(center=(vaush_xpos+50,vaush_ypos+55))
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - Gun_rect.centerx, my - Gun_rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  -211 
        Gun = pygame.transform.rotate(O_Gun,angle) 
    
        current_time = pygame.time.get_ticks()
        clock.tick(1000)
        
        screen.fill(Background)
        
        if ShotFired > current_time-1000:
            reload() 
        if EnemySpawned < current_time-Diff and len(Alive_enemies)<12:
            for i in range(1,9):
                d= random.random() 
                assign_x = random.random()*700
                assign_y = random.random()*500
                if(d>0.75):
                    assign_x+=700
                elif(d>0.5):
                    assign_x-=700
                elif(d>0.25):
                    assign_y+=700 
                else:
                    assign_y-=700  
                Alive_enemies.append(enemy(assign_x,assign_y))  
        
            EnemySpawned = current_time
            
        for i in range(0,len(Alive_enemies)):
            Alive_enemies[i].spawn()
            
        for i in range(0,len(Alive_enemies)):
            if(Alive_enemies[i].x_pos<vaush_xpos):
                Alive_enemies[i].x_pos+=0.25
            elif(Alive_enemies[i].x_pos>vaush_xpos):
                Alive_enemies[i].x_pos-=0.25
            if(Alive_enemies[i].y_pos<vaush_ypos):
                Alive_enemies[i].y_pos+=0.25
            elif(Alive_enemies[i].y_pos>vaush_ypos):
                Alive_enemies[i].y_pos-=0.25
                
        for i in range(0,len(Alive_enemies)):
            b1 = Alive_enemies[i]
            if(math.sqrt(math.pow(b1.x_pos-vaush_xpos,2)+math.pow(b1.y_pos-vaush_ypos,2))<35):
                if Kills > pickle.load(open("HighScore.txt","rb")):
                    pickle.dump(Kills,open("HighScore.txt","wb"))
                    print(pickle.load(open("HighScore.txt","rb")))              
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                    screen.fill((0,0,0))    
                    screen.blit(EndScreen,(260,227.5))
                    KillLabel = myFont.render(str(Kills),1,(0,0,0))
                    screen.blit(KillLabel,(395-3*str(Kills).__len__(),295)) 
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()
                        if(math.sqrt(math.pow(x-395,2)+math.pow(y-315,2))<30):                         
                            sys.exit()
                
        
            
        KillLabel = myFont.render(str(Kills),1,(0,0,0))
        screen.blit(KillLabel,(10,10))    
        player()  
        pygame.display.update()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        Choose()
        High = str(pickle.load(open("HighScore.txt","rb")))
        KillLabel = myFont.render(High,1,(0,0,0))
        screen.blit(KillLabel,(384-3*High.__len__(),280))
        
        if(Diff==8500):
            pygame.draw.rect(screen,(255,0,0),(375,335,25,25))
        elif(Diff==9000):
            pygame.draw.rect(screen,(255,0,0),(248,335,25,25))
        elif(Diff==8100):
            pygame.draw.rect(screen,(255,0,0),(515,335,25,25))
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if(math.sqrt(math.pow(x-248,2)+math.pow(y-315,2))<30):
                Diff = 9000
                #print(Diff)
            elif(math.sqrt(math.pow(x-375,2)+math.pow(y-315,2))<30):
                Diff = 8500
                #print(Diff)    
            elif(math.sqrt(math.pow(x-515,2)+math.pow(y-315,2))<30):
                Diff = 8100
            elif(math.sqrt(math.pow(x-375,2)+math.pow(y-250,2))<30):
                GameStarted = True
                time.sleep(0.5)  

    