import threading
import fanzub

class SearchThread(threading.Thread):
     def __init__(self,id,episode):
         threading.Thread.__init__(self)
         self.id=id
         self.episode=episode

     def run(self):
         