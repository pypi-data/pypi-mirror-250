from threading import Thread as thread

# This is basically a wrapper around the threading module which allows you to do stuff way easier.
# You are free to use it to your will.
# -Threddar 2024

class Thread(thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        thread.join(self, *args)
        return self._return