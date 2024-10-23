import pygame, random, sys, os, time
from pygame.locals import *
import time
from math import cos, sin
import logging

RESPAWNTIMER = 60
respawntime = RESPAWNTIMER
gold = pygame.Color("#FFD700")
silver = pygame.Color("#c0c0c0")
bronze = pygame.Color("#cd7f32")

ALLOWEDCHARS: list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                       "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "?", " "] 

# import board
# import busio
# import adafruit_adxl34x


left = 0
right = 0

# i2c = busio.I2C(board.SCL, board.SDA)
# accelerometer = adafruit_adxl34x.ADXL345(i2c)

# accelerometer.enable_freefall_detection(threshold=5, time=5)
# accelerometer.enable_motion_detection(threshold=18)
# accelerometer.enable_tap_detection(tap_count=2, threshold=20, duration=50, latency=1000, window=255)

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 12
ADDNEWBADDIERATE = 15
BADDIESCOREMOD = 0.001
ADDNEWBADDIERATEMOD = 0.001
PLAYERMOVERATE = 5
count = 3

# ADDED CODE
GREENIMAGECOORDS = (44*3, 24)

YELLOWIMAGECOORDS = (360, 24)

REDIMAGECOORDS = (82*3, 24)

BLUEIMAGECOORDS = (18, 24)


CURBWIDTH = 105

LastWallPointer = 0


# def getAccelerometer(acceleration, left, right):
#  #   time.sleep(0.1)
#     acceleration = accelerometer.acceleration
#     result = 0
#     if acceleration[0] > 1:
#         if left:
#             result -= 1
#             result += -1+(acceleration[1]/10)
#         if right:
#             result += 1
#             result += 1-(-acceleration[1]/10)
#     else:
#         result = -acceleration[1]/10
#         if result < 0:
#             left = True
#             right = False
#         elif result > 0:
#             right = True
#             left = False
#     result = result * 2
# #    print(result)
# #    result = -(result)
#     return [result, left, right]

def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return


def playerHasHitBaddie(playerRect: pygame.rect, baddies: list):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def playerHasGotClose(playerRect: pygame.rect, baddies: list):
    for i, b in enumerate(baddies):
        if playerRect.colliderect(b['close_rect']):
            return i
    #arbitry high number the program will detect and therefore know the player has not hit a baddie
    return 1000000000


def drawText(text: str, font: pygame.font, surface: pygame.surface, x: int, y: int):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def Get_Input(last_input: int):
    key = pygame.key.get_pressed()
    current_input = -1
    # output corresponds to a button
    if key[pygame.K_a]:
        current_input = 0
    elif key[pygame.K_s]:
        current_input = 1
    elif key[pygame.K_d]:
        current_input = 2
    elif key[pygame.K_f]:
        current_input = 3
    # makes sure player can't hold, must press twice
    if current_input == last_input:
        return -2

    return current_input


def Generate(current: list):
    result = current
    result.append(random.randrange(0, 4))
    return result


def DrawOptions(blue: str, green:str, red:str, yellow:str, alpha:int = 255):
    StartScreen = True
    StartText = font.render(blue, False, (255, 255, 255))
    HighScoreText = font.render(green, False, (255,255,255))
    QuitText = font.render(red, False, (255,255,255))
    OtherText = font.render(yellow, False, (255,255,255))

    # coordinates for text in relation to the buttons
    TextY= (BlueImage.get_height()/2 - (StartText.get_height()/2))
    TextX = BlueImage.get_width() + 20

    #set Alpha, prolly a better way to do this but idk
    items = [StartText, HighScoreText, QuitText, OtherText, BlueImage, RedImage, YellowImage, GreenImage]
    for i in items:
        i.set_alpha(alpha)


    screen.blit(BlueImage, (75, 200))
    screen.blit(StartText, (75+TextX, 200 + TextY))
    screen.blit(GreenImage, (75, 300))
    screen.blit(HighScoreText, (75+TextX, 300 + TextY))
    screen.blit(RedImage, (75, 400))
    screen.blit(QuitText, (75+TextX, 400 + TextY))
    screen.blit(YellowImage, (75, 500))
    screen.blit(OtherText, (75+TextX, 500 + TextY))

    for i in items:
        i.set_alpha(255)



def WaitForOptionInput() -> int:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                    terminate()
            elif event.type == KEYDOWN:
                if event.key == ord('a'):
                    return 0
                elif event.key == ord('s'):
                    return 1
                elif event.key == ord('d'):
                    return 2
                elif event.key == ord('f'):
                    return 3
            pygame.display.flip()
            mainClock.tick(FPS)


def ScoreAddEffect(progress: int, length:int, value: int) -> pygame.surface:
    result = font.render(f"+{value}", False, (0,255,255))
    result = pygame.transform.rotate(result, 5)
    result.set_alpha(sin((progress/length) * 3) * 255)
    return result

def RenderLeaderboard(scores: list):
    title = EndFont.render("LEADERBOARD", False, (255,255,255))
    title_x = (WINDOWWIDTH/2 - title.get_width()/2)
    title_y = 50
    screen.blit(title, (title_x, title_y))
    for index, item in enumerate(scores):
        name = item["name"]
        score = item["score"]
        
        if index == 0:
            colour = gold
        elif index == 1:
            colour = silver
        elif index ==2:
            colour = bronze
        else:
            colour = TEXTCOLOR
        if name != NULLCHAR:
            lineLeft:str = f"{index+1}: {name}"
            lineCenter:str = str(score)
            lineImageLeft = font.render(lineLeft, False, colour)
            lineImageCenter = font.render(lineCenter, False, colour)
            image_coords_left = (100, 200 + (index* 50))
            image_coords_center = (WINDOWWIDTH/2 - lineImageCenter.get_width()/2, 200 + index*50)
            screen.blit(lineImageLeft, image_coords_left)
            screen.blit(lineImageCenter, image_coords_center)


def RenderTitleScreen():
    screen.blit(Road, (0,0))
    screen.blit(TitleScreen, (0,0))

    DrawOptions("START GAME", "HIGH SCORES (wip)", "QUIT", "How to play")

# BUG doesnt work with any other lenngth than 4, sould fix (excuse to learn generators)
def GetTextInput(length: int, message: str) -> str:
    selecting = True
    cursor_pos = 0
    TILEWIDTH = 144
    TEXTOFFSETY = 50
    TEXTOFFSETX = 55
    TEXTSEPERATOR = 70
    BUTTONY = 450
    BUTTONWIDTH = 48
    selected_chars = [0,0,0,0]
    message_text = MedFont.render(message.upper(), False, (255,255,255))
    message_coords = (CenterCoords(message_text, screen, Xonly=True), 100)
    while selecting:
        screen.fill(BACKGROUNDCOLOR)
        base = pygame.surface.Surface(((length+1) * TILEWIDTH, TILEWIDTH * 3))
        #render input



        for i in range(length):
            #center text
            text = EndFont.render(ALLOWEDCHARS[selected_chars[i]], False, (255,255,255))
            textCoords = ((TILEWIDTH * i) + TEXTOFFSETX, TILEWIDTH + TEXTOFFSETY)
            base.blit(text, textCoords)
            #upper text
            charIndex = (selected_chars[i] -1) if (selected_chars[i] - 1 >= 0) else len(ALLOWEDCHARS) -1
            text = EndFont.render(ALLOWEDCHARS[charIndex], False, (255,255,255)) 
            textCoords = ((TILEWIDTH * i) + TEXTOFFSETX, (TILEWIDTH + TEXTOFFSETY) - TEXTSEPERATOR)
            text.set_alpha(100)
            base.blit(text, textCoords)
            #bottom text
            charIndex = (selected_chars[i] +1) if (selected_chars[i] + 1 < len(ALLOWEDCHARS) -1) else 0
            text = EndFont.render(ALLOWEDCHARS[charIndex], False, (255,255,255)) 
            textCoords = ((TILEWIDTH * i) + TEXTOFFSETX, (TILEWIDTH+ TEXTOFFSETY) + TEXTSEPERATOR)
            text.set_alpha(100)
            base.blit(text, textCoords)
            squareCoords = ((TILEWIDTH * i), TILEWIDTH)
            base.blit(square, squareCoords)
        
        base.blit(tick, ((TILEWIDTH * (length)), TILEWIDTH))

        base.blit(cursor, (cursor_pos * TILEWIDTH, TILEWIDTH))
        screen.blit(message_text, message_coords)

        screen.blit(base, CenterCoords(base, screen))

        screen.blit(BlueArrow, (160-BUTTONWIDTH, BUTTONY))
        screen.blit(GreenArrow, (320-BUTTONWIDTH, BUTTONY))
        screen.blit(RedArrow, (480-BUTTONWIDTH, BUTTONY))
        screen.blit(YellowArrow, (640-BUTTONWIDTH, BUTTONY))
        screen.blit(message_text, message_coords)



        #move cursor
        pygame.display.flip()
        textInput = WaitForOptionInput()
        if textInput == 0:
            cursor_pos = (cursor_pos - 1) if (cursor_pos - 1 >= 0) else length
        elif textInput == 3:
            cursor_pos = (cursor_pos + 1) if (cursor_pos + 1 <= length) else 0
        elif textInput == 1 and cursor_pos != length:
            current_select = selected_chars[cursor_pos]
            selected_chars[cursor_pos] = (current_select - 1) if (current_select - 1 >= 0) else  len(ALLOWEDCHARS) - 1
        elif  textInput == 2 and cursor_pos != length:
            current_select = selected_chars[cursor_pos]
            selected_chars[cursor_pos] = (current_select + 1) if (current_select + 1 < len(ALLOWEDCHARS)) else  0
        elif (textInput == 2 or textInput == 1) and cursor_pos == length:
            result:str = ""
            for letter in selected_chars:
                result += ALLOWEDCHARS[letter]
            return result

    
def CenterCoords(surface: pygame.surface, background: pygame.surface, *, Yonly:bool = False, Xonly:bool = False):
    result = (background.get_width()/2 - surface.get_width()/2, background.get_height()/2 - surface.get_height()/2)
    if Xonly:
        return result[0]
    elif Yonly:
        return result[1]
    return result



class SpriteSheet():
    def __init__(self, image):      
        self.sheet = image  
    
    def get_image(self, frame: int, width: int, height: int, scale: int = 1, colour: pygame.color = (0,0,0)):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

gameRound: int = 1
TodoList: list = []

CurrentInput: int = 0

position: int = 0

PATTERTIMERMAX: int = 15
patterntime: int = PATTERTIMERMAX
PAUSETIMEMAX: int = 5
pausetime: int = PAUSETIMEMAX

NEWROUNDTIMER: int = 20
newroundtime: int = 0

INPUTTIMER: int = 60
inputtimer: int = INPUTTIMER


# generates a list of 0-3, representing an index for one of the buttons in the  various Button lists
TodoList: list = Generate(TodoList)

last_input: int = -1

# if the number in the lis is greater than 0 the corresponding button will glow
GlowList: list = [0, 0, 0, 0]

SimonScore: int = 0







# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
screen: pygame.display = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts, both fonts and HUDfont
font = pygame.font.Font("misc/New_Font.TTF", size=20)
EndFont = pygame.font.Font("misc/New_Font.TTF", size=45)
MedFont = pygame.font.Font("misc/New_Font.TTF", size=30)



# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/car.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')
LevelUpSFX = pygame.mixer.Sound("SFX/LevelUp.mp3")
BlueSFX = pygame.mixer.Sound("SFX/Blue.wav")
RedSFX = pygame.mixer.Sound("SFX/Red.wav")
GreenSFX = pygame.mixer.Sound("SFX/Green.wav.wav")
YellowSFX = pygame.mixer.Sound("SFX/Yellow.wav")

# images
playerImage = pygame.image.load('image/car1.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car3, car4, baddieImage]
Road = pygame.image.load("Images/Road.png")
FadeOut = pygame.image.load("Images/FadeOut.png")

# SIMON IMAGES

#normal buttons
BlueImage = pygame.image.load("Images/ButtonBlue1.png")
GreenImage = pygame.image.load("Images/ButtonGreen1.png")
RedImage = pygame.image.load("Images/ButtonRed1.png")
YellowImage = pygame.image.load("Images/ButtonYellow1.png")


#active buttons
BlueImageActive = pygame.image.load("Images/ButtonBlue2.png")
RedImageActive = pygame.image.load("Images/ButtonRed2.png")
GreenImageActive = pygame.image.load("Images/ButtonGreen2.png")
YellowImageActive = pygame.image.load("Images/ButtonYellow2.png")


BlueImageDead = pygame.image.load("Images/ButtonBlue3.png")
RedImageDead = pygame.image.load("Images/ButtonRed3.png")
GreenImageDead = pygame.image.load("Images/ButtonGreen3.png")
YellowImageDead = pygame.image.load("Images/ButtonYellow3.png")


Panel = pygame.image.load("Images/SimonPanel.png")
PanelDead = pygame.image.load("Images/SimonPanelBroken.png")

TitleScreen = pygame.image.load("Images/TitleScreent.png")
ExplosionSheet = pygame.image.load("Images/Fireball.png")

explosion = SpriteSheet(ExplosionSheet)

HelpScreen = pygame.image.load("Images/HelpScreen.png")

VingetteEffect = pygame.image.load("Images/Vingette.png")

square = pygame.image.load("Images/TextSelect.png")
tick = pygame.image.load("Images/Tick.png")
cursor = pygame.image.load("Images\Cursor.png")

BlueArrow = pygame.image.load("Images/BlueArrow.png")
RedArrow = pygame.image.load("Images/RedArrow.png")
YellowArrow = pygame.image.load("Images/YellowArrow.png")
GreenArrow = pygame.image.load("Images/GreenArrow.png")

# all lists are in the same order and therefore the same index will apply to the same button in each list
ButtonImages = [BlueImage, GreenImage, RedImage, YellowImage]
ActiveButtons = [BlueImageActive, GreenImageActive, RedImageActive, YellowImageActive]
ButtonCoords = [BLUEIMAGECOORDS, GREENIMAGECOORDS, REDIMAGECOORDS, YELLOWIMAGECOORDS]
ButtonSFX = [BlueSFX, RedSFX, GreenSFX, YellowSFX]





PANELCOORDS = (((WINDOWWIDTH/2)-(Panel.get_width()/2)), WINDOWHEIGHT-Panel.get_height())


# "Start" screen

RenderTitleScreen()

#how much the score changes by once a simon in cleared
scoreMod: int = 0


topScores:list = []

#seperate list that form the list topScores when combined
topNames:list = []
scores:list = []

SWITCHCHAR = "*"
NULLCHAR = "/"

zero = 0
if not os.path.exists("data/save.dat"):
    f = open("data/save.dat", 'w')
    f.write(str(zero) + SWITCHCHAR)
    f.write(NULLCHAR)
    f.close()
v = open("data/save.dat", 'r')

FileList = v.read().split("*")

for index, item in enumerate(FileList):
    if index % 2 == 0:
        scores.append(int(item))
    else:
        topNames.append(item)

for i, _ in enumerate(topNames):
    result: dict = {}
    result["name"] = topNames[i]
    result["score"] = scores[i]
    topScores.append(result)

topScore = topScores[0]["score"]
v.close()



StartScreen = True


TRANSTIME = 30
while StartScreen:
    RenderTitleScreen()

    OptionInput: int = WaitForOptionInput()
    if OptionInput == 0:
        for i in range(TRANSTIME):
            screen.blit(Road, (0,0))
            alpha = int(255 - (i/TRANSTIME * 255))
            TitleScreen.set_alpha(alpha)
            screen.blit(TitleScreen, (0,0))
            DrawOptions("START GAME", "HIGH SCORES (wip)", "QUIT", "How to play", alpha=alpha)
            
            Panel.blit(BlueImage, BLUEIMAGECOORDS)
            Panel.blit(GreenImage, GREENIMAGECOORDS)
            Panel.blit(RedImage, REDIMAGECOORDS)
            Panel.blit(YellowImage, YELLOWIMAGECOORDS)
            panel_position = WINDOWHEIGHT - (i/TRANSTIME) * (WINDOWHEIGHT - PANELCOORDS[1])
            car_position = WINDOWHEIGHT - ((i/TRANSTIME) * (200))
            screen.blit(playerImage, (WINDOWWIDTH/2, car_position))
            screen.blit(Panel, (PANELCOORDS[0], panel_position))
            pygame.display.flip()
            mainClock.tick(FPS)
        StartScreen = False
    elif OptionInput == 1:
        screen.fill(BACKGROUNDCOLOR)
        RenderLeaderboard(topScores)
        pygame.display.flip()
        waitForPlayerToPressKey()


    elif OptionInput == 2:
        terminate()
    elif OptionInput == 3:
        screen.blit(HelpScreen, (0,0))
        pygame.display.flip()
        mainClock.tick(FPS)
        WaitForOptionInput()

# mode is 0 for displaying the pattern and then is set to one when the player has to copy it
mode: int = 0


PlaySFX: bool = True


#the effect is triggered if this is below the length of the effect, therefore set to an arbitrely high number
effectProgress: int = 100000


Playing = True
score = 0

while (True):
    # start of the game
    TodoList = []
    TodoList = Generate(TodoList)
    # inputtimer = INPUTTIMER
    # newroundtime = NEWROUNDTIMER
    # pausetime = PAUSETIMEMAX
    # pausetime = PAUSETIMEMAX
    inputtimer = INPUTTIMER
    newroundtime = 0
    position = 0
    mode = 0
    GlowList = [0,0,0,0]
    baddies = []
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 200)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0

    while Playing:  # the game loop
        score += 1  # increase score

        #getting input
        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

        # spawning walls
        if len(baddies) == 0:
            sideLeft = {'rect': pygame.Rect(0, 0, CURBWIDTH, WINDOWHEIGHT),
                        'close_rect': pygame.Rect(0, 0, CURBWIDTH, WINDOWHEIGHT),
                        'speed': BADDIEMINSPEED + BADDIESCOREMOD * score,
                        'surface': pygame.transform.scale(Road, (800, 600)),
                        }
            baddies.append(sideLeft)
            LastWallPointer = len(baddies) -1
            sideRight = {'rect': pygame.Rect(WINDOWWIDTH-CURBWIDTH, 0, CURBWIDTH, 600),
                         'close_rect': pygame.Rect(WINDOWWIDTH-CURBWIDTH, 0, CURBWIDTH, 600),
                         'speed': BADDIEMINSPEED + BADDIESCOREMOD * score,
                         'surface': pygame.transform.scale(Road, (0, 0)),
                         }
            baddies.append(sideRight)

        elif (baddies[LastWallPointer]["rect"].top >= 0):
            sideLeft = {'rect': pygame.Rect(0, -600 + (BADDIEMINSPEED + BADDIESCOREMOD * score), CURBWIDTH, WINDOWHEIGHT),
                        "close_rect": pygame.Rect(0, -600 + (BADDIEMINSPEED + BADDIESCOREMOD * score), CURBWIDTH, WINDOWHEIGHT),
                        'speed': BADDIEMINSPEED + BADDIESCOREMOD * score,
                        'surface': pygame.transform.scale(Road, (800, 600)),
                        }
            baddies.append(sideLeft)
            LastWallPointer = len(baddies) - 1
            sideRight = {'rect': pygame.Rect(WINDOWWIDTH - CURBWIDTH, -100, CURBWIDTH, WINDOWHEIGHT),
                         'close_rect': pygame.Rect(WINDOWWIDTH - CURBWIDTH, -100, CURBWIDTH, WINDOWHEIGHT),
                         'speed': BADDIEMINSPEED + BADDIESCOREMOD * score,
                         'surface': pygame.transform.scale(Road, (0, 0)),
                         }
            baddies.append(sideRight)

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter >= max(ADDNEWBADDIERATE - int(score * ADDNEWBADDIERATEMOD), 2):
            baddieAddCounter = 0
            baddieSize = 30
            closeDistance = 10
            baddiePos = (random.randint(CURBWIDTH, WINDOWWIDTH-(CURBWIDTH+baddieSize)), 0-baddieSize)
            newBaddie = {'rect': pygame.Rect(baddiePos, (23, 47)),
                         "close_rect": pygame.Rect((baddiePos[0] - closeDistance, baddiePos[1]), (23 + (closeDistance*2), 47)),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED) + BADDIESCOREMOD * score,
                         'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
                         "collided": False
                         }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # movement = getAccelerometer(accelerometer.acceleration, left, right)
        # playerRect.move_ip(movement[0] * PLAYERMOVERATE, 0)
        # left = movement[1]
        # right = movement[2]

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
                b['close_rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies:
            if b['rect'].top > WINDOWHEIGHT:
                if baddies.index(b) <= LastWallPointer:
                    LastWallPointer -= 1
                baddies.remove(b)

        # Draw the game world on the window.
        screen.fill(BACKGROUNDCOLOR)




        for b in baddies:
            screen.blit(b['surface'], b['rect'])

        screen.blit(playerImage, playerRect)


        # SIMON CODE STARTS HERE!!!!!!!!!!!!!!!!!!!!!!!!
        Panel.blit(BlueImage, BLUEIMAGECOORDS)
        Panel.blit(RedImage, REDIMAGECOORDS)
        Panel.blit(YellowImage, YELLOWIMAGECOORDS)
        Panel.blit(GreenImage, GREENIMAGECOORDS)




        if mode == 0:
            # pattern is shown to players
            if patterntime >= 0:
                action = TodoList[position]
                if PlaySFX:
                    ButtonSFX[action].play()
                    PlaySFX = False
                Panel.blit(ActiveButtons[action], ButtonCoords[action])
                patterntime -= 1
            else:
                if pausetime > 0:
                    pausetime -= 1
                else:
                    PlaySFX = True
                    pausetime = (PAUSETIMEMAX if position != len(TodoList) -2 else 0)
                    position += 1
                    patterntime = PATTERTIMERMAX
                    if position == (len(TodoList)):
                        mode = 1
                        position = 0
        elif mode == 1:
            # Player inputs their answers
            key = Get_Input(last_input)

            if newroundtime == 1:
                TodoList = Generate(TodoList)
                mode = 0
                position = 0
                patterntime = PATTERTIMERMAX
                newroundtime = 0
            elif newroundtime > 0:
                if newroundtime == NEWROUNDTIMER:
                    LevelUpSFX.play()
                newroundtime -= 1
            else:
                if inputtimer <= 0:
                    mode = 2
                inputtimer -= 1

                # key does not update if User is holding down button
                if key != -2:
                    last_input = key

                if key == TodoList[position]:
                    # User has pressed correct key
                    inputtimer = INPUTTIMER
                    ButtonSFX[TodoList[position]].play()

                    GlowList[key] = 30
                    if position == len(TodoList) - 1:
                        # end of round
                        score += 100 * len(TodoList)
                        newroundtime = NEWROUNDTIMER
                        scoreMod = 100 * len(TodoList)
                        effectProgress = 0
                    else:
                        position += 1
                elif key >= 0:
                    mode = 2



        for i in range(len(GlowList)):
            button = GlowList[i]
            if button > 0:
                Panel.blit(ActiveButtons[i], ButtonCoords[i])
                GlowList[i] -= 1
            else:
                pass
                # screen.blit(ButtonImages[i], ButtonCoords[i])

        screen.blit(Panel, PANELCOORDS)
        if inputtimer < 30:
            VingetteEffect.set_alpha(255- int(abs(inputtimer/30) * 255))
        else:
            VingetteEffect.set_alpha(0)
        screen.blit(VingetteEffect, (0,0))

        ScoreText = font.render(f"SCORE: {score}", False, (255, 255, 255))
        HighScoreText = font.render(f"HIGH: {topScore}", False, (255, 255, 255))
        screen.blit(ScoreText, (0, 0))
        screen.blit(HighScoreText, (600, 0))

        if effectProgress < 60:
            ScoreEffct = ScoreAddEffect(effectProgress, 60, scoreMod)
            effectProgress += 1
            screen.blit(ScoreEffct, (0,ScoreText.get_height()))

        pygame.display.flip()



        baddie = playerHasGotClose(playerRect, baddies)
        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies) or mode == 2:
            count = count - 1
            pygame.mixer.music.stop()
            gameOverSound.play()
            respawntime = RESPAWNTIMER

            for i in range(RESPAWNTIMER):
                #respawn timers is 60 btw

                #respawn time
                screen.blit(Road, (0, 0))
                respawntime -= 1



                for b in baddies:
                    screen.blit(b['surface'], b['rect'])

                screen.blit(playerImage, playerRect)

                #get frame of explosion animation
                if i < 10:
                    frame = int((i/10) * 3)
                    fireball = explosion.get_image(frame,64,64)
                    if mode == 2:
                        fire_pos = ((playerRect.centerx - fireball.get_width()/2), (playerRect.centery - fireball.get_width()/2))
                    else:
                        fire_pos = (((playerRect.left + playerRect.width/2) - fireball.get_width()/2), playerRect.top - fireball.get_width()/2)
                    screen.blit(fireball, fire_pos)

                PanelDead.blit(BlueImageDead, BLUEIMAGECOORDS)
                PanelDead.blit(RedImageDead, REDIMAGECOORDS)
                PanelDead.blit(YellowImageDead, YELLOWIMAGECOORDS)
                PanelDead.blit(GreenImageDead, GREENIMAGECOORDS)
                screen.blit(PanelDead, PANELCOORDS)
                screen.blit(VingetteEffect, (0,0))

                FadeOut.set_alpha(int((i/30) * 255))


                if count == 0:
                    ScoreText = font.render(f"SCORE: {score}", False, colour)
                    screen.blit(ScoreText, (0, 0))
                    HighScoreText = font.render(f"HIGH: {topScore}", False, (255, 255, 255))
                    screen.blit(HighScoreText, (600, 0))


                screen.blit(FadeOut, (0,0))


                colour = (255,255,255)
                # pulse score red
                if count >  0:
                    if i == 35:
                        score = score//2
                    if i > 30 and i < 52:
                        value = int(abs(cos((i - 30) * 3) * 255))
                        colour = (255, value, value)
                        SubtractText = font.render(f"-{score/2}", False, (255,0,0))
                        SubtractText.set_alpha(255-value)
                        SubtractText = pygame.transform.rotate(SubtractText, -5)
                        screen.blit(SubtractText, (1, SubtractText.get_height()))


                    ScoreText = font.render(f"SCORE: {score}", False, colour)
                    screen.blit(ScoreText, (0, 0))


                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()

                pygame.display.flip()
                mainClock.tick(FPS)
        
            break
        elif baddie < 10000:
            #TODO code all of the getting too close system
            if not(baddies[baddie]["collided"]):
                print("close call")
                score += 100
                baddies[baddie]["collided"] = True
            pass
                
        mainClock.tick(FPS)



    pygame.display.flip()
    mainClock.tick(FPS)
    if count == 0:

        # Game over Mode

        screen.fill((0,0,0))
        GameOverText = EndFont.render("GAME OVER", False, (255,255,255))
        ScoreText = MedFont.render(f"SCORE: {score}", False, TEXTCOLOR)
        NAMENEEDEDCHAR  = "%"
        scoreData:dict = {}
        scoreData["name"] = NAMENEEDEDCHAR
        scoreData["score"] = score
        topScores.append(scoreData)
        topScores.sort(key=lambda d: d["score"], reverse=True)
        score = 0
        LEADERBOARDLENGTH = 7
        topScores = topScores[:LEADERBOARDLENGTH]

        for item in topScores:
            if item["name"] == NAMENEEDEDCHAR:
                item["name"] = GetTextInput(4, "ENTER NAME FOR LEADERBOARD")
        screen.fill((0,0,0))
        FileString: str = ""


        #formats the list into a string to be saved, looking back could have used pickle oh well 😥
        for item in topScores:
            FileString += str(item["score"])
            FileString += SWITCHCHAR
            FileString += item["name"]
            FileString += SWITCHCHAR
        
        FileString = FileString[:len(FileString)-1]
        f = open("data/save.dat", "w")
        f.write(FileString)
        f.close()
        

        screen.blit(GameOverText, (WINDOWWIDTH/2 - GameOverText.get_width()/2, WINDOWHEIGHT/4 -100 - GameOverText.get_height()/2))
        screen.blit(ScoreText, (WINDOWWIDTH/2 - ScoreText.get_width()/2, WINDOWHEIGHT/4 - ScoreText.get_height()/2))



        pygame.display.flip()
        StartScreen = True
        while StartScreen:
            screen.fill((0,0,0))
            screen.blit(GameOverText, (WINDOWWIDTH/2 - GameOverText.get_width()/2, WINDOWHEIGHT/4 -100 - GameOverText.get_height()/2))
            screen.blit(ScoreText, (WINDOWWIDTH/2 - ScoreText.get_width()/2, WINDOWHEIGHT/4 - ScoreText.get_height()/2))
            DrawOptions("RESTART GAME?", "HIGH SCORES (doesnt work)", "QUIT", "CREDITS (why dont I work Sam)")
            pygame.display.flip()

            OptionInput = WaitForOptionInput()

            if OptionInput == 0:
                StartScreen = False
            elif OptionInput == 1:
                screen.fill(BACKGROUNDCOLOR)
                RenderLeaderboard(topScores)
                pygame.display.flip()
                waitForPlayerToPressKey()    
            elif OptionInput == 2:
                terminate()
            else:
                print("ME 😎😎😎😎😎😎😎😎")
        pygame.display.flip()
        mainClock.tick(FPS)
        count = 3
