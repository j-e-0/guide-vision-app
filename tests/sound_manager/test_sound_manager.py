import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.sound_manager import SoundManager

class TestSoundManager(unittest.TestCase):

    def test_read_wave(self):
        # Setup to simulate read WAV file
        with patch('wave.open', MagicMock()) as mock_wave_open:
            mock_wave = MagicMock()
            mock_wave.getnframes.return_value = 1024
            mock_wave.getsampwidth.return_value = 2
            mock_wave.getnchannels.return_value = 1
            mock_wave.readframes.return_value = (b'\x01\x02' * 512)
            mock_wave_open.return_value.__enter__.return_value = mock_wave

            manager = SoundManager()
            audio_array, rate = manager.read_wave('path/to/sound.wav')

            self.assertEqual(audio_array.shape, (512, 1))  # 512 samples, 1 channels
            self.assertEqual(rate, mock_wave.getframerate.return_value)
            mock_wave.readframes.assert_called_once_with(1024)

    def test_stereo_panning(self):
        audio_array = np.array([[1000, 1000]] * 10, dtype=np.int16)
        manager = SoundManager()
        panned_audio = manager.stereo_panning(audio_array, panning=0.5)
        
        expected_left_gain = np.cos(1.5 * np.pi / 4)
        expected_right_gain = np.sin(1.5 * np.pi / 4)
        
        audio_left_int16 = (audio_array[:, 0] * expected_left_gain).astype(np.int16)
        audio_right_int16 = (audio_array[:, 1] * expected_right_gain).astype(np.int16)
        
        np.testing.assert_array_almost_equal(panned_audio[:, 0], audio_left_int16)
        np.testing.assert_array_almost_equal(panned_audio[:, 1], audio_right_int16)

    def test_change_audio_speed(self):
        audio_array = np.arange(30).reshape((15, 2))
        manager = SoundManager()
        speed_up_audio = manager.change_audio_speed(audio_array, 0.5)
        
        self.assertEqual(len(speed_up_audio), 30)

    @patch('sounddevice.play')
    @patch('sounddevice.wait')
    def test_play_audio(self, mock_wait, mock_play):
        with patch.object(SoundManager, 'read_wave') as mock_read_wave, \
             patch.object(SoundManager, 'stereo_panning') as mock_stereo_panning, \
             patch.object(SoundManager, 'change_audio_speed') as mock_change_speed:
            
            mock_read_wave.return_value = (np.zeros((10, 2)), 44100)
            mock_stereo_panning.return_value = np.zeros((10, 2))
            mock_change_speed.return_value = np.zeros((5, 2))

            manager = SoundManager()
            manager.play_audio()

            mock_play.assert_called_once()
            mock_wait.assert_called_once()

if __name__ == '__main__':
    unittest.main()