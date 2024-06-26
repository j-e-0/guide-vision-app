import unittest
from unittest.mock import patch, Mock
import numpy as np
from src.detection_manager import DetectionManager

class TestDetectionManager(unittest.TestCase):
    def setUp(self):
        # Mocking of file and camera
        self.patcher_file = patch('builtins.open', unittest.mock.mock_open(read_data="person\nbicycle\ncar"))
        self.patcher_cv2 = patch('cv2.VideoCapture')
        self.mock_file = self.patcher_file.start()
        self.mock_video = self.patcher_cv2.start()

        # Configuring a dummy object of VideoCapture
        self.mock_video.return_value.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

    def tearDown(self):
        self.patcher_file.stop()
        self.patcher_cv2.stop()

    def test_init(self):
        manager = DetectionManager()
        self.assertEqual(manager.classes, ['person', 'bicycle', 'car'])

    def test_stop(self):
        manager = DetectionManager()
        with patch('cv2.destroyAllWindows') as mock_destroy:
            manager.stop()
            self.assertTrue(manager.cap.release.called)
            mock_destroy.assert_called_once()

    def test_calculate_percents(self):
        manager = DetectionManager()
        input_data = {
            "left": {"obj_sizes": [50, 100]},
            "center": {"obj_sizes": [75]},
            "right": {"obj_sizes": [80, 120]}
        }
        expected_output = {
            "left": 1.0,
            "center": 0.75,
            "right": 1.2
        }
        self.assertEqual(manager.calculate_percents(input_data), expected_output)

    def test_recognition_object(self):
        expected_output = {'center': 0.01, 'left': 0.0, 'left_med': 0.0, 'right': 0.0, 'right_med': 0.0}
        
        manager = DetectionManager()
        with patch('cv2.dnn.blobFromImage'), patch('cv2.dnn_Net.setInput'), \
             patch('cv2.dnn_Net.forward', side_effect=[[np.array([np.array([0.5, 0.5, 0.1, 0.1, 0.6, 0.8])])]]):
            result = manager.processing()
            self.assertEqual(result, expected_output, "The processing method should correctly recognized person.")

    def test_not_recognition_object(self):
        expected_output = {'center': 0.00, 'left': 0.0, 'left_med': 0.0, 'right': 0.0, 'right_med': 0.0}
        
        manager = DetectionManager()
        with patch('cv2.dnn.blobFromImage'), patch('cv2.dnn_Net.setInput'), \
             patch('cv2.dnn_Net.forward', side_effect=[[np.array([np.array([0.5, 0.5, 0.1, 0.1, 0.6, 0.3])])]]):
            result = manager.processing()
            self.assertEqual(result, expected_output, "The processing method should correctly not recognized.")

    def test_not_captured_video(self):
        self.mock_video.return_value.read.return_value = (True, None)
        
        manager = DetectionManager()
        output = manager.processing()
        self.assertIsNone(output) 
        self.setUp()

if __name__ == '__main__':
    unittest.main()