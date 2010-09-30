from text3d import Text3D

#TODO   exampleTask umbenennen
#       in dem Task die Tasten abfangen
#       Immer den aktuellen Eintrag hervorheben

class Menu(object):

    def __init__(self, newgame, device):
        #Test for 3D-Text
        self.text = Text3D(_("NewGame"))
        newgame()
        print "Direc", device.directions
        taskMgr.add(self.exampleTask, 'MyTaskName')
        
    # This task runs for two seconds, then prints done
    def exampleTask(self, task):
        if task.time < 2.0:
            return task.cont
        print 'Done'
        return task.done


if __name__ == "__main__":
    import main
