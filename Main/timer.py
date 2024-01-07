import time
import threading
class timer():
    def __init__(self, max):
        self.max = max
        self.timesUp = False
        self.running = False
        self.passed = 0
    
    def toggle(self):
        if self.running:
            self.running = False
        else:
            self.running = True
            threading.Thread(target=self.update).start()
        
    def update(self):
        start = time.time()
        elapsed = self.passed
        while self.running and not self.timesUp:
            self.passed = time.time() - start + elapsed
            if self.passed % 60 >= self.max:
                self.running = False
                self.timesUp = True
    
    def fetchtime(self):
        timeLeft = self.max - self.passed
        return f"{int(timeLeft // 60):02d}:{int(timeLeft % 60):02d}:{int((timeLeft % 1) * 100):02d}"