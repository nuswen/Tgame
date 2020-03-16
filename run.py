#from app import app
#app.run()

from threading import Thread
 
class MyThread(Thread):

    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        from app import app
        app.run()
    
def create_threads():
    my_thread = MyThread('bot')
    my_thread.start()
 
 
if __name__ == "__main__":
    create_threads()
    print('hi')