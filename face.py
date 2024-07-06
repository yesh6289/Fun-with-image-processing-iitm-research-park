# import required libraries here
import cv2
import mediapipe as mp
# video capture object where 0 is the camera number for a usb camera (orwebcam)
# cam = cv2.VideoCapture(0)
# for video file, use this:
cam = cv2.VideoCapture("mrBean2.mp4")
# Frame width and height, will be useful later to find exact pixel locations from normalized locations of faces
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
# Creating a face detector object from Mediapipe solutions
faces = mp.solutions.face_detection.FaceDetection()
while True:
    _ , frame = cam.read() # reading one frame from the camera object
    if _: # if frame received proceed
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) # Convert to RGB for processing
        faceResults = faces.process(frameRGB) # this returns list of location for all the faces in the current frame
        if faceResults.detections != None: # if detection is non empty or if atleast one face detected > proceed elsse skip
            for face in faceResults.detections: # iterate througheach face locations
                bBox = face.location_data.relative_bounding_box #Collect bounding boxes for each face
                # splitting into variables and converting to integer for drawing rectangle around detected faces
                x,y,w,h = int(bBox.xmin*width),int(bBox.ymin*height),int(bBox.width*width),int(bBox.height*height)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imshow('Webcam', frame)
                # Waits for 1ms and check for the pressed key
                if cv2.waitKey(1) & 0xff == ord('q'): # press q to quit the camera
                    break
cam.release() # close the camera
cv2.destroyAllWindows() # Close all the active windows