
# import opencv-python
import cv2
import tkinter as tk
from PIL import ImageTk, Image

application = tk.Tk()
application.rowconfigure(0, weight=1)
application.columnconfigure(0, weight=1)
lMain = tk.Label(application)
lMain.grid()

# Initialise the camera with index 0:
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("http://192.168.0.20:8080/video") 

# Check that we have camera access:
if not cap.isOpened():
    lMain.config(text="Unable to open camera", wraplength=lMain.winfo_screenwidth())
    application.mainloop()
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def refresh():
    global imgtk
    ret, frame = cap.read()
    if not ret:
        # Error capturing frame, try next time:
        lMain.after(0, refresh)
        return
    
    cv2Image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    w = lMain.winfo_screenwidth()
    h = lMain.winfo_screenheight()
    cw = cv2Image.shape[0]
    ch = cv2Image.shape[1]

    cw, ch = ch, cw
    if (w > h) != (cw > ch):
        cw, ch = ch, cw

        cv2Image = cv2.rotate(cv2Image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    w = min(cw * h / ch, w)
    h = min(ch * w / cw, h)
    w, h = int(w), int(h)

    # cv2Image = cv2.Laplacian(cv2Image, cv2.CV_16SC1)
    cv2Image = cv2.Laplacian(cv2Image, cv2.CV_16SC4)

    cv2Image = cv2.resize(cv2Image, (w, h), interpolation=cv2.INTER_LINEAR)
    img = Image.fromarray(cv2Image)
    imgtk = ImageTk.PhotoImage(image=img)
    lMain.configure(image=imgtk)
    lMain.update()
    lMain.after(0, refresh)

refresh()
application.mainloop()






