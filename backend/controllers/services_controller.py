import cv2

def test_url_rtsp(url):
    # url = 'rtsp://
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        return False
    else:
        cap.release()
        return True