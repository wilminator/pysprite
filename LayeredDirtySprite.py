"""This group has user modifyable height and width, acting as a window for the
sprites contained by this group.  Locations are always relative to the upper
left corner of the window, in pygame coordinate fashion.  The group window can
then be positioned and manipulated like a sprite itself.  This object inherits
from the ManipulatableDirtySprite, so it can be scaled, rotated, and faded."""

import pygame
from pygame.locals import *
import ManipulatableDirtySprite


class LayeredDirtySprite(ManipulatableDirtySprite.ManipulatableDirtySprite):
    """This class takes a LayeredDirty sprite group and turns it into a
positionable DirtySprite itself.  Instead of being able to specify a surface
or draw to this object, the sprites added to this group become the renderable.
All sprites are then drawn relative to the origin of this object.  This
object attempts to optimize the rendering of the children objects by creating a
image cache of the children."""
    _blankImage = None
    _dirty = 1
    _group = None

    def __init__(self, width = None, height = None, *args, **kwargs):
        """Standard init- call both parent classes."""
        super(LayeredDirtySprite, self).__init__(self, *args, **kwargs)
        self._group =  pygame.sprite.LayeredDirty(**kwargs)
        self._rect = pygame.Rect(0, 0, 1, 1)
        if width: self.width = width
        if height: self.height = height
        self._updateImage()

    def _updateImage(self):
        """Updates the bounds of the group's overall rectangle.  Additionally
resizes the cache surface, if needed."""
        if (self._blankImage == None
          or self._blankImage.get_width != self._rect.w 
          or self._blankImage.get_height != self._rect.h):
            self._blankImage = pygame.Surface((max((1, self._rect.w)), max((1, self._rect.h))), SRCALPHA)
            self._image = self._blankImage.copy()
            for o in self._group.sprites():
                if 'dirty' in dir(o) and o.dirty == 0: o.dirty = 1

    def update(self, *args, **kwargs):
        """update always invokes the LayeredDirty update function."""
        self._group.update(*args, **kwargs)

    def add(self, *args):
        """add calls the DirtySprite add for groups passed in and the
LayeredDirty add for sprites passed in."""
        for obj in args:
            if isinstance(obj, pygame.sprite.Sprite):
                self._group.add(obj)
                if self.dirty == 0: self.dirty = 1                
            else:
                super(LayeredDirtySprite, self).add(obj)
        
    def remove(self, *args):
        """remove calls the DirtySprite remove for groups passed in and the
LayeredDirty remove for sprites passed in."""
        for obj in args:
            if isinstance(obj, pygame.sprite.Sprite):
                self._group.remove(obj)
                if self.dirty == 0: self.dirty = 1                
            else:
                super(LayeredDirtySprite, self).remove(obj)

    @property
    def width(self):
        """Return the true width of the sprite bounds."""
        return self.rect.width

    @width.setter
    def width(self, value):
        """Sets the width of the group window."""
        self._rect.width = value
        self._updateImage()

    @property
    def height(self):
        """Return the true height of the sprite bounds."""
        return self.rect.height

    @height.setter
    def height(self, value):
        """Sets the width of the group window."""
        self._rect.height = value
        self._updateImage()

    @property
    def dirty(self):
        """This property is driven in part by its children sprites-
if they are dirty, then this group/sprite is dirty too."""
        if len([o for o in self._group.sprites() if 'dirty' not in dir(o) or o.dirty != 0]) > 0:
            if self._dirty == 0: self._dirty = 1
        return self._dirty
    
    @dirty.setter
    def dirty(self, value):
        """This directly sets the value of the dirty property."""
        self._dirty = value

    @property
    def image(self):
        """If this sprite is dirty, then it's image is regenerated."""
        if self.dirty != 0:
            #Find our background image, if any.
            group = self.groups()[0]
            bgd = group._bgd
            #Draw onto our internal image.
            self._group.draw(self._image, bgd = bgd)
        #Now process through our parent object functionality.
        return super(LayeredDirtySprite, self).image
    
    @image.setter
    def image(self, value):
        """This function is being disabled- there is no way to change the image
for this object directly."""
        pass
        
        
def test():
    import test
    import Bar
    pygame.init()
    bar = Bar.Bar(12340, 12345)
    bar2 = Bar.Bar(120, 135, color = (0, 0 ,255, 255))
    bar2.rect.top = 30
    
    clock = pygame.time.Clock()
    window = LayeredDirtySprite(width = 120, height = 100)
    window.add(bar)
    window.add(bar2)
    window.x = 100
    window.y = 200
    window.ycenter = -2.0
    group = pygame.sprite.LayeredDirty(window, layer = 0, _use_update = True)
    bgd = []
    def testlogic(event):
        if event == None:
            window.rotation += .01
            return
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                return True
            if event.key >= 256:
                return
            import random
            if event.mod & 4095 == 0:
                bar.actual -= min((random.randint(5, 500), bar.actual))
            else:
                bar.actual += min((random.randint(5, 500), bar._max - bar.actual))
    def testrender(screen):
        clock.tick()
        time = clock.get_time()
        group.update(time)
        if len(bgd) == 0:
            bgd.append(pygame.Surface((screen.get_width(), screen.get_height())))
            bgd[0].fill((0, 255, 0))
            group.clear(screen, bgd[0])
        group.draw(screen)
    test.test(testlogic, testrender)

if __name__ == '__main__': test()
