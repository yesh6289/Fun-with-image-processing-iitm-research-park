import cv2

# Initialize global variables
ref_point = []
cropping = False

# Function to handle mouse events
def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping, image

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            temp_image = image.copy()
            cv2.rectangle(temp_image, ref_point[0], (x, y), (0, 255, 0), 2)
            cv2.imshow("image", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

        # Crop the image and save it
        crop_img = orig[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        cv2.imwrite("cropped_image.jpg", crop_img)
        print("Cropped image saved as 'cropped_image.jpg'")

# Load the image
image = cv2.imread('tom.jpg')
if image is None:
    print("Error: Could not read the image.")
    exit()
orig = image.copy()

# Create a window and bind the function to the window
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# Display the image and wait for a key press
while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
