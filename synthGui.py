import math
from math import sin

import pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Futura', 30)


screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
running = True
graph1 = pygame.Surface((760, 320))
graph2 = pygame.Surface((760, 320))
graph3 = pygame.Surface((760, 320))
graphCom = pygame.Surface((780, 485))
graphUsed = pygame.Surface((780,485))

#init var from i2c
waveType = [3, 1, 3] #0 = sin
amp = [4096, 4096, 2000]
phase = [0, 0, 2000]
waves = ["Sine", "Pulse","Triangle","Ramp"]
graphs = [graph1, graph2, graph3]
graphValues = [[0]*640,[0]*640,[0]*640]
combinedGraphValues = [0]*640
finalGraphValues = [[0]*640]
clrWhite = (255,255,255)
clrBlack = (0,0,0)
clrRed = (255,0,0)
clrGreen = (0,255,0)
#text_surface = my_font.render(waves[waveType[0]], False, (0, 0, 0))


i = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(clrBlack)
    graph1.fill(clrWhite)
    graph2.fill(clrWhite)
    graph3.fill(clrWhite)
    graphCom.fill(clrWhite)
    graphUsed.fill(clrWhite)

    for i in range(3):
        #lines
        pygame.draw.line(graphs[i], clrBlack, (20,20), (20, 300))
        pygame.draw.line(graphs[i], clrBlack, (20, 160), (640, 160))
        #boxes for input
        pygame.draw.line(graphs[i], clrBlack, (666, 320), (666, 0), width = 4)
        pygame.draw.line(graphs[i], clrBlack, (666, 104), (760, 104), width=4)
        pygame.draw.line(graphs[i], clrBlack, (666, 210), (760, 210), width=4)
        #lines for 1 and -1
        pygame.draw.line(graphs[i], clrGreen, (20, 260), (640, 260))
        pygame.draw.line(graphs[i], clrGreen, (20, 60), (640, 60))

        #actual graph
            #round values in + to range of 100px centered on 160 = 0, 620 samples
        ooga = phase[i]
        tempPhase = round(ooga * 640 / 4695.0)
        tempAmp = amp[i] / 4096.0
        if(waveType[i] == 0):
            #print(tempPhase)

            for x in range(620):
                tphase = ((x + tempPhase) % 620) * (math.pi / 310)
                graphValues[i][x] = -round(sin(tphase) * tempAmp * 100)

        if(waveType[i]==1):
            for x in range(620):
                tPhase = ((x + tempPhase) % 620)
                if tPhase > 206 and tPhase < 412:
                    graphValues[i][x] = -100 * tempAmp
                else:
                    graphValues[i][x] = 100 * tempAmp

        if(waveType[i]==2):
            for x in range(620):
                tPhase = ((x + tempPhase) % 620)
                if tPhase < 310:
                    graphValues[i][x] = -(tPhase * 400 / 620 - 100) * tempAmp
                else:
                    graphValues[i][x] = ((tPhase - 620 / 2) * 400 / 610 - 100) * tempAmp

        if(waveType[i]==3):
            for x in range(620):
                tPhase = ((x + tempPhase) % 620)
                graphValues[i][x] = -(tPhase/620 * 200 - 100) * tempAmp

        for x in range(619):
            pygame.draw.line(graphs[i], clrRed,(x+20,graphValues[i][x] + 160),(x+20,graphValues[i][x+1] + 160))

        #Print Added Stuff
        text_surface = my_font.render(waves[waveType[i]], False, clrBlack)
        graphs[i].blit(text_surface, (670,50))

        text_surface = my_font.render("Phase:", False, clrBlack)
        graphs[i].blit(text_surface, (670, 135))
        text_surface = my_font.render(str(round(phase[i] / 4096, 2)) + "*2pi", False, clrBlack)
        graphs[i].blit(text_surface, (670, 165))

        text_surface = my_font.render("Amp:", False, clrBlack)
        graphs[i].blit(text_surface, (670, 235))
        text_surface = my_font.render(str(round(tempAmp,2)), False, clrBlack)
        graphs[i].blit(text_surface, (670, 265))

        text_surface = my_font.render("0", False, clrBlack)
        graphs[i].blit(text_surface, (5, 160))
        text_surface = my_font.render("1", False, clrBlack)
        graphs[i].blit(text_surface, (5, 60))
        text_surface = my_font.render("-1", False, clrBlack)
        graphs[i].blit(text_surface, (2, 260))


    #add to plot to big boy
    # lines
    pygame.draw.line(graphCom, clrBlack, (40, 30), (40, 445))
    pygame.draw.line(graphCom, clrBlack, (40, 237), (660, 237))

    #-1 -2 -3 lines etc
    pygame.draw.line(graphCom, clrGreen, (40, 287), (660, 287))
    pygame.draw.line(graphCom, clrGreen, (40, 337), (660, 337))
    pygame.draw.line(graphCom, clrGreen, (40, 387), (660, 387))

    pygame.draw.line(graphCom, clrGreen, (40, 187), (660, 187))
    pygame.draw.line(graphCom, clrGreen, (40, 137), (660, 137))
    pygame.draw.line(graphCom, clrGreen, (40, 87), (660, 87))

    text_surface = my_font.render("0", False, clrBlack)
    graphCom.blit(text_surface, (25, 237))
    text_surface = my_font.render("1", False, clrBlack)
    graphCom.blit(text_surface, (25, 187))
    text_surface = my_font.render("2", False, clrBlack)
    graphCom.blit(text_surface, (25, 137))
    text_surface = my_font.render("3", False, clrBlack)
    graphCom.blit(text_surface, (25, 87))
    text_surface = my_font.render("-1", False, clrBlack)
    graphCom.blit(text_surface, (22, 287))
    text_surface = my_font.render("-2", False, clrBlack)
    graphCom.blit(text_surface, (22, 337))
    text_surface = my_font.render("-3", False, clrBlack)
    graphCom.blit(text_surface, (22, 387))


    for x in range(620):
        combinedGraphValues[x] = round((graphValues[0][x] + graphValues[1][x] + graphValues[2][x]) / 2)
    for x in range(619):
        pygame.draw.line(graphCom, clrRed, (x + 40, combinedGraphValues[x] + 237), (x + 40, combinedGraphValues[x + 1] + 237))



    #for now just copy over
    graphUsed.blit(graphCom,(0,0))

    text_surface = my_font.render("Temp Waveform", False, clrBlack)
    graphCom.blit(text_surface, (0, 0))
    text_surface = my_font.render("Output Waveform", False, clrBlack)
    graphUsed.blit(text_surface, (0, 0))
    #pygame.draw.circle(screen, (i, 0, 255), (250, 250), 75)
    #graph1.blit(text_surface, (0, 250))
    screen.blit(graph1, (20,40))
    screen.blit(graph2, (20,380))
    screen.blit(graph3, (20,720))
    screen.blit(graphCom,(790,40))
    screen.blit(graphUsed,(790, 560))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()