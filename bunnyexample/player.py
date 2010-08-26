# _*_ coding: UTF-8 _*_
###############################################################
##  Autor: Carsten Pfeffer    ##  Version 0.0                ##
###############################################################
##  Programm: BUNNY                                          ##
###############################################################
##  Datum:  23.08.2010                                       ##
###############################################################

from panda3d.core import *
from direct.actor.Actor import Actor                        # bewegliche Models
from direct.showbase.DirectObject import DirectObject       # Basisklasse für das Spiel

import math

STATE_STANDING = 0
STATE_MOVING = 1
STATE_JUMPING = 2
STATE_FALLING = 3

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

SOUND_JUMP = loader.loadSfx("data/sfx/jump.wav")
SOUND_BLASTERSHOT = loader.loadSfx("data/sfx/blastershot.wav")

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #


class Player(object):
    '''
    '''
    def __init__(self, model):
        '''
        '''
        self.speed = Vec3(0,0,0)
        self.actor = Actor(model)
        self.state = STATE_STANDING
        self.jump_time = 0.0
        self.jump_height = 60
        self.is_shooting = False
        self.shoot_time = 1

        # alle abgeschossenen Kugeln
        self.bullets = []

        # Animationszyklen festlegen
        anim_control=self.actor.getAnimControl("run")
        anim_control.setPlayRate(1.8)

        # Floater hinzufügen
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # Kamera hinzufügen
        base.camera.setPos(self.actor.getX(),self.actor.getY()+10,2)
        base.camera.setZ(self.actor.getZ()+3)

        self.initCollision()

    # ----------------------------------------------------------------- #

    def setPos(self, value):
        '''
        '''
        self.actor.setPos(value)

    # ----------------------------------------------------------------- #

    def setScale(self, value):
        '''
        '''
        self.actor.setScale(value)

    # ----------------------------------------------------------------- #

    def reparentTo(self, target):
        '''
        '''
        return self.actor.reparentTo(target)

    # ----------------------------------------------------------------- #

    def movePlayer(self, key_map):
        '''
        '''
        self.speed.setX(0)
        self.speed.setY(0)
        self.speed.setZ(0)


        # Kamera sieht den Spieler an
        base.camera.lookAt(self.actor)

        # Kamera bei Bedarf drehen
        if key_map["joy_a"] != 0:
            base.camera.setX(base.camera, key_map["joy_a"]*-20 * globalClock.getDt())
        if key_map["cam_left"]:    # Kamera nach links drehen, wenn die Taste gedrückt wurde
            base.camera.setX(base.camera, +20 * globalClock.getDt())
        if key_map["cam_right"]:   # Kamera nach links drehen, wenn die Taste gedrückt wurde
            base.camera.setX(base.camera, -20 * globalClock.getDt())



        joy_x = key_map["joy_x"]
        joy_y = key_map["joy_y"]

        # If a move-key is pressed, the joystick / gamepad values will be ignored

        if key_map["arrow_left"]:
            joy_x = -1
        elif key_map["arrow_right"]:
            joy_x = 1
        if key_map["arrow_up"]:
            joy_y = -1
        elif key_map["arrow_down"]:
            joy_y = 1


        # determine the angle the player wants to go
        alpha = 0

        if joy_x != 0 or joy_y != 0:
            if joy_x == 0:
                joy_x = .01
            if joy_y == 0:
                joy_y = .01

            if joy_x < 0 and joy_y > 0:
                alpha = 180-math.degrees(math.atan(-joy_x/joy_y))

            elif joy_x < 0 and joy_y < 0:
                alpha = 90-math.degrees(math.atan(-joy_y/-joy_x))

            elif joy_x > 0 and joy_y < 0:
                alpha = -math.degrees(math.atan(joy_x/-joy_y))

            elif joy_x > 0 and joy_y > 0:
                alpha = -90-math.degrees(math.atan(joy_y/joy_x))

            # determine the speed the player walks
            self.speed.setY(-25 * (abs(joy_x)+abs(joy_y)) * globalClock.getDt())

            # the players angle is computed so that he would walk towards the camera if the angle was 0
            self.actor.lookAt(base.camera)
            self.actor.setR(0)
            self.actor.setP(0)
            self.actor.setH(self.actor.getH()+alpha)




        # let the player jump
        if (key_map["jump"] or key_map["joy_jump"]) and self.state != STATE_FALLING and self.state != STATE_JUMPING:
            self.jump_time = self.jump_height
            self.state = STATE_JUMPING
            SOUND_JUMP.play()

        if (key_map["shoot"] or key_map["joy_shoot"]) and not self.is_shooting:
            self.shoot_time = 1
            self.is_shooting = True
            SOUND_BLASTERSHOT.play()

            bullet = loader.loadModel("data/models/blasterbullet")
            bullet.reparentTo(render)
            pos = self.actor.getPos()
            bullet.setPos(pos)
            bullet.setZ(bullet,1)
            bullet.setH(self.actor.getH())
            bullet.setR(0)
            bullet.setP(0)
            self.bullets.append(bullet)

        if self.is_shooting:
            self.shoot_time -= 2*globalClock.getDt()
            if (key_map["shoot"] == False and key_map["joy_shoot"] == False) or self.shoot_time <= 0:
                self.is_shooting = False

        if self.state == STATE_JUMPING:
            if self.jump_time <= 0:
                self.state = STATE_FALLING
            else:
                self.speed.setZ(globalClock.getDt() * self.jump_time)
                self.jump_time -= self.jump_height*3 * globalClock.getDt()


        if self.state != STATE_JUMPING:
            if self.speed.getY() != 0:
                self.state = STATE_MOVING
            else:
                self.state = STATE_STANDING

        # Kollisionskerkennung
        self.doCollisionDetection()


        ## move bullets
        for bullet in self.bullets:
            bullet.setPos(bullet, Vec3(0, -40 * globalClock.getDt(),0))

        #######################################################
        ## ANIMATION

        if self.state == STATE_FALLING:
            if self.actor.getCurrentAnim() != "fall":
                self.actor.stop()
                self.actor.loop("fall")
        elif self.state == STATE_MOVING:
            if self.actor.getCurrentAnim() != "run":
                    self.actor.stop()
                    self.actor.loop("run")
        elif self.state == STATE_JUMPING:
            if self.actor.getCurrentAnim() != "jump":
                    self.actor.stop()
                    self.actor.loop("jump")
        else:
            if self.is_shooting and self.actor.getCurrentAnim() != "shoot":
                self.actor.stop()
                self.actor.loop("shoot")
            elif self.state == STATE_STANDING and self.actor.getCurrentAnim() != "stand" and not self.is_shooting:
                self.actor.stop()
                self.actor.loop("stand")


        #######################################################
        ## KAMERA

        # If the camera is too far from player, move it closer.
        # If the camera is too close to player, move it farther.

        camvec = self.actor.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if camdist > 12.0:
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-12))
            camdist = 12.0
        if camdist < 8.0:
            base.camera.setPos(base.camera.getPos() - camvec*(8-camdist))
            camdist = 8.0


        # The camera should look in player's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above player's head.

        self.floater.setPos(self.actor.getPos())
        self.floater.setZ(self.actor.getZ() + 2.0)
        base.camera.lookAt(self.floater)


    # ----------------------------------------------------------------- #


    def doCollisionDetection(self):
        '''
        '''
        last_pos = self.actor.getPos()
        stuck = False
        self.actor.setPos(self.actor, self.speed)
        self.speed = Vec3(0,0,0)

        self.c_trav.traverse(render)

        # Adjust player's Z coordinate.  If player's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = []
        for i in range(self.groundHandler.getNumEntries()):
            entry = self.groundHandler.getEntry(i)
            entries.append(entry)

        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))

        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            #self.actor.setZ(entries[0].getSurfacePoint(render).getZ())

            surface_z = entries[0].getSurfacePoint(render).getZ()
            actor_z = self.actor.getZ()

            dist = actor_z-surface_z

            if dist > 0.1 and self.state != STATE_JUMPING:

                if dist > .5:
                    self.speed.setZ(self.speed.getZ()-.65)
                    self.state = STATE_FALLING
                else:
                    self.actor.setZ(surface_z)

            elif dist < -0.1:
                if dist < -.8:
                    stuck = True
                else:
                    #self.speed.setZ(.18)
                    self.actor.setZ(surface_z)

        # kein Boden
        else:
            self.speed.setZ(self.speed.getZ()-.65)
            self.state = STATE_FALLING

        # Keep the camera at one foot above the terrain,
        # or two feet above player, whichever is greater.

        entries = []
        for i in range(self.camGroundHandler.getNumEntries()):
            entry = self.camGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+1.0)
        if (base.camera.getZ() < self.actor.getZ() + 2.0):
            base.camera.setZ(self.actor.getZ() + 2.0)

        self.actor.setPos(self.actor, self.speed)
        if stuck:
            self.actor.setPos(last_pos)

    # ----------------------------------------------------------------- #

    def initCollision(self):
        '''
        '''
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above player's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.

        self.c_trav = CollisionTraverser()

        self.groundRay = CollisionRay()
        self.groundRay.setOrigin(0,0,1000)
        self.groundRay.setDirection(0,0,-1)

        self.groundCol = CollisionNode('playerRay')
        self.groundCol.addSolid(self.groundRay)
        self.groundCol.setFromCollideMask(BitMask32.bit(0))
        self.groundCol.setIntoCollideMask(BitMask32.allOff())

        self.groundColNp = self.actor.attachNewNode(self.groundCol)
        self.groundHandler = CollisionHandlerQueue()
        self.c_trav.addCollider(self.groundColNp, self.groundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.c_trav.addCollider(self.camGroundColNp, self.camGroundHandler)


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
