import time
import pygame

time.sleep(3)   
pygame.mixer.init()
pygame.mixer.music.load("./../data/sounds/greeting.mp3")
pygame.mixer.music.play()
time.sleep(10)