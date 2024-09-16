import cv2
import tensorflow as tf
import tensorflow_hub as hub

model = hub.load('https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2')
coco_classes = [
    "background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", 
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", 
    "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", 
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", 
    "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", 
    "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "TV", 
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", 
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

grocery_items = {
    47: "apple",
    49: "orange",
    50: "banana",
    52: "carrot",
    53: "broccoli",
    44: "bottle",
    41: "cup",
    45: "bowl"
}


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_resized = cv2.resize(frame, (320, 320))
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    input_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.uint8)
    input_tensor = tf.expand_dims(input_tensor, axis=0)  # Add batch dimension

    results = model(input_tensor)

    detection_scores = results['detection_scores'].numpy()[0]
    detection_classes = results['detection_classes'].numpy()[0].astype(int)
    detection_boxes = results['detection_boxes'].numpy()[0]

    for i in range(len(detection_scores)):
        if detection_scores[i] > 0.5:  # Confidence threshold
            class_id = detection_classes[i]

            if class_id in grocery_items:
                class_name = grocery_items[class_id]

                #get boundaries for the box
                h, w, _ = frame.shape
                box = detection_boxes[i] * [h, w, h, w]
                y_min, x_min, y_max, x_max = box.astype(int)

                #make box
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name}: {detection_scores[i]:.2f}", (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
    cv2.imshow('Grocery Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()