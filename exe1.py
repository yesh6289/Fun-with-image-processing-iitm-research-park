import cv2
import numpy as np

# Step 1: Read the two images
image1 = cv2.imread('tom.jpg')
image2 = cv2.imread('rdj.jpg')

# Check if images are read properly
if image1 is None or image2 is None:
    print("Error: Could not read one or both images.")
    exit()

# Step 2: Create a new image by arranging them side-by-side
combined_color = np.hstack((image1, image2))

# Step 3: Convert the new image to grayscale
combined_gray = cv2.cvtColor(combined_color, cv2.COLOR_BGR2GRAY)

# Convert grayscale image back to BGR (so it has 3 channels and can be stacked with color images)
combined_gray_bgr = cv2.cvtColor(combined_gray, cv2.COLOR_GRAY2BGR)

# Step 4: Arrange the colored pair of images on top and the pair of gray images on the bottom
final_image = np.vstack((combined_color, combined_gray_bgr))

# Step 5: Save the final image as "A1_solution.jpg"
cv2.imwrite('A1_solution.jpg', final_image)


print("The image has been saved as 'A1_solution.jpg'")
