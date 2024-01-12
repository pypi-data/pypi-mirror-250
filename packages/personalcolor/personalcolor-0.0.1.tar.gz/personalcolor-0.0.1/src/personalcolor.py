import cv2
import numpy as np
import dlib
import matplotlib.pyplot as plt

def detect_eye_color(img):
    # 顔検出器をロード
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # 画像から顔の領域を検出
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

    # 検出された顔領域から目の色を検出
    for (x, y, w, h) in faces:
        eye_color = img[y:y + h, x:x + w, :]
    return eye_color

def detect_skin_color(img):
    skin_color = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skin_lower = (0, 20, 70)
    skin_upper = (255, 255, 255)
    skin_mask = cv2.inRange(skin_color, skin_lower, skin_upper)
    skin_color = cv2.bitwise_and(img, img, mask=skin_mask)

    return skin_color

def personal_color(img):
    eye_color = detect_eye_color(img)
    skin_color = detect_skin_color(img)
    eye = eye_color.mean()
    skin = skin_color.mean()

    if eye > 120:
      if skin < 120:
        print("イエローベース スプリング")
      else:
        print("イエローベース オータム")
    else:
      if skin < 120:
        print("ブルーベース サマー")
      else:
        print("ブルーベース ウィンター")

def main():
    plt.imshow(img)
    personal_color(img)

if __name__ == "__main__":
  main()
