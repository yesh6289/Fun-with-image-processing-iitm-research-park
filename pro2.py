import cv2
import numpy as np
from scipy.signal import find_peaks

def extract_roi(frame):
    # Convert to grayscale and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Thresholding to isolate the fingertip
    _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Get the largest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        roi = frame[y:y+h, x:x+w]
        return roi
    return None

def calculate_heart_rate(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    roi_means = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        roi = extract_roi(frame)
        if roi is not None:
            # Compute the mean intensity of the ROI
            roi_mean = np.mean(roi)
            roi_means.append(roi_mean)
        
        frame_count += 1
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(roi_means) < 2:
        print("Error: Insufficient data for heart rate calculation.")
        return None

    # Calculate the heart rate using the signal peaks
    roi_means = np.array(roi_means)
    peaks, _ = find_peaks(roi_means, distance=15)
    peak_count = len(peaks)

    duration = frame_count / cap.get(cv2.CAP_PROP_FPS)
    bpm = (peak_count / duration) * 60

    return bpm

def main():
    video_path = '.mp4'  # Replace with the path to your video file
    heart_rate = calculate_heart_rate(video_path)
    
    if heart_rate is not None:
        print(f"Heart Rate: {heart_rate:.2f} BPM")

if __name__ == "__main__":
    main()
