import cv2
import tensorflow as tf

# Load pre-trained object detection model
model = tf.saved_model.load(r'C:\Users\Magshimim\PycharmProjects\stuff\madait\56_32')


# Get the inference function from the saved model
infer = model.signatures["serving_default"]


VIDEO = "best_cars.mp4"

CAR_TYPE = 3


def detect_objects(frame):  # Function to detect objects in a frame
    # Convert the frame to uint8
    frame1 = tf.convert_to_tensor(frame, dtype=tf.uint8)

    # Expand dimensions to create a batch of size 1
    input_tensor = tf.expand_dims(frame1, 0)

    try:
        # Perform inference
        detections = infer(input_tensor)
        return detections

    except Exception as e:
        print("Error during inference:", e)
        return None


def extract_car_positions(frame_from_video, detections, confidence_threshold=0.4):
    # The 'detections' variable should contain the output of the object detection model
    # The exact structure may vary based on the model, so adjust accordingly

    # Filter detections based on confidence threshold
    boxes = detections['detection_boxes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()
    classes = detections['detection_classes'][0].numpy()

    object_boxes = {}
    for i in range(len(boxes)):
        if classes[i] == CAR_TYPE and scores[i] >= confidence_threshold:
            ymin, xmin, ymax, xmax = boxes[i]
            im_height, im_width, _ = frame_from_video.shape

            # Convert normalized coordinates to pixel values
            xmin = int(xmin * im_width)
            xmax = int(xmax * im_width)
            ymin = int(ymin * im_height)
            ymax = int(ymax * im_height)

            object_boxes[(xmin, ymin, xmax, ymax)] = int(classes[i])

    return object_boxes


def draw_rects(frame, objects_positions):
    car_cnt = 0

    for box, typ in objects_positions.items():
        car_cnt += 1

        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(frame, f"Car: {car_cnt}", (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)


def main():
    cap = cv2.VideoCapture(VIDEO)

    ret, img = cap.read()
    rows, cols, _ = img.shape

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        frame = frame[250:rows, 650:cols]

        if not ret:
            break

        if True or count % 3 == 0:
            # Detect cars
            detections = detect_objects(frame)

            # Extract car positions
            car_positions = extract_car_positions(frame, detections)
            draw_rects(frame, car_positions)

        cv2.imshow("Car Detection", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break

        count += 1


if __name__ == "__main__":
    main()
