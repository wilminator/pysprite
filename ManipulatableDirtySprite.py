import pygame
from pygame.locals import *
import math

class ManipulatableDirtySprite(pygame.sprite.DirtySprite):
    """This class is to highly overload the DirtySprite class to have lots of
neat little features, such as scaling and rotation."""
    _blank = None
    _image = None
    _opaqueScreen = None    
    _opaqueImage = None
    _scaledImage = None
    _rotatedImage = None
    _rect = None
    _x = 0
    _y = 0
    _xscale = 1.0
    _yscale = 1.0
    _xcenter = 0.0 #number of half-widths, 0.0 is center of sprite
    _ycenter = 0.0 #number of half-heights, 0.0 is center of sprite
    _rotation = 0.0
    _sine = 0.0
    _cosine = 1.0
    _opacity = 1.0
    #_ichanged indicates if the image has been changed.
    _ichanged = True
    #_ochanged indicates if the image opacity has been changed.
    _ochanged = False
    #_schanged indicates if the scale has changed. 
    _schanged = False
    #_rchanged indicates if the image has been rotated.
    _rchanged = False
    #_pchanged indicates if the rect has changed. 
    _pchanged = False

    def __init__(self, image = None, *args, **kwargs):
        if self._blank == None:
            self._blank = pygame.Surface((1, 1), SRCALPHA)
            ManipulatableDirtySprite._blank = self._blank
        super(ManipulatableDirtySprite, self).__init__(*args, **kwargs)
        self.image = image

    #Property wrapper the rect that this object has.
    @property
    def rect(self):
        """Return a copy of this object's rect."""
        self._update()
        return self._rect.copy()
    #No setter for rect.

    @property
    def top(self):
        """Return the true top of the sprite bounds."""
        return self._rect.top
    #No setter for top.

    @property
    def left(self):
        """Return the true left of the sprite bounds."""
        return self._rect.left
    #No setter for left.

    @property
    def bottom(self):
        """Return the true bottom of the sprite bounds."""
        return self.rect.bottom
    #No setter for bottom.

    @property
    def right(self):
        """Return the true right of the sprite bounds."""
        return self.rect.right
    #No setter for right.

    @property
    def topleft(self):
        """Return the true topleft of the sprite bounds."""
        return self.rect.topleft
    #No setter for topleft.

    @property
    def bottomleft(self):
        """Return the true bottomleft of the sprite bounds."""
        return self.rect.bottomleft
    #No setter for bottomleft.

    @property
    def topright(self):
        """Return the true topright of the sprite bounds."""
        return self.rect.topright
    #No setter for topright.

    @property
    def bottomright(self):
        """Return the true bottomright of the sprite bounds."""
        return self.rect.bottomright
    #No setter for bottomright.

    @property
    def midtop(self):
        """Return the true middle top of the sprite bounds."""
        return self.rect.midtop
    #No setter for midtop.

    @property
    def midleft(self):
        """Return the true middle left of the sprite bounds."""
        return self.rect.midleft
    #No setter for midleft.

    @property
    def midbottom(self):
        """Return the true middle bottom of the sprite bounds."""
        return self.rect.midbottom
    #No setter for midbottom.

    @property
    def midright(self):
        """Return the true middle right of the sprite bounds."""
        return self.rect.midright
    #No setter for midright.

    @property
    def center(self):
        """Return the true center of the sprite bounds."""
        return self.rect.center
    #No setter for center.

    @property
    def centerx(self):
        """Return the true center of x of the sprite bounds."""
        return self.rect.centerx
    #No setter for centerx.

    @property
    def centery(self):
        """Return the true center of y of the sprite bounds."""
        return self.rect.centery
    #No setter for centery.

    @property
    def size(self):
        """Return the true size of the sprite bounds."""
        return self.rect.size
    #No setter for size.

    @property
    def width(self):
        """Return the true width of the sprite bounds."""
        return self.rect.width
    #No setter for width.

    @property
    def height(self):
        """Return the true height of the sprite bounds."""
        return self.rect.height
    #No setter for height.

    @property
    def w(self):
        """Return the true width of the sprite bounds."""
        return self.rect.w
    #No setter for w.

    @property
    def h(self):
        """Return the true height of the sprite bounds."""
        return self.rect.h
    #No setter for h.


    #Now define properties for positioning and manipulating the sprite.
    @property
    def x(self):
        """Return the x position of the specified center of the sprite."""
        return self._x

    @x.setter
    def x(self, value):
        """Set the x position of the specified center of the sprite."""
        self._x = value
        self._pchanged = True

    @property
    def y(self):
        """Return the y position of the specified center of the sprite."""
        return self._y

    @y.setter
    def y(self, value):
        """Set the y position of the specified center of the sprite."""
        self._y = value
        self._pchanged = True

    @property
    def xscale(self):
        """Return the x scaling value of the sprite."""
        return self._xscale

    @xscale.setter
    def xscale(self, value):
        """Set the x scaling value of the sprite."""
        self._xscale = value
        self._schanged = True

    @property
    def yscale(self):
        """Return the y scaling value of the sprite."""
        return self._yscale

    @yscale.setter
    def yscale(self, value):
        """Set the y scaling value of the sprite."""
        self._yscale = value
        self._schanged = True

    @property
    def xcenter(self):
        """Return the x offset of the center of the sprite."""
        return self._xcenter

    @xcenter.setter
    def xcenter(self, value):
        """Set the x offset of the center of the sprite."""
        self._xcenter = value
        self._rchanged = True

    @property
    def ycenter(self):
        """Return the y offset of the center of the sprite."""
        return self._ycenter

    @ycenter.setter
    def ycenter(self, value):
        """Set the y offset of the center of the sprite."""
        self._ycenter = value
        self._rchanged = True

    @property
    def rotation(self):
        """Return the rotation about the center of the sprite in radians."""
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        """Set the rotation about the center of the sprite in degrees."""
        self._rotation = value
        rads = math.radians(value)
        self._sine = math.sin(rads)
        #Negative because y increases going down the screen.
        self._cosine = math.cos(rads) 
        self._rchanged = True

    @property
    def opacity(self):
        """Return the opacity of the sprite."""
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        """Set the opacity of the sprite."""
        self._opacity = value
        self._ochanged = True

    @property
    def image(self):
        """Return the cached image for this sprite.
If it needs to be updated first, it is."""
        self._update()
        return self._rotatedImage

    @image.setter
    def image(self, value):
        """Set the base image for this sprite."""
        self._image = value
        self._ichanged = True
    
    def _update(self):
        """This update function updates the image and it's rect as needed."""
        #Update image if needed.
        if self._ichanged == True:
            self._ichanged = False
            #Destroy the opaque screen.
            self._opaqueScreen = None
            #Case: No image.
            if self._image == None:
                self._rotatedImage = ManipulatbleDirtySprite._blank
                self._rect = pygame.Rect(self._x, self._y, 0, 0)
                self._ochanged = False
                self._schanged = False
                self._rchanged = False
                self._pchanged = False
                return
            #Otherwise, the opacity has changed!
            self._ochanged = True
        #Update opacity, if needed.
        if self._ochanged == True:
            self._ochanged = False
            #By default, the scaling has also changed.
            self._schanged = True
            image = self._image
            #Case: Image is transparent.
            if self._opacity <= 0.0:
                self._rotatedImage = ManipulatableDirtySprite._blank
                self._rect = pygame.Rect(self._x, self._y, self._image.get_width(), self._image.get_height())
                self._schanged = False
                self._rchanged = False
                self._pchanged = False
                return
            #Case: Image is not 100% opaque.
            if self._opacity < 1.0:
                if self._opaqueScreen == None:
                    self._opaqueScreen = pygame.Surface(self._image.get_size(), SRCALPHA)
                image = image.copy()
                self._opaqueScreen.fill((255, 255, 255, int(max((0, self._opacity * 255.0)))))
                image.blit(self._opaqueScreen, (0, 0), special_flags = BLEND_RGBA_MULT)
            self._opaqueImage = image
        #Update scaling if needed.
        if self._schanged == True:
            self._schanged = False
            #By default, the rotation has changed, too.
            self._rchanged = True
            image = self._opaqueImage            
            #Case: Scaled to 0.
            if self._xscale == 0.0 or self._yscale == 0.0:
                self._scaledImage = None
                self._rotatedImage = ManipulatableDirtySprite._blank
                self._rect = pygame.Rect(self._x, self._y, 0, 0)
                self._schanged = False
                self._rchanged = False
                self._pchanged = False
                return
            #Case: Image needs scaling.
            if math.fabs(self._xscale) != 1.0 or math.fabs(self._yscale) != 1.0:
                image = pygame.transform.smoothscale(image, (math.fabs(image.get_width() * self._xscale), math.fabs(image.get_height() * self._yscale)))
            if self._xscale < 0.0 or self._yscale < 0.0:
                image = pygame.transform.flip(image, self._xscale < 0.0, self._yscale < 0.0)
            self._scaledImage = image
        #Update rotation, if needed.
        if self._rchanged == True:
            self._rchanged = False
            #By default, the position has also changed.
            self._pchanged = True
            image = self._scaledImage
            #image.set_at((int((1 - self._xcenter) * image.get_width() * 0.5), int((1 - self._ycenter) * image.get_height() * 0.5)), (0, 255, 0, 255))
            #Case: Image needs rotation
            if self._rotation:
                image = pygame.transform.rotate(image, -self._rotation)
            self._rotatedImage = image
        #Update position, if needed.
        if self._pchanged == True:
            self._pchanged = False
            rect = self._rotatedImage.get_rect()
            ##We now have the width and height of our sprite.
            ##Now calculate the top and left of the rect that
            ##will describe where the sprite is to be rendered.
            #Get half width and half height.
            w, h = self._scaledImage.get_width() * .5, self._scaledImage.get_height() * .5
            #Find the rotated center of rotation
            ox = self._xcenter * w
            oy = self._ycenter * h
            rox = ox * self._cosine - oy * self._sine
            roy = oy * self._cosine + ox * self._sine
            #We now know the offset of rotation relative to the center of the
            #rotated image in pixels.
            #Move the rect to the base x and y location.
            rect.move_ip(self._x, self._y)
            #Get the half width and half height of the rotated image.
            rw, rh = rect.width * .5, rect.height * .5
            #Now move the rect out by the rotated center of rotation
            #and the half size of the image.
            self._rect = rect.move(int(rox - rw), int(roy - rh))
            if self.dirty == 0: self.dirty = 1
            
def test():
    import test
    pygame.init()
    image = pygame.image.load("qbird.png")
    sprite = ManipulatableDirtySprite(image = image)
    clock = pygame.time.Clock()
    group = pygame.sprite.LayeredDirty(sprite, layer = 0, _use_update = True)
    keysused = {}
    def testlogic(event):
        if event == None:            
            time = clock.get_time()
            if K_UP in keysused and keysused[K_UP]:
                sprite.y -= 1
            if K_DOWN in keysused and keysused[K_DOWN]:
                sprite.y += 1
            if K_LEFT in keysused and keysused[K_LEFT]:
                sprite.x -= 1
            if K_RIGHT in keysused and keysused[K_RIGHT]:
                sprite.x += 1
            if K_q in keysused and keysused[K_q]:
                sprite.rotation -= 1
            if K_e in keysused and keysused[K_e]:
                sprite.rotation += 1
            if K_w in keysused and keysused[K_w]:
                sprite.ycenter -= 0.015625
            if K_s in keysused and keysused[K_s]:
                sprite.ycenter += 0.015625
            if K_a in keysused and keysused[K_a]:
                sprite.xcenter -= 0.015625
            if K_d in keysused and keysused[K_d]:
                sprite.xcenter += 0.015625
            if K_r in keysused and keysused[K_r]:
                sprite.yscale += 0.015625
            if K_f in keysused and keysused[K_f]:
                sprite.yscale -= 0.015625
            if K_t in keysused and keysused[K_t]:
                sprite.xscale += 0.015625
            if K_g in keysused and keysused[K_g]:
                sprite.xscale -= 0.015625
            if K_y in keysused and keysused[K_y]:
                sprite.opacity += 0.015625
            if K_h in keysused and keysused[K_h]:
                sprite.opacity -= 0.015625
            return
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                return True
            keysused[event.key] = True
        if event.type == pygame.KEYUP:
            keysused[event.key] = False
    def testrender(screen):
        clock.tick()
        bgd = pygame.Surface((screen.get_width(), screen.get_height()))
        group.draw(screen, bgd = bgd)
    test.test(testlogic, testrender)

if __name__ == '__main__': test()
