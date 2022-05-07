import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
counter = 0
state = None
def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radian = np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = radian*180/np.pi

    return angle

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        image = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        results = pose.process(image)
    
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

        try:
            landmarks = results.pose_landmarks.landmark
        
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
        
            angle = calculate_angle(shoulder, elbow, wrist)
        except:
            pass



        cv2.putText(image, str(angle), 
        tuple(np.multiply(elbow, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            )


        if angle > 150:
            state = 'down'
        
        if angle < 30 and state =='down' :
            counter +=1
            state = 'up'
        
        cv2.putText(image, str(counter), 
        (50,50), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 255), 2, cv2.LINE_AA
            )

        cv2.putText(image, str(state), 
        (100,50), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (166, 166, 255), 2, cv2.LINE_AA
            )

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(155,200,231), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(155,200,230), thickness=2, circle_radius=2) 
                                 )               



        cv2.imshow('squat count', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
