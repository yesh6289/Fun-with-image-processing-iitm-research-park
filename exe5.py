import cv2
import numpy as np

# Function to replace the green screen background
def replace_background(frame, background, lower_green, upper_green):
    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask to detect green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert the mask to get the foreground
    mask_inv = cv2.bitwise_not(mask)
    
    # Extract the foreground from the frame
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    
    # Extract the background from the replacement image
    bg = cv2.bitwise_and(background, background, mask=mask)
    
    # Combine the foreground and background
    combined = cv2.add(fg, bg)
    
    return combined

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the video file path

# Load the background image
background = cv2.imread('ball.jpg')

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Get the frame dimensions
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    cap.release()
    exit()

# Resize the background to match the frame size
background = cv2.resize(background, (frame.shape[1], frame.shape[0]))

# Define the lower and upper bounds for the green color in HSV
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

# Main loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Replace the green screen background
    result = replace_background(frame, background, lower_green, upper_green)
    
    # Display the resulting frame
    cv2.imshow('Green Screen Replacement', result)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
