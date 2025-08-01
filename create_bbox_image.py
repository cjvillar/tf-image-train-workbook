import cv2
import csv
import os

def draw_bbox(event, x, y, flags, param):
    
    state = param
    if event == cv2.EVENT_LBUTTONDOWN:
        state["drawing"] = True
        state["start"] = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and state["drawing"]:
        img_copy = state["image"].copy()
        cv2.rectangle(img_copy, state["start"], (x, y), (0, 255, 0), 2)
        cv2.imshow("Image", img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        state["drawing"] = False
        end = (x, y)
        x1, x2 = sorted([state["start"][0], end[0]])
        y1, y2 = sorted([state["start"][1], end[1]])
        state["bbox"] = (x1, y1, x2, y2)
        cv2.rectangle(state["image"], (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Image", state["image"])

def process_image(image_path, csv_file):
    image = cv2.imread(image_path)
    state = {
        "image": image,
        "start": (0, 0),
        "bbox": None,
        "drawing": False,
    }

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_bbox, param=state)
    cv2.imshow("Image", image)

    print('\nImage:', image_path)
    print("Draw a box. Then press 's' to save, or 'q' to skip.")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s") and state["bbox"]:
            x1, y1, x2, y2 = state["bbox"]
            data = [os.path.basename(image_path), x1, y1, x2, y2]
            file_exists = os.path.exists(csv_file)
            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["image_name", "bbox_x_min", "bbox_y_min", "bbox_x_max", "bbox_y_max"])
                writer.writerow(data)
            print(f"Saved to {csv_file}")
            break

    cv2.destroyWindow("Image")

def main():
    image_dir = "./image_scrape_code/screenshots/"
    csv_file = "bbox_data.csv"
    image_paths = [
        os.path.join(image_dir, fname)
        for fname in sorted(os.listdir(image_dir))
        if fname.endswith(".png")
    ]

    for img_path in image_paths:
        process_image(img_path, csv_file)
        # wait to go to next
        while True:
            key = cv2.waitKey(0) & 0xFF
            if key in [ord("s"), ord("q")]:
                break
            print("Press 's' to save and continue, or 'q' to quit.")
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    print("All done.")

if __name__ == "__main__":
    main()
