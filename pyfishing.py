import time
import numpy as np
import cv2
from mss.windows import MSS as mss
import mss
import pyautogui

# I know these config constants are not uppercased, they are camelCased for readeability #
# This is based on the original script from Black_Triangle here (https://habr.com/ru/users/Black_Triangle)

## LENGHT SETTINGS ##
numLoops = 50 # number of times you will try to fish with the script
## FISHING SETTINGS ##
throwPosWidth = 414
throwPosHeight = 285
throwDuration = 1 # in seconds
fishClickTime = 0.8 # in seconds, the time between clicks when fishing mini-game
minigamePxMin = 750 # floater left limit in mini-game
minigamePxMax = 852 # floater right limit in mini-game
extrasClickTime = 3.2 # in seconds, the time between clicks when fishing mini-game for harder things
minigamePxExtrasMin = 707
# floater monitoring (in px)
floaterPosTop = 175
floaterPosLeft = 360
floaterAreaWidth = 100
floaterAreaHeight = 100

## SCREEN SETTINGS ## (in px)
screenPosTop = 30
screenPosLeft = 0
screenWidth = 1600
screenHeight = 900

template = cv2.imread("floater.png", cv2.IMREAD_GRAYSCALE) #replace this with your own reference image
w, h = template.shape[::-1]

color_yellow = (0,255,255)

# define the area to monitor when we throw the floater
mon = {'top': floaterPosTop, 'left': floaterPosLeft, 'width': floaterAreaWidth, 'height': floaterAreaHeight}

def process_image(original_image):

    # GREYSCALE the image and then canny
    #processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    
    #canny without greyscaling
    processed_image = cv2.Canny(original_image, threshold1=200, threshold2=300)
    return processed_image

def ss():
    op = 1
    with mss.mss() as sct:

        monitor = {"top": screenPosTop, "left": screenPosLeft, "width": screenWidth, "height": screenHeight}

        while "Screen capturing":
            img = np.array(sct.grab(monitor))

            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)
            op += 1
            #print (op)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
                for _ in img:
                    x = (pt[0])
                    #print (x)
                    if minigamePxMin < x < minigamePxMax:
                        pyautogui.mouseDown(button='left')
                        time.sleep(fishClickTime)
                        pyautogui.mouseUp(button='left')
                        x = 0
                    elif minigamePxExtrasMin < x < minigamePxMin:
                        pyautogui.mouseDown(button='left')
                        time.sleep(extrasClickTime)
                        pyautogui.mouseUp(button='left')
                        x = 0
                    else:
                        continue
                    break
                else:
                    continue
                break
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
            if op > 35:
                return

def screen_record():
    sct = mss.mss()

    while(True):
        img = sct.grab(mon)

        img = np.array(img)
        processed_image = process_image(img)
        cv2.imshow("Monitoring Area", processed_image) #display the monitoring area for testing
        mean = np.mean(processed_image)
        #print('mean = ', mean)

        if  mean <= float(0.2):
            print('FLOAT DISAPPEARED ')
            pyautogui.click(button='left')
            break
        else:
            time.sleep(0.02)
            continue
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        return

for loopNum in range(0,numLoops):
    time.sleep(1)
    pyautogui.moveTo(throwPosWidth,throwPosHeight,duration=1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(throwPosWidth+50,throwPosHeight+56,duration=throwDuration)
    pyautogui.mouseUp(button='left')
    time.sleep(2)
    screen_record()
    time.sleep(0.01)
    ss()
    print("Loop Number: " + str(loopNum))