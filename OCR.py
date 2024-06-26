
import cv2
import pytesseract
from pytesseract import Output
 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
 
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    text = pytesseract.image_to_string(frame)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    print(text)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



