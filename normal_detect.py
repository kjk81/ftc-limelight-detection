import cv2
import numpy as np

def runPipeline(image, llrobot):
    # Initialize variables
    largestContour = np.array([[]])
    llpython = [0, -1, 0, 0]

    largestColor = ""
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Filter out large areas (e.g., entire frame) with contour area thresholds
    max_area = 97000
    big_area = 70000
    min_area = 30000  # Ignore very small contours

    # Define range of red color in HSV
    lower_red1 = np.array([0, 120, 70])  # Adjusted lower range
    upper_red1 = np.array([10, 255, 255])  # Adjusted upper range
    lower_red2 = np.array([170, 120, 70])  # Second red range
    upper_red2 = np.array([180, 255, 255])  # Second red range
    
    # Mask for both ends of red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    # define range of yellow color in HSV
    lower_yellow = np.array([6, 100, 85])
    upper_yellow = np.array([40, 255, 255])

    # create a mask for yellow color
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    masks = {
        "Red": cv2.bitwise_or(mask1, mask2),
        "Yellow": cv2.inRange(hsv, lower_yellow, upper_yellow),
        "Blue": cv2.inRange(hsv, lower_blue, upper_blue)
    }

    for key, mask in masks.items():
        # Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        processed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        processed_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            continue
            # print(f"No {key} samples detected.") # debugging

        # Process contours
        rectangles = []
        hasMultiple = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area or area > max_area:
                # if the detected area is too small or large, skip
                continue
            elif area > big_area:
                hasMultiple = True
                #TODO: logic to differentiate/seperate multiple samples
                # EITHER HERE OR AFTER ASPECT RATIO CHECK
                # print(area)
        
            # Get rotated rectangle
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
        
            # Aspect ratio filtering
            width = min(rect[1])
            height = max(rect[1])
            aspect_ratio = float(width) / height
            if 0.4 < aspect_ratio < 1:  # Adjust aspect ratio limits as needed
                rectangles.append(box)

                # saving largest contour to send to robot
                if hasMultiple: # TEMP - restrict Multiple from being sent to Robot
                    continue # ignores touching samples
                if largestContour.size == 0:
                    largestContour = contour
                    largestColor = key
                elif cv2.contourArea(contour) > cv2.contourArea(largestContour):
                    largestContour = contour
                    largestColor = key
    
        # Draw rectangles and label detected samples
        for i, rectangle in enumerate(rectangles):
            text = key
            if hasMultiple:
                # multiple samples detected and touching each other
                text = f"Multiple {text}"
            cv2.drawContours(image, [rectangle], 0, (0, 255, 0), 2)
        
            # Get center of the rectangle
            M = cv2.moments(rectangle)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                

            
                # Draw circle and label
                cv2.circle(image, (cX, cY), 5, (255, 0, 0), -1)
                cv2.putText(image, f"{text} {i+1}", (cX - 20, cY - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
        # Update llpython with the number of rectangles found
        llpython[0] += len(rectangles)
    
    # Add overall status text
    cv2.putText(image, f"Found {llpython[0]} samples", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if largestContour.size != 0:
        # Get the minimum area rectangle
        rect = cv2.minAreaRect(largestContour)
        angle = rect[2] # Orientation angle
        width, height = rect[1]
        
        # Normalize the angle to [0, 180) degrees
        if width < height:
            angle = 90 + angle  # Adjust for vertical rectangles

        # Convert to [0, 180) range
        if angle < 0:
            angle += 180

        llpython[1] = angle # send angle to robot
        llpython[2] = {"Red": 1, "Yellow": 2, "Blue": 3}.get(largestColor, 0) # encode color
        text = f"Orientation: {int(angle)}, Color: {largestColor}"
    else:
        text = "No valid contour fond"
        llpython[1] = 0
        llpython[2] = 0

    # Display orientation and color on the image
    cv2.putText(image, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    '''
    # send back to robot
    for i in range(len(llpython)):
        print(llpython[i], i)
    '''
    
    return largestContour, image, llpython
    #llypython returns [number of objects detected, angle, and the encoded color of the object]
