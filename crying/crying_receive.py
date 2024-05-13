#!/usr/bin/env python
# coding: utf-8

# # 녹음

# In[2]:


import pyaudio
import wave
import numpy as np
import time
from tensorflow.keras.models import load_model
import librosa
import os
import socket
import sys
import struct

# 서버 설정
HOST = '0.0.0.0'
PORT = 6666

# In[8]:


if 'model1' not in globals():
    model1 = load_model('/home/piai/바탕화면/crying/others_cnn_model.h5')
if 'model2' not in globals():
    model2 = load_model('/home/piai/바탕화면/crying/sound_resnet_best_model.h5')

# # 분류

# In[17]:


# 멜 스펙트로그램을 추출 및 전처리하는 함수
# CNN을 위한 것
def extract_features1(audio_path):
    y, sr = librosa.load(audio_path)
    if len(y[len(y)-50000:len(y)]) == 50000:
        y = y[len(y)-50000:len(y)]
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_ = np.array(S, np.float32)
    S_ = np.expand_dims(S_, -1)
    S_ = S_.reshape(1,128,98,1)
    return S_

def baby_crying_or_not(mel_spectrogram, model):
    prediction = model.predict(mel_spectrogram)
    return prediction.argmax()


# In[18]:


# 멜 스펙트로그램을 추출 및 전처리하는 함수
# ResNet50을 위한 것
def extract_features2(audio_path):
    y, sr = librosa.load(audio_path)
    if len(y[len(y)-100000:len(y)]) == 100000:
        y = y[len(y)-100000:len(y)]
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_ = np.array(S, np.float32)
    S_ = np.expand_dims(S_, -1)
    S_ = S_.reshape(1,128,196,1)
    return S_

def predict_audio_class(mel_spectrogram, model):

    # 예측 실행
    prediction = model.predict(mel_spectrogram)
    class_index = prediction.argmax()

    # 클래스 인덱스에 따른 예측 결과 매핑
    classes = ["배가 많이 아파요", "트림 하고싶어요", " 지금 불편해요 ", "배가 많이 고파요", "정말 자고 싶어요"]
    result = classes[class_index]  # 인덱스를 사용하여 예측 클래스 결정

    return prediction, result

# 파일 수신 from client
def receive_file(client_socket, output_filename):
    """ 클라이언트로부터 파일을 수신하는 함수 """
    # 파일 크기 수신
    file_info = client_socket.recv(4)
    if not file_info:
        print("Failed to receive file size")
        return False
    file_size = struct.unpack('<L', file_info)[0]

    # 파일 데이터 수신
    with open(output_filename, 'wb') as f:
        received_size = 0
        while received_size < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
            received_size += len(data)
    
    print(f"File {output_filename} received successfully.")
    return True

not_crying = "저 안 울었어요 "


def crying_main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Server listening for connections...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")

            # 파일 수신
            if receive_file(client_socket, "received_crying.wav"):
                # 파일 처리 로직 (예: 분석 등)
                print("Processing received file...")
                # 예시: 여기에 파일 분석 로직 추가
                file_path = "received_crying.wav"
                # CNN
                mel_spectrogram1 = extract_features1(file_path)
                baby_or_not = baby_crying_or_not(mel_spectrogram1, model1)

                if baby_or_not == 0:
                    # ResNet50
                    mel_spectrogram2 = extract_features2(file_path)
                    prediction, result = predict_audio_class(mel_spectrogram2, model2)
                    print(result)
                    return(result)
                else:
                    print(not_crying)
                    return(not_crying)
                    continue                

            client_socket.close()

if __name__ == "__main__":
    crying_main()
