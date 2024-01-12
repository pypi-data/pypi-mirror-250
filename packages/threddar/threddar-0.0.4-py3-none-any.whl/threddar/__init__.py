import threading
from threddar.rethread import *

# The class for a threddar instance
class Threddar(list[threading.Thread, Thread]):
    """
    Initiate a threddar instance.

    ...

    Parameters
    -----------

    threads: list[Thread] = threads to include
    """

    def append(self, *args: list[Thread, threading.Thread]):
        """Add a thread to the threddar."""
        for arg in args:
            if isinstance(arg, threading.Thread) or isinstance(arg, Thread):
                list.append(self, arg)
            else:
                raise TypeError("Cannot append non-thread to Threddar.")

    # Args are threads to include
    def __init__(self, *args: list[Thread, threading.Thread]):
        self.append(*args)
    
    def join(self):
        """
        Runs thread.join() on each thread and finally returns the results.
        Results will be list[None] if not using rethread.

        Returns list[any]
        """
        results = []
        for thread in self:
            results.append(thread.join())
        return results

    def start(self):
        """
        Runs thread.start() on each thread.
        """
        for thread in self:
            thread.start() 