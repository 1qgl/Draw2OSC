import pygame
import os
import colorsys
import pandas as pd
import numpy as np
from time import perf_counter, sleep
from pythonosc.udp_client import SimpleUDPClient

screenSize = (1400, 800)

screen = pygame.display.set_mode((1400, 800))
draw_surf1 = pygame.surface.Surface((1400, 800))
draw_surf2 = pygame.surface.Surface((1400, 800))
draw_surf3 = pygame.surface.Surface((1400, 800))
draw_surf4 = pygame.surface.Surface((1400, 800))
draw_surf5 = pygame.surface.Surface((1400, 800))

voice = 1

pygame.display.set_caption('Draw2OSC')

draw_on = False
erase_on = False
last_pos = (0, 0)

radius = 1

dir_path = os.path.dirname(os.path.realpath(__file__))

ip = "127.0.0.1"
port = 7001

client = SimpleUDPClient(ip, port)
playlength = 5.0

def roundline(canvas, color, start, end, radius=1):
    Xaxis = end[0] - start[0]
    Yaxis = end[1] - start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0] + float(i) / dist * Xaxis)
        y = int(start[1] + float(i) / dist * Yaxis)
        pygame.draw.circle(canvas, color, (x, y), radius)

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def play():

    print("playing to OSC")
    giventime = False
    while (giventime == False):
        try:
            playlength = float(input("Enter number of seconds to play for: "))
            giventime = True
            print("running for " + str(playlength) + " seconds")
        except:
            pass
    play_array1 = np.copy(pygame.surfarray.pixels3d(draw_surf1))
    play_array1 = (play_array1[30:-30,30:-30,:]!=0).argmax(axis=1)[:,0]
    play_array1 = pd.array(play_array1, dtype="Int64")
    play_array1[play_array1 == 0] = pd.NA
    play_array1 = ((((740 - play_array1)/720)*3)-(1/24))+1.0

    play_array2 = np.copy(pygame.surfarray.pixels3d(draw_surf2))
    play_array2 = (play_array2[30:-30, 30:-30, :] != 0).argmax(axis=1)[:, 0]
    play_array2 = pd.array(play_array2, dtype="Int64")
    play_array2[play_array2 == 0] = pd.NA
    play_array2 = ((((740 - play_array2) / 720) * 3) - (1 / 24)) + 1.0

    play_array3 = np.copy(pygame.surfarray.pixels3d(draw_surf3))
    play_array3 = (play_array3[30:-30, 30:-30, :] != 0).argmax(axis=1)[:, 0]
    play_array3 = pd.array(play_array3, dtype="Int64")
    play_array3[play_array3 == 0] = pd.NA
    play_array3 = ((((740 - play_array3) / 720) * 3) - (1 / 24)) + 1.0

    play_array4 = np.copy(pygame.surfarray.pixels3d(draw_surf4))
    play_array4 = (play_array4[30:-30, 30:-30, :] != 0).argmax(axis=1)[:, 0]
    play_array4 = pd.array(play_array4, dtype="Int64")
    play_array4[play_array4 == 0] = pd.NA
    play_array4 = ((((740 - play_array4) / 720) * 3) - (1 / 24)) + 1.0

    play_array5 = np.copy(pygame.surfarray.pixels3d(draw_surf5))
    play_array5 = (play_array5[30:-30, 30:-30, :] != 0).argmax(axis=1)[:, 0]
    play_array5 = pd.array(play_array5, dtype="Int64")
    play_array5[play_array5 == 0] = pd.NA
    play_array5 = ((((740 - play_array5) / 720) * 3) - (1 / 24)) + 1.0

    starttime = perf_counter()
    delt = 0
    firstscreen = pygame.surface.Surface((1400, 800))
    firstscreen.blit(source=screen, dest=(0, 0))
    while delt < playlength:
        delt = perf_counter() - starttime

        if pd.isna(play_array1[min(int((delt/playlength)*1339),1339)]):
            client.send_message("/ch/2", False)
        else:
            client.send_message("/ch/1", play_array1[min(int((delt/playlength)*1339),1339)])
            client.send_message("/ch/2", True)

        if pd.isna(play_array2[min(int((delt/playlength)*1339),1339)]):
            client.send_message("/ch/4", False)
        else:
            client.send_message("/ch/3", play_array2[min(int((delt/playlength)*1339),1339)])
            client.send_message("/ch/4", True)

        if pd.isna(play_array3[min(int((delt/playlength)*1339),1339)]):
            client.send_message("/ch/6", False)
        else:
            client.send_message("/ch/5", play_array3[min(int((delt/playlength)*1339),1339)])
            client.send_message("/ch/6", True)

        if pd.isna(play_array4[min(int((delt/playlength)*1339),1339)]):
            client.send_message("/ch/8", False)
        else:
            client.send_message("/ch/7", play_array4[min(int((delt/playlength)*1339),1339)])
            client.send_message("/ch/8", True)

        if pd.isna(play_array5[min(int((delt/playlength)*1339),1339)]):
            client.send_message("/ch/10", False)
        else:
            client.send_message("/ch/9", play_array5[min(int((delt/playlength)*1339),1339)])
            client.send_message("/ch/10", True)

        screen.blit(source = firstscreen,dest = (0,0))
        pygame.draw.line(screen, (255, 255, 255), (29 + min(int((delt/playlength)*1339),1339), 29), (29 + min(int((delt/playlength)*1339),1339), 800 - 30), width=1)
        pygame.display.flip()

        delt = perf_counter() - starttime
        sleep(0.01)
    screen.blit(source=firstscreen, dest=(0, 0))
    pygame.display.flip()
    client.send_message("/ch/2", False)
    client.send_message("/ch/4", False)
    client.send_message("/ch/6", False)
    client.send_message("/ch/8", False)
    client.send_message("/ch/10", False)
    print("done")

for i in range(37):
    notecol = hsv2rgb((i % 12)/12.0,1,1)
    space = pygame.Rect(25, (i*20)+30, 5, 20)
    screen.fill(notecol,space)
    pygame.draw.line(screen, (255, 255, 255), (25, (i*20)+39), (29, (i*20)+39), width=1)

pygame.draw.line(screen,(255,255,255),(29,29),(29,800-30),width=1)
pygame.draw.line(screen, (255, 255, 255), (29, 29), (1400-30, 29), width=1)
pygame.draw.line(screen, (255, 255, 255), (29,800-30), (1400 - 30, 800-30), width=1)
pygame.draw.line(screen, (255, 255, 255), (1400-30, 29), (1400 - 30, 800 - 30), width=1)

try:
    while True:
        e = pygame.event.wait()

        if e.type == pygame.QUIT:
            raise StopIteration

        if e.type == pygame.MOUSEBUTTONDOWN:
            if(e.button == 1):
                if(voice == 1):
                    color = (255, 50, 50)
                    radius = 1
                    pygame.draw.circle(draw_surf1, color, e.pos, radius)
                if (voice == 2):
                    color = (50, 255, 50)
                    radius = 1
                    pygame.draw.circle(draw_surf2, color, e.pos, radius)
                if (voice == 3):
                    color = (50, 50, 255)
                    radius = 1
                    pygame.draw.circle(draw_surf3, color, e.pos, radius)
                if (voice == 4):
                    color = (255, 255, 50)
                    radius = 1
                    pygame.draw.circle(draw_surf4, color, e.pos, radius)
                if (voice == 5):
                    color = (255, 50, 255)
                    radius = 1
                    pygame.draw.circle(draw_surf5, color, e.pos, radius)
                pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = True
                erase_on = False
            elif(e.button == 3):
                color = (0, 0, 0)
                radius = 4
                pygame.draw.circle(draw_surf1, color, e.pos, radius)
                pygame.draw.circle(draw_surf2, color, e.pos, radius)
                pygame.draw.circle(draw_surf3, color, e.pos, radius)
                pygame.draw.circle(draw_surf4, color, e.pos, radius)
                pygame.draw.circle(draw_surf5, color, e.pos, radius)
                pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = False
                erase_on = True


        if e.type == pygame.MOUSEBUTTONUP:
            if (e.button == 1 or e.button == 3):
                draw_on = False
                erase_on = False

        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                if (voice == 1):
                    pygame.draw.circle(draw_surf1, color, e.pos, radius)
                    roundline(draw_surf1, color, e.pos, last_pos, radius)
                if (voice == 2):
                    pygame.draw.circle(draw_surf2, color, e.pos, radius)
                    roundline(draw_surf2, color, e.pos, last_pos, radius)
                if (voice == 3):
                    pygame.draw.circle(draw_surf3, color, e.pos, radius)
                    roundline(draw_surf3, color, e.pos, last_pos, radius)
                if (voice == 4):
                    pygame.draw.circle(draw_surf4, color, e.pos, radius)
                    roundline(draw_surf4, color, e.pos, last_pos, radius)
                if (voice == 5):
                    pygame.draw.circle(draw_surf5, color, e.pos, radius)
                    roundline(draw_surf5, color, e.pos, last_pos, radius)
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)

            elif erase_on:
                pygame.draw.circle(draw_surf1, color, e.pos, radius)
                roundline(draw_surf1, color, e.pos, last_pos, radius)
                pygame.draw.circle(draw_surf2, color, e.pos, radius)
                roundline(draw_surf2, color, e.pos, last_pos, radius)
                pygame.draw.circle(draw_surf3, color, e.pos, radius)
                roundline(draw_surf3, color, e.pos, last_pos, radius)
                pygame.draw.circle(draw_surf4, color, e.pos, radius)
                roundline(draw_surf4, color, e.pos, last_pos, radius)
                pygame.draw.circle(draw_surf5, color, e.pos, radius)
                roundline(draw_surf5, color, e.pos, last_pos, radius)
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)

            last_pos = e.pos
        if e.type == pygame.KEYDOWN:
            if (e.key == pygame.K_1):
                voice = 1
            if (e.key == pygame.K_2):
                voice = 2
            if (e.key == pygame.K_3):
                voice = 3
            if (e.key == pygame.K_4):
                voice = 4
            if (e.key == pygame.K_5):
                voice = 5
            if(e.key == pygame.K_s):
                saved = False
                while(saved == False):
                    try:
                        savefile = input("Enter file name to save as: ")
                        print("saving file")
                        pygame.image.save(draw_surf1, os.path.join(dir_path, savefile + "v1" + ".png"))
                        pygame.image.save(draw_surf2, os.path.join(dir_path, savefile + "v2" + ".png"))
                        pygame.image.save(draw_surf3, os.path.join(dir_path, savefile + "v3" + ".png"))
                        pygame.image.save(draw_surf4, os.path.join(dir_path, savefile + "v4" + ".png"))
                        pygame.image.save(draw_surf5, os.path.join(dir_path, savefile + "v5" + ".png"))
                        pygame.image.save(screen, os.path.join(dir_path, savefile + "scr" + ".png"))
                        saved = True
                        print("saved")
                    except:
                        pass
            if (e.key == pygame.K_l):
                loaded = False
                while (loaded == False):
                    try:
                        loadfile = input("Enter file name to load: ")
                        print("loading file")
                        draw_surf1.blit(source = pygame.image.load(os.path.join(dir_path, loadfile + "v1" + ".png")), dest = (0,0))
                        draw_surf2.blit(source=pygame.image.load(os.path.join(dir_path, loadfile + "v2" + ".png")),
                                        dest=(0, 0))
                        draw_surf3.blit(source=pygame.image.load(os.path.join(dir_path, loadfile + "v3" + ".png")),
                                        dest=(0, 0))
                        draw_surf4.blit(source=pygame.image.load(os.path.join(dir_path, loadfile + "v4" + ".png")),
                                        dest=(0, 0))
                        draw_surf5.blit(source=pygame.image.load(os.path.join(dir_path, loadfile + "v5" + ".png")),
                                        dest=(0, 0))
                        screen.blit(source=pygame.image.load(os.path.join(dir_path, loadfile + "scr" + ".png")),
                                        dest=(0, 0))
                        loaded = True
                        print("loaded")
                    except:
                        pass
            if (e.key == pygame.K_p):
                play()
            if (e.key == pygame.K_n):
                nloaded = False
                while (nloaded == False):
                    try:
                        print("loading blank file")
                        nloadfile = "blank"
                        screen.blit(source = pygame.image.load(os.path.join(dir_path, f"{nloadfile}.png")), dest = (0,0))
                        draw_surf1 = pygame.surface.Surface((1400, 800))
                        draw_surf2 = pygame.surface.Surface((1400, 800))
                        draw_surf3 = pygame.surface.Surface((1400, 800))
                        draw_surf4 = pygame.surface.Surface((1400, 800))
                        draw_surf5 = pygame.surface.Surface((1400, 800))
                        nloaded = True
                        print("loaded")
                    except:
                        pass
            if (e.key == pygame.K_f):
                print("Listing png files in load folder:")
                for file in os.listdir(dir_path):
                    if file.endswith(".png"):
                        print(os.path.join(dir_path, file))
        for i in range(37):
            notecol = hsv2rgb((i % 12) / 12.0, 1, 1)
            pygame.draw.line(screen, (notecol[0]*0.3,notecol[1]*0.3,notecol[2]*0.3), (25, (i * 20) + 39), (1400-30, (i * 20) + 39), width=1)
        pygame.display.flip()
except StopIteration:
    pass

pygame.quit()