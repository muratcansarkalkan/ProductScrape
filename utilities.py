from threading import Thread

# Defined the object as ID (Specific for BOTH Amazon & Trendyol), title, price, product link
class ProductCard():
    def __init__(self, id, title, price, link):
        self.id = id
        self.title = title
        self.price = price
        self.link = link

# Defines the properties of threaded function with return value.
# This class helps us to have return of lists from our parsing functions.
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return