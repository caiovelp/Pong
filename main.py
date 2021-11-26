import pygame

from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *

#inicialização
janela = Window(1280, 720)
janela.set_title("PONG")

background = GameImage("fundo.jpg")

ball = Sprite("ball.png", 1)
ball.x = janela.width/2 - ball.width/2
ball.y = janela.height/2 - ball.height/2
vel_ballX = 500
vel_ballY = 500

padD = Sprite("barra.png", 1)
padE = Sprite("barra2.png", 1)
padE.x = 5
padE.y = janela.height/2 - padD.height/2
padD.x = janela.width - padE.width - 5
padD.y = janela.height/2 - padE.height/2
vel_Pad = 500
vel_Pad_IA = 500

padE_metade = Sprite("barra_metade.png", 1)
padE_metade.x = padE.x/2
padE_metade.y = padE.y/2


teclado = Window.get_keyboard()

pontoE = 0
pontoD = 0

timer = 0
frames = 0

ballBounce = 0

fps = "FPS: " + str(0)


#Game Loop
while True:
    #Entrada de dados
    if (teclado.key_pressed("w") and (padE.y >= 0)): #Movimento do pad da esquerda
        padE.y = padE.y - vel_Pad * janela.delta_time()
    if (teclado.key_pressed("s") and (padE.y + padE.height <= janela.height)):
        padE.y = padE.y + vel_Pad * janela.delta_time()
    if (teclado.key_pressed("w") and (padE_metade.y >= 0)): #Movimento do pad da esquerda metade
        padE_metade.y = padE_metade.y - vel_Pad * janela.delta_time()
    if (teclado.key_pressed("s") and (padE_metade.y + padE_metade.height <= janela.height)):
        padE_metade.y = padE_metade.y + vel_Pad * janela.delta_time()

    if (padD.y > ball.y and (padD.y >= 0)):
        padD.y = padD.y - vel_Pad_IA * janela.delta_time() #Movimento da IA
    if (padD.y < ball.y and (padD.y + padE.height <= janela.height)):
        padD.y = padD.y + vel_Pad_IA * janela.delta_time() #Movimento da IA

    #Update

    ball.x += vel_ballX*janela.delta_time()
    ball.y += vel_ballY*janela.delta_time()
    if (ball.collided(padE)): #Colisão com o pad da Esquerda
        vel_ballX *= -1
        ball.x = padE.x + padE.width #Move a bola para a direita de acordo com o tamanho do pad, evitando a patinação.
        ballBounce += 1
    if (ball.collided(padD)): #Colisão com o pad da Direita
        vel_ballX *= -1
        ball.x = padD.x - ball.width #Move a bola para a esquerda de acordo com o tamanho do pad, evitando a patinação.
        ballBounce += 1
    if (ball.collided(padE_metade)): #Colisão com o pad da Esquerda Metade
        vel_ballX *= -1
        ball.x = padE_metade.x + padE_metade.width #Move a bola para a direita de acordo com o tamanho do pad, evitando a patinação.

    if((ball.x + ball.width) >= janela.width): #Ponto para o pad da esquerda
        ball.set_position(janela.width / 2 - ball.width / 2, janela.height/2 - ball.height/2)
        vel_ballX *= -1
        pontoE+=1
        ballBounce = 0
    if((ball.x + ball.width) <= 0): #Ponto para o pad da direita
        ball.set_position(janela.width / 2 - ball.width / 2, janela.height/2 - ball.height/2)
        vel_ballX *= -1
        pontoD+=1
        ballBounce = 0

    if ((ball.y) <= 0): #Colisão com a parede de cima
        vel_ballY *= -1
        ball.y += ball.height/16 #Move a bola 1/16 avos da sua altura para baixo, evitando a patinação.
    if ((ball.y + ball.height) >= janela.height): #Colisão com a parede de baixo
        vel_ballY *= -1
        ball.y -= ball.height/16 #Move a bola 1/16 avos da sua altura para cima, evitando a patinação.


    #Desenho
    background.draw()
    ball.draw()
    padD.draw()
    janela.draw_text(str(pontoE), 370, 45, size=50, color=(70, 235, 125), font_name="Arial", bold=True, italic=False)
    janela.draw_text(str(pontoD), 910, 45, size=50, color=(235, 125, 70), font_name="Arial", bold=True, italic=False)

    timer += janela.delta_time()
    frames += 1
    if (timer >= 1):
        timer = 0
        fps = "FPS: " + str(frames)
        frames = 0
    janela.draw_text(fps, 20, 20, size=20, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)

    if (ballBounce >= 4):
        padE_metade.draw()
    else:
        padE.draw()



    janela.update()