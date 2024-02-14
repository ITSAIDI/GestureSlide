import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
import numpy as np
from PyQt5.QtCore import QTimer
from cvzone.HandTrackingModule import HandDetector
from cvzone.PoseModule import PoseDetector
import pyautogui
from PyQt5.QtCore import Qt
import autopy

def Is_Blank(Image):
        
    # Count the number of zeros in the image array
    num_zeros = np.count_nonzero(Image == 0)
    Percentage_Zeros= num_zeros/np.prod(Image.shape)
    if Percentage_Zeros > 0.8:
        return True
    return False
 
 
class Present(QWidget):
     
    def __init__(self, camera_index):
        super().__init__()
        layout = QVBoxLayout()
        self.video_capture = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_frame)
        self.timer.start(2)  # Retrieve frames every 5ms
                
    def SDPE(self):
        
        pyautogui.FAILSAFE = False
        pTime = 0
        WScr,HScr = autopy.screen.size()
        gestureTh = 0
        Get_Out  = False

        Smoothning = 3
        plocX,plocY = 0,0
        clocX,clocY = 0,0

        # Initialize the PoseDetector class with the given parameters
        Pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)
        Handetector = HandDetector(detectionCon=0.8,minTrackCon=0.7,maxHands=1)

        while True:
            Frame = self.get_frame()
            Frame = cv2.flip(Frame, 1)
            
            # Resize the frame
            Frame = cv2.resize(Frame, (800, 600))
            
            # The dimension s of the frame :
            _, WCam = Frame.shape[:2]
            
            # Find the human pose in the frame
            Frame = Pose_detector.findPose(Frame,draw=False)
            PoselmList,_ = Pose_detector.findPosition(Frame, draw=False, bboxWithHands=False)
            if 11 < len(PoselmList):
                gestureTh = int(PoselmList[11][1]) 
                
               
            hands,Frame = Handetector.findHands(Frame)
            
            if hands:
                hand = hands[0]
                FingersUp_list = Handetector.fingersUp(hand)
                lmlist = hand['lmList']
                x8,y8 = lmlist[8][0],lmlist[8][1]
                
                FingersUp_list = Handetector.fingersUp(hand)
                
                if lmlist[0][1] < gestureTh:
                    
                    pyautogui.keyUp('ctrl')
                    
                    if hand['type'] == 'Left': ## It's Right hand in reality hhhh
                        # Go UP :
                        if FingersUp_list == [1,0,0,0,0]:
                            pyautogui.press('pgup',interval=1)

                        # Go Down:
                        if FingersUp_list == [0,0,0,0,1]:
                            pyautogui.press('pgdn',interval=1)
                        
                        # Moving the Mouse :
                        if FingersUp_list == [0,1,0,0,0]:

                            x8 = np.interp(x8,(WCam-300,WCam-200),(0,WScr))
                            y8 = np.interp(y8,(80,150),(0,HScr))
                            
                            #Smoothen the values :
                            clocX = plocX + (x8-plocX)/Smoothning
                            clocY = plocY + (y8-plocY)/Smoothning
                            
                            autopy.mouse.move(clocX,clocY)
                            plocX,plocY = clocX,clocY
                                
                            
                        # Clicking:
                        if FingersUp_list == [1,1,0,0,0]:
                            pyautogui.click()
                            pyautogui.sleep(0.5)
                        
                        # Double Click:
                        if FingersUp_list == [1,1,1,0,0]:
                            pyautogui.doubleClick()
                        
                        # Zoom In
                        if FingersUp_list == [0,1,1,0,0]:
                            pyautogui.keyDown('ctrl')
                            pyautogui.scroll(30)
                            
                        # Zoom Out
                        if FingersUp_list == [0,1,1,1,0]:
                            pyautogui.keyDown('ctrl')
                            pyautogui.scroll(-30) 
                            
                    if hand['type'] == 'Right':
                        # Get Out:
                        if FingersUp_list == [1,1,1,1,1]:
                            Get_Out = True
                    
            # Frame Rate :
            #cTime = time.time()
            #fps   = 1/(cTime-pTime)
            #pTime = cTime
            #cv2.putText(Frame,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
            
            #Draw the Threshold          
            #cv2.line(Frame,(0,gestureTh),(int(WScr),gestureTh),(0,255,0),10)
            #cv2.circle(Frame, (500,gestureTh-300), 10, (255,0,0), -1)
            #cv2.circle(Frame, (WCam-80,gestureTh-500), 10, (0,255,0), -1)
            
            #cv2.imshow('Image',Frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q') or Get_Out:
                pyautogui.keyUp('ctrl')
                cv2.destroyAllWindows()
                return Get_Out                  
                         
    def get_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            return frame
        else:
            return None



   
   
  

     








































