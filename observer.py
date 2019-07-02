class Observer:
    def __init__(self):
        self.subject = None

    def Notify(self, target, notificationEventType):
        pass


class Observable:
    def __init__(self):
        self.observers = []

    def NotifyAll(self, notificationEventType):
        for o in self.observers:
            o.Notify(self, notificationEventType)

    def AddObserver(self, observer):
        self.observers.append(observer)
        observer.subject = self
        # print 'AddObserver', observer, observer.subject

    def RemoveObserver(self, observer):
        # print 'RemoveObserver', observer, self
        observer.subject = None
        self.observers.remove(observer)
