import time

from utils import load_coefficients
import cv2
import argparse
import os
import random
from camera import Camera


def run(capture, calibrate, test, camera_url, square_size):
    if capture:

        # Standard path for the collected images
        path = "images"
        folder_exist = os.path.exists(path)
        number_images = 20

        # Create folder if not exist
        if not folder_exist:
            os.makedirs(path)

        camera = Camera(camera_url)

        while number_images > 0:
            if camera.get_frame().shape[0] != 3:
                # Print the number of images
                number_images -= 1
                print(f'Num of image taken: {20 - number_images}')

                frame = camera.get_frame()

                # Show frame
                cv2.imshow('frame', frame)
                cv2.waitKey(1)

                # Write frame to the defined standard path
                filename = f'{20 - number_images}.jpg'
                cv2.imwrite(os.path.join(path, filename), frame)

                time.sleep(1)
            else:
                time.sleep(1)

        print('Finished capturing, calibration can be processed')

    elif calibrate:
        from chessboard import calibrate_chessboard
        from utils import save_coefficients

        if square_size == '0':
            print('Please specify square size -> --square_size 1.6')
            exit()

        # Parameters
        path = 'images/'
        images_format = '.jpg'
        square_size = square_size
        width = 6
        height = 9

        print('Calibration started!')

        # Calibrate
        ret, mtx, dist, rvecs, tvecs = calibrate_chessboard(
            path,
            images_format,
            square_size,
            width,
            height
        )
        # Save coefficients into a file
        save_coefficients(mtx, dist, "calibration_chessboard.yml")

        print('Calibration successful!')

    elif test:
        # Load coefficients
        mtx, dist = load_coefficients('calibration_chessboard.yml')
        original = cv2.imread(random.choice(os.listdir('test_images')))
        dst = cv2.undistort(original, mtx, dist, None, None)
        cv2.imshow('undist', dst)
        cv2.waitKey(1)


def parse_opt():
    # Parse the arguments
    parser = argparse.ArgumentParser()

    # Arguments for capturing images
    parser.add_argument("--capture", action="store_true", help="Get images from camera for calibration")
    parser.add_argument("--camera_url", type=str, default='0', help="Url for the camera")

    # Arguments for calibration mode
    parser.add_argument("--calibrate", action="store_true", help="Start calibration")
    parser.add_argument('--square_size', type=float, default='0', help='Provide the size of the square in chessboard')

    # Argument for testing
    parser.add_argument("--test", action="store_true", help="Test it!")

    option = parser.parse_args()

    return option


def main(options):
    run(**vars(options))


if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
