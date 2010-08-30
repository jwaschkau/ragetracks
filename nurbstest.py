# _*_ coding: UTF-8 _*_
###################################################################
## TEST FOR NURBS http://www.panda3d.org/manual/index.php/Other_Vertex_and_Model_Manipulation
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        ShowBase.__init__(self)
        base.setFrameRateMeter(True) #Show the Framerate

        #curve = NurbsCurve()
        #curve.appendCv(0,0,0)
        #curve.appendCv(10,10,10)
        #curve.appendCv(50,60,10)
        #curve.appendCv(10,-60,50)
        #curve.recompute()
        #curve.writeEgg("test.egg")

        mdl = loader.loadModel("test.egg")
        mdl = loader.loadModel("data/models/vehicle01.egg")
        mdl.reparentTo(render)


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

# this code is only executed if the module is executed and not imported
if __name__ == "__main__":
    game = Game()
    game.run()




