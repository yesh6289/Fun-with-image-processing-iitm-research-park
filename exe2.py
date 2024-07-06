import cv2
import numpy as np

# Function to create a 4x4 checkerboard
def create_checkerboard(size=100):
    checkerboard = np.zeros((size * 4, size * 4, 3), dtype=np.uint8)
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                checkerboard[i*size:(i+1)*size, j*size:(j+1)*size] = 255  # White squares
    return checkerboard

# Create a checkerboard pattern
checkerboard = create_checkerboard()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('checkerboard_video.avi', fourcc, 1.0, (checkerboard.shape[1], checkerboard.shape[0]))

# Create a video of 10 seconds (10 frames)
for i in range(10):
    if i % 2 == 0:
        out.write(checkerboard)
    else:
        inverted_checkerboard = cv2.bitwise_not(checkerboard)
        out.write(inverted_checkerboard)

# Release the VideoWriter object
out.release()

print("The video has been saved as 'checkerboard_video.avi'")
