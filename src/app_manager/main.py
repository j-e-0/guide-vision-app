from src.detection_manager import DetectionManager
from src.sound_manager import SoundManager

class AppManager:
    
    def __init__(self) -> None:
        video_process = DetectionManager()
        alert_sound = SoundManager()

        while True:
            result = video_process.processing()
            
            left_speed = result["left"]
            left_med_speed = result["left_med"]
            center_speed = result["center"]
            right_med_speed = result["right_med"]
            right_speed = result["right"]
            
            ## Size of objects between 0 and 1
            ## Proximily to 1 is bigger and proximily 0 is minner
            ## Value 0 no object detected in this orientation
            print(result)

            if(left_speed > 0):
                speed = 1.2 + round(left_speed,1)
                alert_sound.play_audio(panning=-1, speed_factor=speed)
            
            if(left_med_speed > 0):
                speed = 1.2 + round(left_med_speed,1)
                alert_sound.play_audio(panning=-.5, speed_factor=speed)
            
            if(center_speed > 0):
                speed = 1.2 + round(center_speed,1)
                alert_sound.play_audio(panning=0, speed_factor=speed)
                
            if(right_med_speed > 0):
                speed = 1.2 + round(right_med_speed,1)
                alert_sound.play_audio(panning=.5, speed_factor=speed)
                
            if(right_speed > 0):
                speed = 1.2 + round(right_speed,1)
                alert_sound.play_audio(panning=1, speed_factor=speed)
                
if __name__ == '__main__':
    AppManager()