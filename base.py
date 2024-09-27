import cv2
import pytesseract 
from gtts import gTTS
import pyttsx3
import threading
from queue import Queue

# TODO : 
#   keep bounding box displayed until audio is finished
#   anchor bounding box to background image

pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\ansel\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
selected = Queue()
engine = pyttsx3.init()
engine.setProperty("rate", 150)
tl = [None]*2
br = [None]*2
# mouse callback function

def get_pos(event, x, y, flags, params):
    global mouseX, mouseY
    global tl, br
    frame
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x,y)
        if tl[0] == None:
            tl[0], tl[1] = x,y
            br[0], br[1] = x,y
        elif br[0] == tl[0]:
            br[0], br[1] = x,y
        elif tl[0] != None and br[0] != None:
            tl = [None]*2
            br = [None]*2
        if tl[0] != None and br[0] != None:
            cv2.rectangle(frame, (tl[0], tl[1]), (br[0], br[1]), (0,255,0), 2)
    return tl, br

def play_audio():
    global selected
    while True:
        if not selected.empty():
            to_play = selected.get()
            print("hello from sound thread")
            engine.say(to_play) 
            engine.runAndWait()
            selected.task_done()

threading.Thread(target=play_audio, daemon=True).start()

cap = cv2.VideoCapture(0) 
if not cap.isOpened():
    raise Exception("Could not open video device")
try:
    while True:

        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        if tl[0] != None and br[0] != tl[0]:
            to_process = frame[tl[1]:br[1], tl[0]:br[0]]
            cc_to_process = cv2.cvtColor(to_process, cv2.COLOR_BGR2RGB)
            result = pytesseract.image_to_string(cc_to_process)
            print(result)
            # play_sound(result)
            print("too much put?")
            selected.put(result)
            tl = [None]*2
            br = [None]*2
        frame = cv2.rectangle(frame, (tl[0], tl[1]), (br[0], br[1]), (0,255,0), 2)
        cv2.imshow('Webcam Feed', frame)
        cv2.setMouseCallback('Webcam Feed', get_pos)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()