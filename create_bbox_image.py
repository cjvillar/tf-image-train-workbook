import cv2
import csv
import os

# var to store bbox coord
bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max = 0, 0, 0, 0
drawing = False

# mouse callback func
def draw_bbox(event, x, y, flags, param):
    global bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max, drawing, image

    if event == cv2.EVENT_LBUTTONDOWN:
        bbox_x_min, bbox_y_min = x, y
        drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        bbox_x_max, bbox_y_max = x, y
        drawing = False
        cv2.rectangle(image, (bbox_x_min, bbox_y_min), (bbox_x_max, bbox_y_max), (0, 255, 0), 2)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            image_copy = image.copy()
            cv2.rectangle(image_copy, (bbox_x_min, bbox_y_min), (x, y), (0, 255, 0), 2)
            cv2.imshow('Image', image_copy)
        else:
            cv2.imshow('Image', image)

# def menu options
menu_options = [
    ('Press "s" to Save and Go to Next Image', 's'),
    ('Press "q" to Quit without Saving', 'q')
]

# func to process the current image
def process_image(image_path):
    global image, bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max

    # load image
    image = cv2.imread(image_path)

    # create a window and set mouse callback func
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_bbox)

    # display image
    cv2.imshow('Image', image)

    # print menu options
    for option in menu_options:
        print(option[0])

    # loop to wait for user to draw the bbox or choose an option
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  #  quit without saving
            break
        elif key == ord('s'):  # save the bounding box coordinates
           
            image_name = os.path.basename(image_path)
            data = [image_name, bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max]

            csv_file = 'bbox_data.csv'
            file_exists = os.path.isfile(csv_file)
            #save
            with open(csv_file, 'a') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['image_name', 'bbox_x_min', 'bbox_y_min', 'bbox_x_max', 'bbox_y_max'])
                writer.writerow(data)

            print(f"Bounding box coordinates saved to {csv_file}")
            break

    # closes current window
    cv2.destroyAllWindows()

# dir containing the images
image_dir = './image_scrape_code/screenshots/'

# list of image file paths in the dir
image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.png')]

# loop through images
for image_path in image_paths:
    process_image(image_path)

    # loop to wait for user input to proceed to the next image
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord('s') or key == ord('q'): 
            break
        else:
            print("Invalid option. Press 's' to save and go to the next image or 'q' to quit.")
    if key == ord('q'):
        break

# closes all windows
cv2.destroyAllWindows()