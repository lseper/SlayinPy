# # a file to represent Observers

# class Observable:
#     def __init__(self):
#         self._observers = []
    
#     def register_observer(self, observer):
#         self._observers.append(observer)
    
#     def notify_observers(self, *args, **kwargs):
#         for observer in self._observers:
#             observer.notify(self, *args, **kwargs)

# class Observer:
#     def __init__(self, observable):
#         observable.register_observer(self)
    
#     def notify(self, observable):
#         print(""Got", args, kwargs, "From", observable")

class Observable:
    def __init__(self):
        self._observers = []
    
    def register_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.notify(self)

class Observer:
    def __init__(self, observable):
        observable.register_observer(self)
        self.observable = observable
    
    def notify(self, msg):
        print(f"Player has passed the {msg} border")

subject = Observable() # create the thing to watch for 
observer = Observer(subject) # attach that thing to watch for to the thing that's watching it
subject.notify_observers() # notify the things watching this event that something has happened