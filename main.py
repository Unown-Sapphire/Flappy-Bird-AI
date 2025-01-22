from fastai.vision.all import *
from fastai.learner import *
import torch
import cv2
import numpy as np
import pyautogui
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def label_func(x):
    return x.parent.name

learn = load_learner('C:/Users/varun/Desktop/project/model.pkl')

def preprocess_frame(frame):
    frame = cv2.resize(frame, (224, 224))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=100, threshold2=200)
    edges_resized = cv2.resize(edges, (224, 224))
    transposed = np.expand_dims(edges_resized, axis=0)
    transposed = tensor(transposed)
    return transposed

def predict_action(frame):
    frame = preprocess_frame(frame)
    prediction = learn.predict(frame)
    return prediction

cap = cv2.VideoCapture(0)

def perform_action(action):
    if action == "click":
        pyautogui.click()

while True:
    ret, frame = cap.read()
    action = predict_action(frame)
    print("Predicted action:", action)
    
    # Perform the action in the game
    perform_action(action)
    
    # Display the frame (optional)
    cv2.imshow('Game Frame', frame)
    
    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()