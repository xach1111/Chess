import pygame
from constants import *
pygame.init()
class TextBox():
    font = pygame.font.SysFont("Montserrat", 40)
    def __init__(self, screen, x, y, width, height, placeHolderText = None):
        self.text = ""
        self.renderedText = TextBox.font.render(self.text, True, WHITE)
        self.placeHolderText = placeHolderText
        self.renderedPlaceHolderText = TextBox.font.render(self.placeHolderText, True, WHITE)
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.placeHolderText = placeHolderText if placeHolderText else ""
        self.rect = pygame.rect.Rect(self.x,self.y,self.width,self.height)
        self.selected = False
        self.hiddenText = ""
    
    def toggleSelected(self):
        self.selected = True if self.rect.collidepoint(pygame.mouse.get_pos()) else False

    def draw(self, show = None):
        pygame.draw.rect(self.screen, WHITE, self.rect, 5, 30)
        if show:
            self.hiddenText = show * len(self.text)
            self.renderedText = TextBox.font.render(self.hiddenText, True, WHITE)
        self.screen.blit(self.renderedText, (self.x + 20, self.y + 20)) if self.text != "" or self.selected else self.screen.blit(self.renderedPlaceHolderText, (self.x + 20, self.y + 20))
    
    def add(self, letter):
        if self.selected:
            self.text += letter
            self.renderedText = self.font.render(self.text, True, WHITE)
    
    def remove(self):
        if self.selected:
            self.text = self.text[:-1]
            self.renderedText = self.font.render(self.text, True, WHITE)

class Button():
    font = pygame.font.SysFont("Montserrat", 40)
    def __init__(self, screen, x ,y, width, height, text, mainColour = WHITE, secondaryColour = LIGHTGREY):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.mColour = mainColour
        self.sColour = secondaryColour
        self.renderedText = Button.font.render(self.text, True, self.mColour)
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.sColour, self.rect, border_radius=20)

        pygame.draw.rect(self.screen, self.mColour, self.rect, 5, 20)
        self.screen.blit(self.renderedText, (self.x + 20, self.y + 20))

    def clicked(self):
        return True if self.rect.collidepoint(pygame.mouse.get_pos()) else False
    
    def setText(self, text):
        self.text = text
        self.renderedText = Button.font.render(self.text, True, self.mColour)

class Label():
    font = pygame.font.SysFont("Montserrat", 30)
    def __init__(self,screen, x, y, text):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.renderedText = Label.font.render(self.text, True, WHITE)
    
    def draw(self):
        self.screen.blit(self.renderedText, (self.x, self.y))
    
    def setText(self, text):
        self.text = text
        self.renderedText = Label.font.render(self.text, True, WHITE)



    
