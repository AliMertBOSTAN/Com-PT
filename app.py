from flask import Flask,render_template,Response
import cv2
from cv2 import cv2
import mediapipe as mp
import time
import math
import numpy as np 
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc

app=Flask(__name__)
cap=cv2.VideoCapture("C:\\Users\\Ali Mert BOSTAN\\Desktop\\Hareketler\\Squat nasıl yapılır.mp4")
global img


class poseDetector():
    def __init__(self, mode= False, upBody=False, smooth=True, detectionCon=0.70, trackCon=0.70):
    
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

            return img
    
    def findPosition(self, img, draw=True):
        try:
            self.lmList = []
            if self.results.pose_landmarks:

                for id, lm in enumerate(self.results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])

                    if draw:
                        cv2.circle(img, (cx, cy), 3, (255,0,0), cv2.FILLED)
        except:
            self.lmList.append([id, 1, 1])

        return self.lmList  

    def findeAngle(self, img, p1, p2, p3, draw=True):
        try:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]

            angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2, x1-x2))
            if angle < 0:
                angle = angle + 360


            if draw:
                cv2.line(img, (x1, y1),(x2,y2),(255,255,255),2)
                cv2.line(img, (x3, y3),(x2,y2),(255,255,255),2)

                cv2.circle(img, (x1,y1), 2,(0, 0, 255), cv2.FILLED)

                cv2.circle(img, (x1,y1), 4,(255, 0, 0), 1)

                cv2.circle(img, (x2,y2), 2,(0, 0, 255), cv2.FILLED)

                cv2.circle(img, (x2,y2), 4,(255, 0, 0), 1)

                cv2.circle(img, (x3,y3), 2,(0, 0, 255), cv2.FILLED)

                cv2.circle(img, (x3,y3), 4,(255, 0, 0), 1)


            #cv2.putText(img, str(int(angle)), (x2-20, y2+50),cv2.FONT_HERSHEY_PLAIN, 0.7, (255,0,255),2)
            return  angle
        except:
            return 1


detector = poseDetector()

   
def bicepscurl (img):

    count = 0
    dir = 0
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if frame_width < 300:
        tickness = 1
        tickenss2 = 0.5
    else :
        if frame_width < 600:
            tickenss = 2
            tickenss2 = 1
            
        else:
            if frame_width < 900:
                tickenss = 3
                tickenss2 = 1.5
            else:
                if frame_width < 1200:
                    tickenss = 4
                    tickenss2 = 2
                else:
                    tickenss = 5
                    tickenss2 = 2.5


    # success, img = cap.read()

    
    #img = cv2.resize(img, (1288, 720))
    #img = cv2.imread("test/test.jpg")
    img = cv2.flip(img, 1)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)


    angleSag = detector.findeAngle(img, 12, 14, 16)
    angleSol = detector.findeAngle(img, 11, 13, 15)
    per = np.interp(angleSol, (200,270),(0,100))

    
    #bilek y değeri kontrolü yap
 

    if per == 100:
            if dir == 0:
                count +=0.5
                dir = 1
    if per == 0:
            if dir == 1:
                count +=0.5
                dir =0

    #cv2.rectangle(img, (0,0), (10000,90), (0,0,0), -1)

    angle1 = detector.findeAngle(img, 13, 11, 23)

    angle2 = detector.findeAngle(img, 14, 12, 24)


    if angleSol < 200:

        if angle1 > 30:
            if angle2 > 330:
                cv2.putText(img, "Bring your left arm closer ", (10,40), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                cv2.putText(img, "to your body before starting.", (10,60), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                time.sleep(0.05)                

        if angle1 < 30:
            if angle2 < 330:
                cv2.putText(img, "Bring your right arm closer ", (10,40), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                cv2.putText(img, "to your body before starting.", (10,60), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                time.sleep(0.05)


        if angle1 > 30:
            if angle2 < 330:
                cv2.putText(img, "Bring your arms closer ", (10,40), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                cv2.putText(img, "to your body before starting.", (10,60), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss) 
                time.sleep(0.05)   

    else:
        if count == 0:
            cv2.putText(img, "Waiting for movement start", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (255,0,0), tickenss)
            time.sleep(0.01)
        else:
            cv2.putText(img, "You doing great", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (255,0,0), tickenss)
            time.sleep(0.01)                    
                    
    cv2.putText(img, f'{int(count)}',(frame_width - 60,60), cv2.FONT_HERSHEY_PLAIN, tickenss2 + 4, (255,0,0), tickenss + 4)
                        
              
    try:
  
        return img
    except:
        pass

def squat(img):

    count = 0
    dir = 0

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if frame_width < 300:
        tickness = 1
        tickenss2 = 0.5
    else :
        if frame_width < 600:
            tickenss = 2
            tickenss2 = 1
            
        else:
            if frame_width < 900:
                tickenss = 3
                tickenss2 = 1.5
            else:
                if frame_width < 1200:
                    tickenss = 4
                    tickenss2 = 2
                else:
                    tickenss = 5
                    tickenss2 = 2.5

        
    #img = cv2.resize(img, (1288, 720))
    #img = cv2.imread("test/test.jpg")
    img = cv2.flip(img, 1)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    

    if True:
        angle1 = detector.findeAngle(img, 25, 23, 11)
        angle2 = detector.findeAngle(img, 24, 26, 28)
        per = np.interp(angle2, (0,360),(0,100))
        #print(angle2,per)



        if per == 100:
            if dir == 0:
                count +=0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count +=0.5
                dir =0
        #print(count)

        
        
        cv2.putText(img, f'{int(count)}',(frame_width - 60,60), cv2.FONT_HERSHEY_PLAIN, tickenss2 + 4, (255,0,0), tickenss + 4)
        
        if angle2 < 195:
            if angle1 > 150:

                if True:
                    if angle1 < 300:
                        if count == 0:
                            cv2.putText(img, "You can start now.", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (255,0,0), tickenss)
                            
                        else:
                            cv2.putText(img, "Keep going", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (255,0,0), tickenss)
                            
                    

            if angle1 <150:
                cv2.putText(img, "Posture is wrong.", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                

        else:
            cv2.putText(img, "Posture is wrong.", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
           

    try:
  
        return img
    except:
        pass

def shoulderpress (img):
    count = 0
    dir = 0

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if frame_width < 300:
        tickness = 1
        tickenss2 = 0.5
    else :
        if frame_width < 600:
            tickenss = 2
            tickenss2 = 1
            
        else:
            if frame_width < 900:
                tickenss = 3
                tickenss2 = 1.5
            else:
                if frame_width < 1200:
                    tickenss = 4
                    tickenss2 = 2
                else:
                    tickenss = 5
                    tickenss2 = 2.5


    #img = cv2.resize(img, (1288, 720))
    #img = cv2.imread("test/test.jpg")
    img = cv2.flip(img, 1)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    #print(lmList)

    if True:

        #sol kol
        angleSol = detector.findeAngle(img, 23, 11, 13)

        #sağ kol
        angleSag = detector.findeAngle(img, 24, 12, 14)

        per = np.interp(angleSol, (230,290),(0,100))
        #print(angle,per)

        
        #print(count)

        

        angle1 = detector.findeAngle(img, 11, 13, 15)
        angle2 = detector.findeAngle(img, 12, 14, 16)

        



        cv2.putText(img, f'{int(count)}',(frame_width - 60,60), cv2.FONT_HERSHEY_PLAIN, tickenss2 + 4, (255,0,0), tickenss + 4)

        if per == 100:
            if dir == 0:
                count +=0.5
                dir = 1
        if per == 0:
                if dir == 1:
                    count +=0.5
                    dir =0

       

        if angleSol > 230:
        
                if angle1 > 80:
                    cv2.putText(img, "Your left wrist should be in line with your elbows", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                   
                
                if angle1 < 40:
                    cv2.putText(img, "Your left wrist should be in line with your elbows", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                    

                if angle2 > 310:
                    cv2.putText(img, "Your right wrist should be in line with your elbows", (10,60), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                    
                
                if angle2 < 270:
                    cv2.putText(img, "Your right wrist should be in line with your elbows", (10,60), cv2.FONT_HERSHEY_PLAIN, tickenss2, (0,0,255), tickenss)
                        
                
                if angle1 <80:
                    if angle1 >40:
                        if angle2 < 310:
                            if angle2 > 270:

                                if True:
                                    if count == 0:
                                        cv2.putText(img, "You can start now", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (255,0,0), tickenss)
                                        
                                    else:
                                        cv2.putText(img, "Keep going", (10,20), cv2.FONT_HERSHEY_PLAIN, tickenss2, (255,0,0), tickenss)
                                        
                                

    try:
         
        return img
    except:
        pass
     
def generate_frames(handler):

    while True:
            
        ## read the camera frame
        success,img=cap.read()

        if not success:
            break
        else:
            
            img = handler(img)
            try:
                ret,buffer=cv2.imencode('.jpg',img)
                img=buffer.tobytes()


                    
                yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            except:
                pass


@app.route('/')
def index():
    return render_template('index.html')

#########################################################

@app.route('/squat_video')
def squat_video():
    return Response(generate_frames(squat),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/squat_page')
def squat_page():
    return render_template('squat_page.html')

#########################################################

@app.route('/shoulderpress_video')
def shoulderpress_video():
    return Response(generate_frames(shoulderpress),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/shoulderpress_page')
def shoulderpress_page():

    return render_template('shoulderpress_page.html')

#########################################################

@app.route('/video')
def bicpescurl_video():

    return Response(generate_frames(bicepscurl),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/bicepscurl_page')
def bicepscurl_page():

    return render_template('bicepscurl_page.html')

########################################################





if __name__=="__main__":
    app.run(debug=False)

