import cv2
import pytesseract 


pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\ansel\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

tl = [None]*2
br = [None]*2



# mouse callback function
def get_pos(event, x, y, flags, params):
    global mouseX, mouseY
    global tl, br
    global frame
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
            print("we're here")
    return tl, br



# cv2.namedWindow('image')
# cv2.setMouseCallback('image', get_pos)
cap = cv2.VideoCapture(0)  # 0 is the index of the default webcam


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise Exception("Could not open video device")

# Set properties. Each property is specified by a number code and a value
frame = None
# Capture video frames in a loop
try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # get input, mouse for now, eventually eye tracking

        # create bounding box around relevant words
         
        if tl[0] != None and br[0] != tl[0]:
        #Crop image with bounding box
            to_process = frame[tl[1]:br[1], tl[0]:br[0]]
        #convert to RGB
            cc_to_process = cv2.cvtColor(to_process, cv2.COLOR_BGR2RGB)

        # call pytesseract for OCR - this is a google wrapper, in future replace for improvement 
            result = pytesseract.image_to_string(cc_to_process)
            print(result)
        # call google api for text to speech

        # add visual indicator of words being read
 
        # add input to break reading 

        # Display the resulting frame

        frame = cv2.rectangle(frame, (tl[0], tl[1]), (br[0], br[1]), (0,255,0), 2)
        cv2.imshow('Webcam Feed', frame)
        
        cv2.setMouseCallback('Webcam Feed', get_pos)
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
finally:
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()