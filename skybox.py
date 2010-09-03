# this is only a snippet
self.skybox = loader.loadModel("data/models/skybox.egg")
self.skybox.setBin("background", 1)
self.skybox.setDepthWrite(0)
self.skybox.setDepthTest(0)
self.skybox.setLightOff()
self.skybox.reparentTo(render)
