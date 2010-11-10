# -*- coding: utf-8 -*-
###################################################################
## this module represents one vehicle a player can control
###################################################################

from pandac.PandaModules import * #Load all PandaModules
from panda3d.core import TexGenAttrib
from wiregeom import WireGeom
from collisionray import CollisionRay
from direct.directnotify.DirectNotify import DirectNotify
from direct.particles.ParticleEffect import ParticleEffect
#Glow
from pandac.PandaModules import *
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.DirectObject import DirectObject

class Vehicle(object):
    '''
    '''
    def __init__(self, ode_world, ode_space, name = "standard"):
        '''
        '''
        self._notify = DirectNotify().newCategory("Vehicle")
        self._notify.info("New Vehicle-Object created: %s" %(self))
        self._ode_world = ode_world
        self._ode_space = ode_space
        self._model = None
        self._physics_model = None
        self._physics_mass = None
        self._collision_model = None
        self._speed = 0.0 #the actual speed of the vehicle (forward direction)
        self._direction = Vec3(0,0,0) #the direction the car is heading
        self._boost_direction = Vec3(0,0,0)
        self._boost_strength = 10.0 #the boost propertys of the vehicle
        self._control_strength = 1.5 #impact on the steering behaviour
        self._grip_strength = 0.5 #impact on the steering behaviour
        self._track_grip = 0.8 #impact on the steering behaviour
        self._energy = 100.0
        self._armor = 100.0
        self._max_energy = 100.0
        self._max_armor = 100.0
        self._weight = 400.0
        self._description = "The best vehicle ever"
        self._name = "The flying egg"
        self._brake_strength = 10.0
        self._hit_ground = True
        self._model_loading = False
        self._blowout = []
        
        #set up the propertys of the vehicle that schould be loaded
        #the methods get called because the data is immutable and 
        #wouldnt get updated when calling the objects directly
        #the last entry is the function to convert the string
        self._tags =    [["name",self.setName,str],
                        ["description",self.setDescription,str],
                        ["control_strength",self.setControlStrength,float],
                        ["grip_strength",self.setGripStrength, float],
                        ["track_grip",self.setTrackGrip,float],
                        ["max_energy",self.setMaxEnergy,float],
                        ["max_armor",self.setMaxArmor,float],
                        ["weight",self.setWeight,float],
                        ["brake_strength",self.setBrakeStrength,float]]

    # ---------------------------------------------------------
    
    def setVehicle(self, model):
        '''
        Choose what vehicle the player has chosen. This method initializes all data of this vehicle
        '''
        self.cleanResources()
        ##Seems not to work
        #self._notify.debug("Delete unused Nodes")
        #for node in self._blowout:
        #    node.removeNode()
        
        self._notify.debug("Set new vehicle: %s" %model)
        
        #Load the attributes of the vehicle
        attributes = model.find("**/Attributes")
        if attributes.isEmpty(): self._notify.warning("No Attribute-Node found")
        for tag in self._tags:
            value = attributes.getNetTag(tag[0])
            if value:
                self._notify.debug("%s: %s" %(tag[0],value))
                #translate the value if its a string
                if type(tag[2](value)) == str: tag[1](_(tag[2](value)))
                else: tag[1](tag[2](value))
            else: self._notify.warning("No value defined for tag: %s" %(tag[0]))
        
        blowout = model.find("**/Blowout")
        if not blowout.isEmpty():
            self._notify.debug("Loading Blowout-Particles")
            for node in blowout.getChildren():
                particle = ParticleEffect()
                self._blowout.append(particle)
                particle.loadConfig('./data/particles/blowout_test.ptf')
                particle.start(node)
                particle.softStop()
        else: self._notify.warning("No Blowout-Node found")
            
        print self._model
        if self._model != None: 
            heading  = self._model.getH()
            
            #display the attributes
            text = self._model.getParent().find("AttributeNode")
            if text: 
                node = text.find("name").node()
                node.setText(self._name)
                node.update()
                text.show()
            self._model.removeNode()
        else:
            heading = 160
        self._model = model
        self._model.setPos(0,0,2)
        self._model.setHpr(heading,0,0)
       
        #GlowTextur
        #self.glowSize=0
        #self.filters = CommonFilters(base.win, base.cam)
        #self.filters.setBloom(blend=(1,0,0,1),mintrigger=.6, maxtrigger=1, desat=-.5,intensity=3,size=1)
        #self.filters.setBloom(blend=(0,self.glowSize,0,0) ,desat=-2, intensity=3, size='medium')
        #tex = loader.loadTexture( 'data/textures/vehicle03_glow_map.jpg' )
        #ts = TextureStage('ts')
        #ts.setMode(TextureStage.MGlow)
        #self._model.setTexture(ts, tex)
       
        #Initialize the physics-simulation for the vehicle
        self._physics_model = OdeBody(self._ode_world)
        self._physics_model.setPosition(self._model.getPos(render))
        self._physics_model.setQuaternion(self._model.getQuat(render))        
        
        #Initialize the mass of the vehicle
        physics_mass = OdeMass()
        physics_mass.setBox(self._weight,1,1,1)
        self._physics_model.setMass(physics_mass)
        
        #Initialize the collision-model of the vehicle
        ##for use with blender models
        try:
            col_model = loader.loadModel("data/models/vehicles/%s.collision" %(self._model.getName()))
            self.collision_model = OdeTriMeshGeom(self._ode_space, OdeTriMeshData(col_model, True))
            self._notify.info("Loading collision-file: %s" %("data/models/vehicles/%s.collision" %(self._model.getName())))
        ##for fast collisions
        except:
            self._notify.warning("Could not load collision-file. Using standard collision-box")
            self.collision_model = OdeTriMeshGeom(self._ode_space, OdeTriMeshData(model, False))
            #self._collision_model = OdeBoxGeom(self._ode_space, 3,3,2)
        self._collision_model.setBody(self._physics_model)
        self._collision_model.setCollideBits(3)
        self._collision_model.setCategoryBits(2)

        #Add collision-rays for the floating effect
        self._ray = CollisionRay(Vec3(0,0,0), Vec3(0,0,-1), self._ode_space, parent = self._collision_model, length = 10.0)

        ##Overwrite variables for testing purposes
        self._grip_strength = 0.99
        self._track_grip = 0.99
        self._model_loading = False
        
    def toggleGlow(self):
        self.glowSize += .1
        print self.glowSize
        if (self.glowSize == 4): self.glowSize = 0
        self.filters.setBloom(blend=(0,self.glowSize,0,0) ,desat=-2, intensity=3, size='medium')
      
    def boggleGlow(self):
        self.glowSize -= .1
        print self.glowSize
        if (self.glowSize == 4): self.glowSize = 0
        self.filters.setBloom(blend=(0,self.glowSize,0,0) , desat=-2, intensity=3.0, size='medium')
        
    # ---------------------------------------------------------
    
    def setPos(self, x, y, z):
        '''
        '''
        self._model.setPos(x,y,z)
        
    def getPos(self):
        '''
        '''
        return self._model.setPos(x,y,z)
        
    position = property(fget = getPos, fset = setPos)
        
    # ---------------------------------------------------------
    
    def startBlowout(self):
        '''
        '''
        for particle in self._blowout:
            particle.softStart()
        
    def stopBlowout(self):
        '''
        '''
        for particle in self._blowout:
            particle.softStop()
        
    # ---------------------------------------------------------
    
    def setModel(self, model):
        '''
        '''
        self._model = model
        
    def getModel(self):
        '''
        '''
        return self._model
        
    model = property(fget = getModel, fset = setModel)
        
    # ---------------------------------------------------------
    
    def setCollisionModel(self, model):
        '''
        '''
        self._collision_model = model
        
    def getCollisionModel(self):
        '''
        '''
        return self._collision_model
        
    collision_model = property(fget = getCollisionModel, fset = setCollisionModel)
        
    # ---------------------------------------------------------
    
    def setPhysicsModel(self, model):
        '''
        '''
        self._physics_model = model
        
    def getPhysicsModel(self):
        '''
        '''
        return self._physics_model
        
    physics_model = property(fget = getPhysicsModel, fset = setPhysicsModel)
        
    # ---------------------------------------------------------
    
    def setBoost(self):
        '''
        Boosts the vehicle by indicated strength
        '''
        self.startBlowout()
        if self._hit_ground:
            direction = self._collision_model.getQuaternion().xform(Vec3(0,1,0))
            self._physics_model.addForce(direction*self._boost_strength*self.physics_model.getMass().getMagnitude())
        else:
            direction = self._collision_model.getQuaternion().xform(Vec3(0,1,0))
            self._physics_model.addForce(direction*self._boost_strength*0.2*self.physics_model.getMass().getMagnitude())
    # ---------------------------------------------------------
        
    def setDirection(self, dir):
        '''
        Boosts the vehicle by indicated strength
        '''
        rel_direction = self._collision_model.getQuaternion().xform(Vec3(dir[1],0,dir[0]))
        #rel_position = self._collision_model.getQuaternion().xform(Vec3(5,0,0))
        #force = Vec3(rel_direction[0]*self.direction[0]*self._control_strength*self.speed,rel_direction[1]*self.direction[1]*self._control_strength*self.speed,rel_direction[2]*self.direction[2]*self._control_strength*self.speed)
        self._physics_model.addTorque(-rel_direction*self._control_strength*self.physics_model.getMass().getMagnitude())
    
    def getDirection(self):
        return self._direction
        
    direction = property(fget = getDirection, fset = setDirection)        
        
    # ---------------------------------------------------------
    
    def getBoostDirection(self):
        return self._boost_direction
        
    boost_direction = property(fget = getBoostDirection)        
    
    # ---------------------------------------------------------
    
    def getSpeed(self):
        return self._speed
        
    speed = property(fget = getSpeed) 
        
    # ---------------------------------------------------------
    
    def setEnergy(self, energy):
        '''
        Boosts the vehicle by indicated strength
        '''
        self._energy = energy
    
    def getEnergy(self):
        return self._energy
        
    energy = property(fget = getEnergy, fset = setEnergy)        
        
    # ---------------------------------------------------------
    def setModelLoading(self, bool):
        '''
        '''
        self._model_loading = bool
    
    def getModelLoading(self):
        return self._model_loading
        
    model_loading = property(fget = getModelLoading, fset = setModelLoading)        
        
    # ---------------------------------------------------------
    
    def doStep(self):
        '''
        Needs to get executed every Ode-Step
        '''
        #refresh variables
        linear_velocity = self._physics_model.getLinearVel()
        direction = self._collision_model.getQuaternion().xform(Vec3(0,1,0))
        self._boost_direction[0],self._boost_direction[1],self._boost_direction[2] = self.physics_model.getLinearVel()[0],self.physics_model.getLinearVel()[1],self.physics_model.getLinearVel()[2]
        
        #This needs to be done, so we dont create a new object but only change the existing one. else the camera wont update
        self.direction[0], self.direction[1],self.direction[2] = direction[0],direction[1],direction[2]
        
        xy_direction = self.collision_model.getQuaternion().xform(Vec3(1,1,0)) 
        self._speed = Vec3(linear_velocity[0]*xy_direction[0],linear_velocity[1]*xy_direction[1],linear_velocity[2]*xy_direction[2]).length()
        
        #calculate delayed velocity changes
        linear_velocity.normalize()
        self._direction.normalize()
        self._physics_model.addForce(self._direction*(self._speed*self._grip_strength*self.physics_model.getMass().getMagnitude()))#+linear_velocity)
        self._physics_model.addForce(-linear_velocity*(self._speed*self._grip_strength*self.physics_model.getMass().getMagnitude()))#+linear_velocity)
        
        #calculate the grip
        self._physics_model.addTorque(self._physics_model.getAngularVel()*-self._track_grip*self.physics_model.getMass().getMagnitude())
        
        #refresh the positions of the collisionrays
        self._ray.doStep()
        
    
    # ---------------------------------------------------------
    
    def getRay(self):
        return self._ray
    
    ray = property(fget = getRay)    
    
    # ----------------------------------------------------------------- 
        
    def getHitGround(self):
        return self._hit_ground
        
    def setHitGround(self, value):
        if type(value) != bool:
            raise TypeError("Type should be %s not %s"% (bool,type(value)))
        self._hit_ground = value
    
    hit_ground= property(fget = getHitGround, fset = setHitGround)
    
    # ----------------------------------------------------------------- 
    
    def getControlStrength(self):
        return self._control_strength
        
    def setControlStrength(self, value):
        self._control_strength = value
    
    control_strength = property(fget = getControlStrength, fset = setControlStrength)
    
    # ----------------------------------------------------------------- 
    
    def getGripStrength(self):
        return self._grip_strength
        
    def setGripStrength(self, value):
        self._grip_strength = value
    
    grip_strength = property(fget = getGripStrength, fset = setGripStrength)
    
    # ----------------------------------------------------------------- 
    
    def getTrackGrip(self):
        return self._track_grip
        
    def setTrackGrip(self, value):
        self._track_grip = value
    
    track_grip = property(fget = getTrackGrip, fset = setTrackGrip)
    
    # ----------------------------------------------------------------- 
    
    def getMaxEnergy(self):
        return self._max_energy
        
    def setMaxEnergy(self, value):
        self._max_energy = value
    
    max_energy = property(fget = getMaxEnergy, fset = setMaxEnergy)
    
    # ----------------------------------------------------------------- 
    
    def getMaxArmor(self):
        return self._max_armor
        
    def setMaxArmor(self, value):
        self._max_armor = value
    
    max_armor = property(fget = getMaxArmor, fset = setMaxArmor)
    
    # ----------------------------------------------------------------- 
    
    def getWeight(self):
        return self._weight
        
    def setWeight(self, value):
        self._weight = value
    
    weight = property(fget = getWeight, fset = setWeight)
    
    # ----------------------------------------------------------------- 
    
    def getDescription(self):
        return self._description
        
    def setDescription(self, value):
        self._description = value
    
    description = property(fget = getDescription, fset = setDescription)
    
    # ----------------------------------------------------------------- 
        
    def getBrakeStrength(self):
        return self._brake_strength
        
    def setBrakeStrength(self, value):
        self._brake_strength = value
    
    brake_strength = property(fget = getBrakeStrength, fset = setBrakeStrength)
    
    # ----------------------------------------------------------------- 
            
    def getName(self):
        return self._name
        
    def setName(self, value):
        self._name = value
    
    name = property(fget = getName, fset = setName)
    
    # ----------------------------------------------------------------- 
    
    def cleanResources(self):
        '''
        Removes old nodes, gets called when a new vehcile loads
        '''
        for node in self._blowout:
            node.removeNode()
            
        if self._model != None:
            for node in self._model.getChildren():
                node.removeNode()
            self._model.removeNode()
            self._model = None
            self._physics_model.destroy()
            self._collision_model.destroy()
        
        self._notify.info("Vehicle-Object cleaned: %s" %(self))
    
    def __del__(self):
        '''
        Destroy unused nodes
        '''
        for node in self._blowout:
            node.removeNode()
            
        if self._model != None:
            for node in self._model.getChildren():
                node.removeNode()
            self._model.removeNode()
            self._model = None
            self._physics_model.destroy()
            self._collision_model.destroy()
        
        self._notify.info("Vehicle-Object deleted: %s" %(self))
    
if __name__ == "__main__":
    import main