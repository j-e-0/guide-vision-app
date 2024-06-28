from src.detection_manager import DetectionManager
from src.sound_manager import SoundManager

class AppManager:
    
    def __init__(self) -> None:
        video_process = DetectionManager()
        alert_sound = SoundManager()

        while True:
            ## Size of objects between 0.0 and 1.0
            ## Proximily to 1 is bigger and proximily 0 is minner
            ## Value 0 no object detected in this orientation
            results = video_process.processing()
            
            ## Panning | Orientation
            ## -1      | Left
            ## -.5     | Left Med
            ## 0       | Center
            ## .5      | Right Med
            ## 1       | Right
            panning = -1
            
            for orientation in results:
                speed = results[orientation]
                
                if(speed > 0):
                    speed = 1.2 + round(speed,1)
                    alert_sound.play_audio(panning=panning, speed_factor=speed)
                                        
                panning +=.5
                
if __name__ == '__main__':
    AppManager()