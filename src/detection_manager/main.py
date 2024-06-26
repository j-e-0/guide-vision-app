import cv2
import numpy as np

class DetectionManager:
    def __init__(self) -> None:
        with open("assets/yolov4/coco.names", 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        
        self.classes = classes
        self.net = cv2.dnn.readNet('assets/yolov4/yolov4.weights', 'assets/yolov4/yolov4.cfg')
        self.cap = cv2.VideoCapture(0)
    
    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
    def calculate_percents(self, size_obj_estimate):
        percents = {}
        
        # Calculate percent with major size object defined in your category ('left', 'left_med', ...)
        for orientation in size_obj_estimate:
            percents[orientation] = max(size_obj_estimate[orientation]['obj_sizes']) / 100
        
        return percents
        
    def processing(self):
        _, frame = self.cap.read()
        if frame is None or not isinstance(frame, np.ndarray):
            print("Error reading frame or frame is not a NumPy array")
            return None
            
        # Convert Frame to Blob
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        
        # Getting output layer names of Yolov4
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers().flatten()]

        # Detection
        outs = self.net.forward(output_layers)
        
        frame_height, frame_width = frame.shape[:2]
        third_width = frame_width / 5
        size_obj_estimate = {
            "left": {"obj_counts": 0, "obj_sizes": [0]},
            "left_med": {"obj_counts": 0, "obj_sizes": [0]},
            "center": {"obj_counts": 0, "obj_sizes": [0]},
            "right_med": {"obj_counts": 0, "obj_sizes": [0]},
            "right": {"obj_counts": 0, "obj_sizes": [0]}
        }
        
        # Displaying information on the screen
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.4:
                    # Detection object
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    w = int(detection[2] * frame_width)
                    h = int(detection[3] * frame_height)

                    # Coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # Determining the horizontal positions
                    if center_x < third_width:
                        position = "left"
                    elif center_x <= 2 * third_width:
                        position = "left_med"
                    elif center_x > 3 * third_width and center_x < 4 * third_width:
                        position = "right_med"
                    elif center_x >= 4 * third_width:
                        position = "right"
                    else:
                        position = "center"

                    # Counter of objects and your sizes 
                    size_obj_estimate[position]["obj_counts"] += 1
                    size_obj_estimate[position]["obj_sizes"].append(((w * h) * 100) / (frame_width * frame_height))

                    # Drawing a rectangle with labels
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    label = "{}: {:.2f}% Position: {}".format(self.classes[class_id], confidence * 100, position)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Image", frame)
        cv2.waitKey(1)
        
        return self.calculate_percents(size_obj_estimate)
