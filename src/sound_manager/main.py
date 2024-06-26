import sounddevice as sd
import numpy as np
import wave

class SoundManager: 
        
    def read_wave(self, file_path):
        """Upload a WAV file and return an NumPy array and sampling rate"""
        with wave.open(file_path, 'rb') as wav:
            frames = wav.readframes(wav.getnframes())
            dtype = np.int16 if wav.getsampwidth() == 2 else np.float32
            audio_array = np.frombuffer(frames, dtype=dtype)
            audio_array = audio_array.copy()
            audio_array = audio_array.reshape(-1, wav.getnchannels())
        return audio_array, wav.getframerate()

    def stereo_panning(self, audio_array, panning=0):
        """Apply stereo panning to audio array."""
        audio_float = audio_array.astype(np.float32)
        
        # Guaranting panning value rate is between -1 and 1
        panning = max(min(panning, 1), -1)
        
        # Calculate gains per channel
        gain_left = np.cos((panning + 1) * np.pi / 4)
        gain_right = np.sin((panning + 1) * np.pi / 4)
        
        # Apply gains
        audio_float[:, 0] *= gain_left
        audio_float[:, 1] *= gain_right
        
        # Convert output again to int16
        return audio_float.astype(np.int16)

    def change_audio_speed(self, audio_array, speed_factor):
        indices = np.round(np.arange(0, len(audio_array), speed_factor))
        indices = indices[indices < len(audio_array)].astype(int)
        return audio_array[indices.astype(int)]

    def play_audio(self, panning=0, speed_factor=0.6):
        """Upload, appling panning and play the WAV audio"""
        file_path = 'assets/sound/sound.wav'
        audio_array, samplerate = self.read_wave(file_path)
        panned_audio = self.stereo_panning(audio_array, panning=panning)
        adjusted_audio = self.change_audio_speed(panned_audio, speed_factor)

        sd.play(adjusted_audio, samplerate)
        sd.wait()