import cv2
import numpy as np

# Initialize global variables for cropping
ref_point = []
cropping = False

# Load the image
image = cv2.imread('balls.jpg')
if image is None:
    print("Error: Could not read the image.")
    exit()

# Function to apply filters
def apply_filters(img, filter_type):
    if filter_type == 0:  # No filter
        return img
    elif filter_type == 1:  # Sepia filter
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        return cv2.transform(img, sepia_filter)
    elif filter_type == 2:  # Gray filter
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter_type == 3:  # Inverted filter
        return cv2.bitwise_not(img)
    elif filter_type == 4:  # Colormap filter
        return cv2.applyColorMap(img, cv2.COLORMAP_JET)
    return img

# Function to apply sketch effect
def sketch_effect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    inv_blur = cv2.bitwise_not(blur)
    sketch = cv2.divide(gray, inv_blur, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

# Function to handle mouse events for cropping
def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            temp_image = image.copy()
            cv2.rectangle(temp_image, ref_point[0], (x, y), (0, 255, 0), 2)
            cv2.imshow("Image Editor", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("Image Editor", image)

# Function to process the image
def process_image(img, zoom, rotate, blur, filter_type, sketch):
    rows, cols = img.shape[:2]

    # Zoom
    zoomed_img = cv2.resize(img, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_LINEAR)

    # Rotate
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotate, 1)
    rotated_img = cv2.warpAffine(zoomed_img, M, (cols, rows))

    # Blur
    if blur > 0:
        blurred_img = cv2.GaussianBlur(rotated_img, (blur, blur), 0)
    else:
        blurred_img = rotated_img

    # Apply filter
    filtered_img = apply_filters(blurred_img, filter_type)

    # Sketch effect
    if sketch:
        final_img = sketch_effect(filtered_img)
    else:
        final_img = filtered_img

    return final_img

# Create a window and bind the function to the window
cv2.namedWindow("Image Editor")
cv2.setMouseCallback("Image Editor", click_and_crop)

# Create trackbars for image processing
cv2.createTrackbar("Zoom", "Image Editor", 1, 4, lambda x: None)
cv2.createTrackbar("Rotate", "Image Editor", 0, 360, lambda x: None)
cv2.createTrackbar("Blur", "Image Editor", 0, 50, lambda x: None)
cv2.createTrackbar("Filter", "Image Editor", 0, 4, lambda x: None)
cv2.createTrackbar("Sketch", "Image Editor", 0, 1, lambda x: None)

# Main loop
while True:
    zoom = cv2.getTrackbarPos("Zoom", "Image Editor")
    rotate = cv2.getTrackbarPos("Rotate", "Image Editor")
    blur = cv2.getTrackbarPos("Blur", "Image Editor")
    filter_type = cv2.getTrackbarPos("Filter", "Image Editor")
    sketch = cv2.getTrackbarPos("Sketch", "Image Editor")

    edited_image = process_image(image.copy(), zoom, rotate, blur, filter_type, sketch)
    cv2.imshow("Image Editor", edited_image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and len(ref_point) == 2:
        crop_img = image[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        cv2.imwrite("cropped_image.jpg", crop_img)
        print("Cropped image saved as 'cropped_image.jpg'")
    elif key == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
