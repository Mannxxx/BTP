import cv2
import numpy as np
import csv

# Replace 'input_video.mp4' with the path to your video file
video_path = 'D:/BTP/CODE/Diving board/Diving.mp4'
cap = cv2.VideoCapture(video_path)

def nothing(x):
    pass

cv2.namedWindow("Frame")
cv2.createTrackbar("quality", "Frame", 2, 10, nothing)  # Adjust initial quality value

# Open a CSV file for writing the corner coordinates
csv_file = open('corner_coordinates.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Frame', 'X', 'Y'])

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
     
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    quality = cv2.getTrackbarPos("quality", "Frame")
    quality = quality / 100 if quality > 0 else 0.01

    corners = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
    corners = cv2.dilate(corners, None)

    corners = corners > corners.max() * quality
    corner_indices = np.argwhere(corners)             

    for i, j in corner_indices:
        x, y = j, i
        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        # Write corner coordinates to CSV
        csv_writer.writerow([frame_count, x, y])

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(0)
    if key == 27:
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

# Close the CSV file
csv_file.close()
