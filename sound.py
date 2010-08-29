from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        #base = ShowBase()
        self.mySound = base.loader.loadSfx("data/sounds/vehicle01.ogg")
        self.speed = 0;
        if self.mySound.status() == self.mySound.READY:
            self.mySound.setLoop(True)
            #mySound.setPlayRate(2)
            self.mySound.setVolume(0.5)
            self.mySound.play()
        myTask = taskMgr.add(self.myFunction, 'myFunction')

    def myFunction(self, task):
        self.speed = self.speed + 0.1
        self.mySound.setPlayRate(self.speed)
        return task.cont



app = MyApp()
app.run()
