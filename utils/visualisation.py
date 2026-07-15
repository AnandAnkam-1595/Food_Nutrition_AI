from pathlib import Path
import cv2

from config import OUTPUT_DIR


class Visualizer:
    """
    Draw bounding boxes and labels on detected food items.
    """

    def __init__(self):
        self.output_dir = OUTPUT_DIR

    def draw_detections(self, image_path, detections):
        """
        Draw bounding boxes on the image.

        Args:
            image_path (str): Input image path.
            detections (list): Detection results.

        Returns:
            str: Saved image path.
        """

        image = cv2.imread(str(image_path))

        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            food = detection["food"]

            confidence = detection["confidence"]

            label = f"{food} ({confidence:.2f})"

            # Green bounding box
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Label background
            cv2.rectangle(
                image,
                (x1, y1 - 30),
                (x1 + 220, y1),
                (0, 255, 0),
                -1
            )

            # Label text
            cv2.putText(
                image,
                label,
                (x1 + 5, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )

        output_path = self.output_dir / "detected_food.jpg"

        cv2.imwrite(str(output_path), image)

        return str(output_path)