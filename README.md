# Camera Calibration

## Capture mode
This mode is provided to capture chessboard images in 1 second interval for using at calibration mode. Captured images will be stored in images folder.

```commandline
python main.py --capture --camera_url '0'
```

## Calibration mode
This mode is provided to start the calibration process using the captured images. Square size should also be provided in centimeters.

```commandline
python main.py --calibrate --square_size 1.6
```

## Test mode
This mode is for testing the calibration on real image in test_images folder. Please provide your test images in that directory.

```commandline
python main.py --test
```