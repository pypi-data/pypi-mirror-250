import cv2
import mediapipe as mp
import numpy as np
import pyfirmata
from time import sleep
from playsound import playsound
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def main():
    pose= mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    while True:
        success, image = cap.read()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # 画像からポーズを検出する
        image_tree = cv2.imread('Tree_Pose.jpeg')
        image_tree = cv2.cvtColor(cv2.flip(image_tree, 1), cv2.COLOR_BGR2RGB)
        image_tree.flags.writeable = False
        results_tree = pose.process(image_tree)

        if results_tree.pose_landmarks and results.pose_landmarks:
        # ポーズのランドマークのx,y,z座標を取得する
            x_tree = [landmark.x for landmark in results_tree.pose_landmarks.landmark]
            y_tree = [landmark.y for landmark in results_tree.pose_landmarks.landmark]
            z_tree = [landmark.z for landmark in results_tree.pose_landmarks.landmark]

            x = [landmark.x for landmark in results.pose_landmarks.landmark]
            y = [landmark.y for landmark in results.pose_landmarks.landmark]
            z = [landmark.z for landmark in results.pose_landmarks.landmark]

            # ポーズのランドマークのベクトルを作成する
            v_tree = np.array([x_tree, y_tree, z_tree]).flatten()
            v = np.array([x, y, z]).flatten()

            # ポーズのランドマークのベクトル間のユークリッド距離を計算する
            euclidean_distance = np.linalg.norm(v_tree - v)

            # ポーズの類似度を表示する
            print("ユークリッド距離:", euclidean_distance)
            # ユークリッド距離に応じて音を再生する
            if euclidean_distance < 1:
                # 正しいポーズをしたときに鳴らす音
                playsound('correct.mp3')


        else:
        # 画像または映像からポーズが検出できなかった場合の処理
            print("ポーズが検出できませんでした")

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()

if __name__ == "__main__":
  main()