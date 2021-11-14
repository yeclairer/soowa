# Initiate holistic model
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from collections import defaultdict
from itertools import chain

def detection(cap):
    # MediaPipe hands model
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    #while cap.isOpened():
        ret, img = cap.read()
        img0 = img.copy()
        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = holistic.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        Angle, distance = [], []
        right, left = 0, 0  # 손 인식 여부 확인
        RHAngle, LHAngle, PAngle = np.zeros((15,)), np.zeros((15,)), np.zeros((10,))
        RHjoint, LHjoint, Pjoint, Fjoint = np.zeros((21, 3)), np.zeros((21, 3)), np.zeros((33, 3)), np.zeros((468,3))

        # Get RIGHT HAND angle info
        if results.right_hand_landmarks is not None:
            right = 1
            for i in range(21):
                RHjoint[i] = [results.right_hand_landmarks.landmark[i].x, results.right_hand_landmarks.landmark[i].y,
                                results.right_hand_landmarks.landmark[i].z]
            # Compute angles between joints
            v1 = RHjoint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
            v2 = RHjoint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
            v = v2 - v1  # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
            # Get angle using arcos of dot product
            RHAngle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

            RHAngle = np.degrees(RHAngle)  # Convert radian to degree
            Angle = np.append(Angle, RHAngle)

        # get LEFT HAND angle info
        if results.left_hand_landmarks is not None:
            left = 1
            for i in range(21):
                LHjoint[i] = [results.left_hand_landmarks.landmark[i].x, results.left_hand_landmarks.landmark[i].y,
                                results.left_hand_landmarks.landmark[i].z]
            if right == 1:
                distance = np.append(distance, LHjoint[0] - RHjoint[0])  # # 오른손목_왼손목 간 거리
            # Compute angles between joints
            v1 = LHjoint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
            v2 = LHjoint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
            v = v2 - v1  # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
            # Get angle using arcos of dot product
            LHAngle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]
            LHAngle = np.degrees(LHAngle)  # Convert radian to degree
            Angle = np.append(Angle, LHAngle)
        # Get distance info between face&hand
        if results.face_landmarks is not None:
            facdidx = [368, 159]
            handidx = [0, 4, 8, 12, 16, 20]
            for i in facdidx:
                Fjoint[i] = Fjoint[i] = [results.face_landmarks.landmark[i].x, results.face_landmarks.landmark[i].y, results.face_landmarks.landmark[i].z]
            if right == 1:  # 오른쪽손 인식
                for i in handidx:
                    distance = np.append(distance, Fjoint[368] - RHjoint[i])  # 왼쪽눈-오른쪽손
                    distance = np.append(distance, Fjoint[159] - RHjoint[i])  # 오른쪽눈-오른쪽손
                # print("right", len(distance))   # len(distance) = 36    (right or left)
            if left == 1:  # 왼쪽손 인식
                for i in handidx:
                    distance = np.append(distance, Fjoint[368] - LHjoint[i])  # 왼쪽눈-왼쪽손
                    distance = np.append(distance, Fjoint[159] - LHjoint[i])  # 오른쪽눈-왼쪽손
                # print("+ left", len(distance))  # len(distance) = 72    (right + left)
        # Get Arm&Face angle info AND distance info between finger&face
        if results.pose_landmarks is not None:
            for i in range(33):
                Pjoint[i] = [results.pose_landmarks.landmark[i].x, results.pose_landmarks.landmark[i].y, results.pose_landmarks.landmark[i].z] 
            ## angle info ##
            # Compute angles between joints
            v1 = Pjoint[[11,13,15,17,19,21, 12,14,16,18,20,22, 15,7,15,8, 17,7,17,8, 19,7,19,8, 21,7,21,8, 16,7,16,8, 18,7,18,8, 20,7,20,8, 22,7,22,8],:] # Parent joint
            v2 = Pjoint[[13,15,17,19,21,11, 14,16,18,20,22,12, 7,9,8,10, 7,9,8,10, 7,9,8,10, 7,9,8,10, 7,9,8,10, 7,9,8,10, 7,9,8,10, 7,9,8,10],:] # Child joint
            v = v2 - v1 # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
            # Get angle using arcos of dot product
            PAngle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,3,4, 6,7,8,9,10,  12,14,16,18,20,22,24,26, 28,30,32,34,36,38,40,42],:],
                v[[1,2,3,4,5, 7,8,9,10,11, 13,15,17,19,21,23,25,27, 29,31,33,35,37,39,41,43],:])) # [26,]
            PAngle = np.degrees(PAngle) # Convert radian to degree
            Angle = np.append(Angle, PAngle)
            ## distance info ##
            dis1 = Pjoint[[17,21,17,21, 18,22,18,22],:]
            dis2 = Pjoint[[9,9,0,0,     10,10,0,0],:]
            dis = dis1-dis2
            for i in range(4):
                distance = np.append(distance, dis1[2*i]-dis[2*i+1])    #[12,]
            Angle = np.append(Angle, distance)
            print(RHAngle[4])
            # Draw Landmark
            # Right Hand
            mp_drawing.draw_landmarks(img, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            # Left Hand
            mp_drawing.draw_landmarks(img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            # Pose
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
           

    return Angle