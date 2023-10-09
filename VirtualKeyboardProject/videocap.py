import threading
import queue
import cv2
from queue import Queue

class VideoCapture:
    
    def __init__(self, idx, width=1280, height=720):
        
        self.cap = cv2.VideoCapture(idx)
        self.cap.set(3, width)
        self.cap.set(4, height)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # чтение фреймов в отдельном потоке
    def _reader(self):
        while True:
            r, frame = self.cap.read()
            if not r:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except Queue.Empty:
                    pass
            self.q.put((r, frame))

    def read(self):
        return self.q.get()