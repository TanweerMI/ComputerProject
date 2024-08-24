import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

video = cv2.VideoCapture(0)
labels = []

while True:
  ret, frame = video.read()
  bbox, label, conf = cv.detect_common_objects(frame)
  outputImage = draw_bbox(frame, bbox, label, conf)

  cv2.imshow("object", outputImage)

  for item in labels:
    if item in labels:
      pass

  if cv2.waitKey(1) & 0xFF == ord("q"):
    break
