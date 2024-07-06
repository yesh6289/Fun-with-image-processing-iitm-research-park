import cv2
import numpy as np

def cartoonify_image(image):
    # Step 1: Edge Detection
    # Apply bilateral filter to smooth the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    
    # Use adaptive thresholding to detect and emphasize edges
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)

    # Step 2: Color Quantization
    # Apply bilateral filter multiple times to get a cartoon effect
    color = cv2.bilateralFilter(image, 9, 300, 300)
    
    # Step 3: Combine edges and quantized color
    # Convert back to grayscale and combine with edges
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

def main():
    # Read the image
    image_path = 'tom.jpg'  # Change this to your image file path
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read the image.")
        return

    # Apply the cartoonify effect
    cartoon_image = cartoonify_image(image)

    # Display the original and cartoonified images
    cv2.imshow('Original Image', image)
    cv2.imshow('Cartoonified Image', cartoon_image)

    # Save the cartoonified image
    cv2.imwrite('cartoonified_image.jpg', cartoon_image)
    print("Cartoonified image saved as 'cartoonified_image.jpg'")

    # Wait until a key is pressed and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
