class Observer:
    def __init__(self):
        self.subject = None

    def Notify(self, target, data):

        # TODO need equivalent general python broadcasting system - perhaps 'multicast' from pynsource?
        # document.dispatchEvent(new CustomEvent("observer-notification", {  // debug functions can listen for this
        #     detail: { target: target, data: data }
        #   }));      

        if target:
            print(f"  Observer {self.__class__} got notification from: {target.__class__}, data: '{data}'")
        else:
            print(f"Observer {self.__class__} got direct call to notify(), data: '{data}'")


class Observable:
    def __init__(self):
        self.observers = []

    def NotifyAll(self, data):
        for o in self.observers:
            print(f"Subject {self.__class__} notifying: {o.__class__} with: {data}")
            o.Notify(self, data)

    def AddObserver(self, observer):
        self.observers.append(observer)
        observer.subject = self

    def RemoveObserver(self, observer):
        observer.subject = None
        self.observers.remove(observer)
