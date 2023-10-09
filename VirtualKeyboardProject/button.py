import cv2

class Button():
    
    def __init__(self, pos, text, size=None) -> None:
        
        if size is None:
            size = [85, 85]

        self.pos = pos
        self.text = text
        self.size = size
        self.state = False
        self.prepressed = False
        
    def draw(self, img):
        
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (0,255,0), cv2.FILLED)
        cv2.putText(img, self.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                (255, 255, 255), 4)
        return img
    
    def reset_state(self):
        self.state = False