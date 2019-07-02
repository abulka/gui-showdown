import unittest
from observer import Observable, Observer

# pytest test_observer.py or just pytest


class TestObserver:
    def test_CanMakeObserverHookup(self):
        me = Observable()
        spriteview = Observer()
        me.AddObserver(spriteview)

        assert spriteview in me.observers
        assert spriteview.subject == me

    def test_NotificationOccurs(self):
        class Watcher(Observer):
            state = 0

            def Notify(self, target, notificationEventType):
                Watcher.state += 1

        class Model(Observable):
            def Add(self):
                self.NotifyAll(notificationEventType="")

        me = Model()
        o = Watcher()
        me.AddObserver(o)
        assert Watcher.state == 0
        me.Add()
        assert Watcher.state == 1

        me.Add()
        assert Watcher.state == 2

        me.RemoveObserver(o)

        me.Add()  # should be no notification, thus no change in Watcher state.
        assert Watcher.state == 2

    def test_NotificationOccurs02(self):
        class StateKeeper:
            state = 0

        class Watcher1(Observer):
            def Notify(self, target, notificationEventType):
                StateKeeper.state += 1

        class Watcher2(Observer):
            def Notify(self, target, notificationEventType):
                StateKeeper.state += 10

        class Model(Observable):
            def Add(self):
                self.NotifyAll(notificationEventType="")

        me = Model()
        o1 = Watcher1()
        o2 = Watcher2()
        me.AddObserver(o1)
        me.AddObserver(o2)
        assert StateKeeper.state == 0

        me.Add()
        assert StateKeeper.state == 11  # two notifications in a row did this.

        me.RemoveObserver(o1)
        me.Add()
        assert StateKeeper.state == 21  # one notification did this.
