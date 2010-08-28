import pygame
from pygame.locals import *

class TextBox (pygame.sprite.DirtySprite):
    __fonts = {}

    splitChars = (' ', '-')

    _changed = False

    _text = ""
    _rect = None
    _fontName = ""
    _fontSize = 0
    _italic = False
    _bold = False
    _underline = False
    _antialias = True
    _color = None
    _myFont = None
    _image = None

    def __init__(self, text  = "", x = 0, y = 0, width = 50, height = 12, fontName = " ", fontSize = 10, italic = False, bold = False, underline = False, antialias = True, color = (255, 255, 255, 255), *args, **kwargs):
        super(TextBox, self). __init__(*args, **kwargs)
        self._rect = pygame.Rect(x, y, width, height)
        self._fontName = fontName
        self._fontSize = fontSize
        self._myFont = self._getFont(fontName, fontSize)
        self._text = text
        self._italic = italic
        self._bold = bold
        self._underline = underline
        self._antialias = antialias
        self._color = color
        self._update()

    def _getFont(self, fontName, size):
        choices = filter(lambda (x):x.find(fontName) != -1 , pygame.font.get_fonts())
        if len(choices) == 0:
            fontFile = pygame.font.get_default_font()
        else:
            fontFile = pygame.font.match_font(choices[0])
        key =(fontFile, size)
        if key not in TextBox.__fonts:
            TextBox.__fonts[key] = pygame.font.Font(fontFile, size)
        return TextBox.__fonts[key]        

    def _update(self):
        """Update the surface taht contains our text."""
        if self._image == None or self._image.get_size() != self._rect.size:
            self._image = pygame.Surface(self._rect.size, SRCALPHA)
        self._image.fill((0, 0, 0, 0))
        self._renderText()
        self.dirty = 1
        self._changed = False

    def _renderText(self):
        self._myFont.set_italic(self._italic)
        self._myFont.set_bold(self._bold)
        self._myFont.set_underline(self._underline)
        image = self._myFont.render(self._text, self._antialias, self._color)
        self._image.blit(image, (0, self._image.get_height() - image.get_height()))
            
    @property
    def rect(self):
        """Return the bounding box for this object.  Recalculate the object if
it has changed."""
        if self._changed:
            self._update()
        return self._rect
    #No setter property for rect.

    @property
    def image(self):
        """Return the rendered image for this object.  Recalculate the object
if it has changed."""
        if self._changed:
            self._update()
        return self._image
    #No setter property fot image.

    @property
    def x(self):
        """Return the left bound for this object."""
        return self.rect.left
  
    @x.setter
    def x(self, value):
        """Set the left bound for this object.  Mark this object as dirty."""
        self._rect.left = value
        if self.dirty == 0: self.dirty = 1

    @property
    def y(self):
        """Return the top bound for this object."""
        return self.rect.top

    @y.setter
    def y(self, value):
        """Set the left bound for this object.  Mark the object as dirty."""
        self._rect.top = value
        if self.dirty == 0: self.dirty = 1

    @property
    def width(self):
        """Return the left bound for this object."""
        return self.rect.width
  
    @width.setter
    def width(self, value):
        """Set the left bound for this object.  Mark this object as dirty."""
        self._rect.width = value
        self._changed = True

    @property
    def height(self):
        """Return the top bound for this object."""
        return self.rect.height

    @y.setter
    def height(self, value):
        """Set the left bound for this object.  Mark the object as dirty."""
        self._rect.height = value
        self._changed = True

    @property
    def bold(self):
        """Return the bold for this object."""
        return self._bold

    @bold.setter
    def bold(self, value):
        """Set the bold for this object."""
        self._bold = value
        self._changed = True

    @property
    def italic(self):
        """Return the italic for this object."""
        return self._italic

    @italic.setter
    def italic(self, value):
        """Set the italic for this object."""
        self._italic = value
        self._changed = True

    @property
    def underline(self):
        """Return the underline for this object."""
        return self._underline

    @underline.setter
    def underline(self, value):
        """Set the underline for this object."""
        self._underline = value
        self._changed = True

    @property
    def color(self):
        """Return the color for this object."""
        return self._color

    @color.setter
    def color(self, value):
        """Set the color for this object."""
        self._color = value
        self._changed = True

    @property
    def antialias(self):
        """Return the antialias for this object."""
        return self._antialias

    @antialias.setter
    def antialias(self, value):
        """Set the antialias for this object."""
        self._antialias = value
        self._changed = True

    @property
    def fontName(self):
        """Return the fontName for this object."""
        return self._fontName

    @fontName.setter
    def fontName(self, value):
        """Set the fontName for this object."""
        self._fontName = value
        self._changed = True

    @property
    def fontSize(self):
        """Return the fontSize for this object."""
        return self._fontSize

    @fontSize.setter
    def fontSize(self, value):
        """Set the fontSize for this object."""
        self._fontSize = value
        self._changed = True

    @property
    def text(self):
        """Return the text this object is displaying."""
        return self._text

    @text.setter
    def text(self, value):
        """Set the text this object displays."""
        self._text = value
        self._changed = True

def test():
    import test
    pygame.init()
    tb = TextBox(text = "Fishy")
    clock = pygame.time.Clock()
    group = pygame.sprite.LayeredDirty(tb, layer = 0, _use_update = True)
    def testlogic(event):
        if event == None:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                return True
            if event.key == K_BACKSPACE:
                if len(tb.text) > 0:
                    tb.text = tb.text[:-1]
                return
            if event.key >= 256:
                return
            tb.text += chr(event.key)
    def testrender(screen):
        clock.tick()
        time = clock.get_time()
        group.update(time)
        bgd = pygame.Surface((screen.get_width(), screen.get_height()))
        group.draw(screen, bgd = bgd)
    test.test(testlogic, testrender)

if __name__ == '__main__': test()
