"""
label_images.py
---------------
Crop YouTube screenshots to just the video frame, then label them
as "person" or "not_person" with a single keypress.

Controls:
  P  → label as "person"
  N  → label as "not_person"
  Q  → quit and save progress

Output:
  - Cropped images saved to ./cropped/<label>/
  - labels.csv with columns: original_file, cropped_file, label

Usage:
  python label_images.py
  python label_images.py --input ./screenshots --crop 15 68 843 462
"""

import cv2
import csv
import os
import shutil
import argparse

# ── Default crop region (x, y, width, height) ────────────────────────────────
# Measured from the screenshot you shared. Adjust if your resolution differs.
DEFAULT_CROP = (15, 68, 843, 462)
# ─────────────────────────────────────────────────────────────────────────────

LABELS = {
    ord("p"): "person",
    ord("n"): "not_person",
}

def setup_dirs(base):
    for label in ["person", "not_person"]:
        os.makedirs(os.path.join(base, label), exist_ok=True)

def already_labelled(csv_path):
    """Return set of original filenames already in the CSV."""
    done = set()
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                done.add(row["original_file"])
    return done

def crop_image(image, x, y, w, h):
    ih, iw = image.shape[:2]
    x2 = min(x + w, iw)
    y2 = min(y + h, ih)
    return image[y:y2, x:x2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="./screenshots", help="Folder of raw screenshots")
    parser.add_argument("--output", default="./processed_images",     help="Output folder for cropped images")
    parser.add_argument("--csv",    default="labels.csv",    help="CSV file to write labels to")
    parser.add_argument("--crop",   nargs=4, type=int,
                        metavar=("X", "Y", "W", "H"),
                        default=list(DEFAULT_CROP),
                        help="Crop region in pixels")
    args = parser.parse_args()

    x, y, w, h = args.crop
    setup_dirs(args.output)

    # Load all PNGs, skip already-labelled ones
    all_files = sorted(f for f in os.listdir(args.input) if f.lower().endswith(".png"))
    done = already_labelled(args.csv)
    pending = [f for f in all_files if f not in done]

    if not pending:
        print("No new images to label.")
        return

    print(f"{len(pending)} image(s) to label. {len(done)} already done.")
    print("Controls:  P = person   N = not_person   Q = quit\n")

    csv_exists = os.path.exists(args.csv)
    csv_file   = open(args.csv, "a", newline="")
    writer     = csv.writer(csv_file)
    if not csv_exists:
        writer.writerow(["original_file", "cropped_file", "label"])

    cv2.namedWindow("Label", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Label", w, h)

    labelled = 0

    for idx, fname in enumerate(pending):
        fpath = os.path.join(args.input, fname)
        image = cv2.imread(fpath)

        if image is None:
            print(f"  Skipping unreadable file: {fname}")
            continue

        cropped = crop_image(image, x, y, w, h)

        # Overlay progress text on a copy for display
        display = cropped.copy()
        progress = f"{idx + 1}/{len(pending)}"
        cv2.putText(display, progress, (10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, "P=person  N=not_person  Q=quit", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

        cv2.imshow("Label", display)

        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == ord("q"):
                print(f"\nQuitting. Labelled {labelled} image(s) this session.")
                csv_file.close()
                cv2.destroyAllWindows()
                return
            if key in LABELS:
                label = LABELS[key]
                # Save cropped image into the label subfolder
                cropped_name = f"{os.path.splitext(fname)[0]}_{label}.png"
                cropped_path = os.path.join(args.output, label, cropped_name)
                cv2.imwrite(cropped_path, cropped)
                writer.writerow([fname, cropped_path, label])
                csv_file.flush()
                labelled += 1
                print(f"  [{progress}] {fname} → {label}")
                break
            # Any other key: re-show instructions
            print("  Press P (person), N (not_person), or Q (quit).")

    csv_file.close()
    cv2.destroyAllWindows()
    print(f"\nAll done. Labelled {labelled} image(s). Results in {args.csv}")


if __name__ == "__main__":
    main()
