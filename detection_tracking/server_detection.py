import cv2
import torch
import numpy as np
import struct
import socket

class YoloDetector():
    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path='/home/piai/바탕화면/obstacle_model.pt', force_reload=True)
        self.model.classes = None  #모든 클래스 탐지
        self.model.conf = 0.4  # 신뢰도 설정
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def score_frame(self, frame):
        self.model.to(self.device)
        results = self.model(frame)
        labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cords

    def plot_boxes(self, results, frame, height, width, confidence=0.3):
        labels, cords = results
        detections = []
        # 탐지하고자 하는 클래스 목록
        desired_classes = ['curb', 'kickboard', 'bollard', 'pothole', 'pole', 'bicycle']

        for i in range(len(labels)):
            row = cords[i]

            if row[4] >= confidence:
                x1, y1, x2, y2 = int(row[0]*width), int(row[1]*height), int(row[2]*width), int(row[3]*height)
                # 현재 라벨이 원하는 클래스에 해당하는지 검사
                if self.model.names[int(labels[i])] in desired_classes:
                    detections.append(([x1, y1, x2, y2, labels[i]], row[4]))
        return frame, detections

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def crop_image(frame, bbox):
    x1, y1, x2, y2 = map(int, bbox)
    if x2 <= x1 or y2 <= y1:
        return None
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return None
    return crop

def send_direction_and_speed(conn, direction, speed):
    # # 방향과 속력을 문자열로 전송
    # message = f"{direction},{speed}"
    # conn.sendall(message.encode())
    try:
        # 방향과 속력을 문자열로 전송
        message = f"{direction},{speed}"
        conn.sendall(message.encode())
    except BrokenPipeError:
        # 여기에서 BrokenPipeError를 처리합니다.
        print("연결이 예상치 못하게 닫혔습니다.")

def main():
    # 카메라 소켓
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8181))
    server_socket.listen(1)
    print("Waiting for a connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # 모터 소켓
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    command_socket.bind(("192.168.0.43", 12345))  # 명령을 보낼 클라이언트를 위한 포트
    command_socket.listen()
    print("서버가 연결을 기다리고 있습니다...")
    command_conn, command_addr = command_socket.accept()
    print(f"{command_addr}에서 연결되었습니다.")
    detector = YoloDetector()
    safe_distance = 100000
    
    while True:
        lengthbuf = recvall(client_socket, 4)
        if lengthbuf is None:
            print("Connection closed by client.")
            break
        length, = struct.unpack('<L', lengthbuf)
        frame_data = recvall(client_socket, length)
        if frame_data is None:
            print("Failed to receive complete frame data.")
            continue
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            print("Could not decode frame.")
            continue
        labels, cords = detector.score_frame(frame)
        height, width = frame.shape[:2]
        stop_sign_shown = False

        for index, cord in enumerate(cords):
            label_name = detector.model.names[int(labels[index])]
            x1, y1, x2, y2, conf = [int(val * width) for val in cord[:4]] + [cord[4]]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if label_name == 'kickboard':
                distance = 60000 / (x2 - x1)
            elif label_name == 'bicycle':
                distance = 80000 / (x2 - x1)
            elif label_name == 'bollard':
                distance = 5000 / (x2 - x1)
            elif label_name == 'pole':
                distance = 15000 / (x2 - x1)
            else :
                distance = 40000 / (x2 - x1)
            cv2.putText(frame, f"{label_name} - Distance: {distance:.2f} cm", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if distance < safe_distance:
                send_direction_and_speed(command_conn, "stop", 0)
                print("유모차가 정지합니다.")
                stop_sign_shown = True
                # return 'stop'
            # else:
            #     #send_direction_and_speed(command_conn, "forward", 100)
            #     print("유모차가 직진합니다.")
            if stop_sign_shown:
                # 화면에 'stop!' 표시
                cv2.putText(frame, 'stop!', (int(width / 2), int(height / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if not stop_sign_shown:  # 탐지된 객체가 없거나 모두 안전 거리 이상인 경우
            send_direction_and_speed(command_conn, "forward", 100)
            print("유모차가 직진합니다.")

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC to quit
            break

    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
