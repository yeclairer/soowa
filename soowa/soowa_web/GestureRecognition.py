import mediapipe as mp
import cv2
import os
import numpy as np
import json
from django.http import StreamingHttpResponse
from django.shortcuts import render
from keras.models import model_from_json  
from keras.preprocessing import image 
from django.http import JsonResponse


def GestureRecognition(request):
    gesture = {0:'JEJUDO', 1:'BLUE', 2:'NIGHT', 3:'STAR', 4:'BELOW'}

    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    # Gesture recognition model
    file = np.genfromtxt('/Users/yunkyeong/Desktop/project/soowa/soowa_web/SWDB.txt', delimiter=',')
    angle = file[:,:-1].astype(np.float32)
    label = file[:, -1].astype(np.float32)
    knn = cv2.ml.KNearest_create()
    knn.train(angle, cv2.ml.ROW_SAMPLE, label)

    cap = cv2.VideoCapture(0)

    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            # Recolor image back to BGR for rendering
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            Angle = []
            RHAngle, LHAngle, PAngle = np.zeros((15,)), np.zeros((15,)), np.zeros((10,))

            if results.right_hand_landmarks is not None:
                # RH = []

                joint = np.zeros((21, 3))
                for i in range(21):
                    joint[i] = [results.right_hand_landmarks.landmark[i].x, results.right_hand_landmarks.landmark[i].y,
                                results.right_hand_landmarks.landmark[i].z]
                # print(joint)

                # Compute angles between joints
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
                v = v2 - v1  # [20,3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                RHAngle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

                RHAngle = np.degrees(RHAngle)  # Convert radian to degree
                Angle = np.append(Angle, RHAngle)
                #print("RH : ", RHAngle)

            if results.left_hand_landmarks is not None:
                # LH = []

                joint = np.zeros((21, 3))
                for i in range(21):
                    joint[i] = [results.left_hand_landmarks.landmark[i].x, results.left_hand_landmarks.landmark[i].y,
                                results.left_hand_landmarks.landmark[i].z]
                # print(joint)

                # Compute angles between joints
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
                v = v2 - v1  # [20,3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                LHAngle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

                LHAngle = np.degrees(LHAngle)  # Convert radian to degree
                Angle = np.append(Angle, LHAngle)
                #print("LH : ", LHAngle)

            if results.pose_landmarks is not None:
                #PL = []

                joint = np.zeros((33, 3))
                for i in range(33):
                    joint[i] = [results.pose_landmarks.landmark[i].x, results.pose_landmarks.landmark[i].y, results.pose_landmarks.landmark[i].z]
                #print("pose: ", joint)

                # Compute angles between joints
                v1 = joint[[12,14,16,18,20,22, 11,13,15,17,19,21],:] # Parent joint
                v2 = joint[[14,16,18,20,22,12, 13,15,17,19,21,11],:] # Child joint
                v = v2 - v1 # [12,3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                PAngle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,3,4, 6,7,8,9,10],:],
                    v[[1,2,3,4,5, 7,8,9,10,11],:])) # [10,]

                PAngle = np.degrees(PAngle) # Convert radian to degree
                Angle = np.append(Angle, PAngle)
                if len(Angle) == 40:
                    # Inference gesture
                    data = np.array([Angle], dtype=np.float32)
                    ret, results, neighbours, dist = knn.findNearest(data, 3)
                    idx = int(results[0][0])

                    # Draw gesture result
                    if idx in gesture.keys():
                        #emotion_result= emotionDetect_test(cap)
                        #cv2.putText(image, text=gesture[idx].upper(), org=(50,100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

                        detect_result = {
                            'gesture_id': idx,
                            'gesture': gesture[idx].upper(),
                            'r': idx*5,
                            'g': 100,
                            'b': 78,
                            
                        }
                        context= {
                            'result': detect_result
                        }

                        detect_result_JSON= json.dumps(detect_result)
                        return JsonResponse(detect_result)
            if cv2.waitKey(10) and 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()