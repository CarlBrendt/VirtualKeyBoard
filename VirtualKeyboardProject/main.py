import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from button import Button
from time import sleep
from pynput.keyboard import Controller
from videocap import VideoCapture

def drawALL(img, buttonList):
    
	for button in buttonList:
		x, y = button.pos
		w, h = button.size
		#check button state
		if button.state:
			cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
			change_color(img, button, (255,0,0), (255, 255, 255))
		else:
			cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
			cv2.rectangle(img, button.pos, (x + w, y + h), (0,255,0), cv2.FILLED)
			cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
						(255, 255, 255), 4)
	return img


def change_color(img, button, color1, color2, bigger=False):
    x, y = button.pos
    w, h = button.size
    if bigger:
        cv2.rectangle(img, (x-15, y-5), (x + w+5, y + h+5), color1, cv2.FILLED)
    else:
        cv2.rectangle(img, button.pos, (x + w, y + h), color1, cv2.FILLED)
    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, color2, 4)

cap = VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P', 'Dl'],
    ['A','S','D','F','G','H','J','K','L',':'],
    ['Z','X','C','V','B','N','M',',','.'],
]

final_text = ""
buttonList = []
keyboard = Controller()

for i in range(len(keys)):
    buttonList.extend(
        Button([100 * j + 50, 100 * i + 50], key)
        for j, key in enumerate(keys[i])
    )

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    hands, img = detector.findHands(img, flipType=False)
    # Hand have dict-lmlist-bbox-center-type
    
    if hands:
        
        # hand
        lmlist = hands[0]['lmList'] # list of 21 landmarks points
        bbox = hands[0]['bbox'] # bunding box info
        img = drawALL(img, buttonList)
        
        if lmlist:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if button.state:
                # If button is pressed, set the color to blue
                    change_color(img, button, (255,0,0), (255, 255, 255))

                elif x < lmlist[8][0] < x+w and y < lmlist[8][1] < y+h:
                    l, _, _ = detector.findDistance((lmlist[8][0], lmlist[8][1]), (lmlist[12][0], lmlist[12][1]), img)

                    if button.text == 'Dl' and l<40:
                        change_color(img, button, (0, 220, 0), (255, 255, 255), bigger=True)
                        if len(final_text)!=0:
                            final_text = final_text[:-1]
                            sleep(0.15) 
                        continue

                    # If the hand is over the button, change its color to a darker green
                    if l > 30:
                        change_color(img, button, (0, 100, 0), (255, 255, 255))
                        button.state = False

                    elif l < 30:
                        change_color(img, button, (0, 220, 0), (255, 255, 255), bigger=True)
                        if not button.state:
                            keyboard.press(button.text)
                            keyboard.release(button.text)
                            button.state = True
                            for btn in buttonList:
                                if btn != button:
                                    btn.state = False
                            final_text += button.text
                            
                # If the hand is not over the button, reset its color to original
                else:
                    change_color(img, button, (0, 255, 0), (255, 255, 255))
                    button.state = False                   
        cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, final_text, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)                              
    
    cv2.imshow('Image',img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break