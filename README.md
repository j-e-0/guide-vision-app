# Guide Vision App

This project aims to facilitate the interpretation of environments in a spatial auditory way, using a sound balance technique and reproduction sound speed to read the environment, using the device's camera.

Its main benefit at the moment is for people with visual impairments, where it is possible to locate themselves more efficiently, considering obstacles in their path and hearing how to know the proximity and location of some objects.

This project includes modules for managing audio operations and video processing, focusing on object detection and audio file manipulation. The core classes are `SoundManager` for audio and `DetectionManager` for visual detection.

This project is in the study stage to improve detection techniques and improve the ability to transpile to other languages.

## Requirements

Before running the project, install the dependencies listed in the `requirements.txt` file. To install, execute:

```bash
pip install -r requirements.txt
```

Key libraries used include:

- OpenCV
- NumPy
- sounddevice

Download YOLOv4 Weights (`yolov4.weights`) and put on path `assets/yolov4/`

## Example Operation App

![objects detection](/docs/guide_vision_operation.png "Example objects detection").

## Running Project

On the root path:

- **Application**

```bash
python -m src.app_manager.main
```

- **Tests**

```bash
python -m unittest
```

## Directory Structure

The project is organized in the following directory structure:

- **Root Folder**:
  - `requirements.txt`: Contains all the Python dependencies required for the project.
  - `README.md`: Documentation of the project.
  - **src/**: Contains the source code modules.
    - `app_manager`: Module that contains the `AppManager` class and your dependencies files.
    - `sound_manager`: Module that contains the `SoundManager` class and your dependencies files.
    - `detection_manager`: Module that contains the `DetectionManager` class and your dependencies files.
  - **test/**: Unit tests for the project.
  - **assets/**: Dependencies files to run packages (Weights YOLOV4, Sounds, ...)
  - **docs/**: Additional documentation and references.

## Package Descriptions

### AppManager

The `AppManager` class is the initializer App to centralize functions and logics. Your responsibilities start detection camera, parse values after object detection and play sound with certain parameters.

### DetectionManager

The `DetectionManager` class is designed for real-time object detection using the device's camera. It utilizes pre-trained YOLOv4 models for detection. Main features:

- **Initialization**: Loads detection model weights and configuration and starts video capture.
- **Frame Processing**: Reads frames from the camera, performs object detection, and marks detected objects with rectangles and labels.
- **Calculating Percentages**: Calculates the percentage of the total frame area that each detected object occupies.
- **Stopping**: Releases camera resources and closes all OpenCV windows.

### SoundManager

The `SoundManager` class provides functionalities to load, manipulate, and play audio files. Key features include:

- **Reading WAV Files**: Loads a WAV file and returns a NumPy array along with the sampling rate.
- **Stereo Panning**: Applies stereo panning to an audio array, adjusting the balance between left and right channels.
- **Changing Audio Speed**: Modifies the playback speed of the audio.
- **Playing Audio**: Loads an audio file, applies stereo panning and speed change, and plays the result.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### References

This project uses the following open source software:

[OpenCV](https://opencv.org/): Library for computer vision and image processing.
YOLO (You Only Look Once): Real-time object detection system.
[sounddevice](https://python-sounddevice.readthedocs.io/): Library for playing and recording sound in Python, based on the PortAudio library.
