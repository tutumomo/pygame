import unittest
import pygame
import pygame.mask
from pygame.locals import *

import random

def random_mask(size = (100,100)):
    """random_mask(size=(100,100)): return Mask
    Create a mask of the given size, with roughly half the bits set at random."""
    m = pygame.Mask(size)
    for i in range(size[0] * size[1] // 2):
        x, y = random.randint(0,size[0] - 1), random.randint(0, size[1] - 1)
        m.set_at((x,y))
    return m

def maskFromSurface(surface, threshold = 127):
    mask = pygame.Mask(surface.get_size())
    key = surface.get_colorkey()
    if key:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x+0.1,y+0.1)) != key:
                    mask.set_at((x,y),1)
    else:
        for y in range(surface.get_height()):
            for x in range (surface.get_width()):
                if surface.get_at((x,y))[3] > threshold:
                    mask.set_at((x,y),1)
    return mask


class MaskTypeTest( unittest.TestCase ):
    def assertMaskEquals(self, m1, m2):
        self.assertEqual(m1.get_size(), m2.get_size())

        for i in range(m1.get_size()[0]):
            for j in range(m1.get_size()[1]):
                self.assertEqual(m1.get_at((i,j)), m2.get_at((i,j)))

    def test_mask(self):
        """Ensure masks are created correctly without fill parameter."""
        expected_count = 0
        expected_size = (11, 23)
        mask1 = pygame.mask.Mask(expected_size)
        mask2 = pygame.mask.Mask(size=expected_size)

        self.assertEqual(mask1.count(), expected_count)
        self.assertEqual(mask1.get_size(), expected_size)

        self.assertEqual(mask2.count(), expected_count)
        self.assertEqual(mask2.get_size(), expected_size)

    def test_mask__fill_kwarg(self):
        """Ensure masks are created correctly using the fill keyword."""
        width, height = 37, 47
        expected_size = (width, height)
        fill_counts = {True : width * height, False : 0 }

        for fill, expected_count in fill_counts.items():
            mask = pygame.mask.Mask(expected_size, fill=fill)

            self.assertEqual(mask.count(), expected_count,
                             'fill={}'.format(fill))
            self.assertEqual(mask.get_size(), expected_size,
                             'fill={}'.format(fill))

    def test_mask__fill_arg(self):
        """Ensure masks are created correctly using a fill arg."""
        width, height = 59, 71
        expected_size = (width, height)
        fill_counts = {True : width * height, False : 0 }

        for fill, expected_count in fill_counts.items():
            mask = pygame.mask.Mask(expected_size, fill)

            self.assertEqual(mask.count(), expected_count,
                             'fill={}'.format(fill))
            self.assertEqual(mask.get_size(), expected_size,
                             'fill={}'.format(fill))

    def test_mask__size_kwarg(self):
        """Ensure masks are created correctly using the size keyword."""
        width, height = 73, 83
        expected_size = (width, height)
        fill_counts = {True : width * height, False : 0 }

        for fill, expected_count in fill_counts.items():
            mask1 = pygame.mask.Mask(fill=fill, size=expected_size)
            mask2 = pygame.mask.Mask(size=expected_size, fill=fill)

            self.assertEqual(mask1.count(), expected_count,
                             'fill={}'.format(fill))
            self.assertEqual(mask1.get_size(), expected_size,
                             'fill={}'.format(fill))

            self.assertEqual(mask2.count(), expected_count,
                             'fill={}'.format(fill))
            self.assertEqual(mask2.get_size(), expected_size,
                             'fill={}'.format(fill))

    def test_get_size(self):
        """Ensure a mask's size is correctly retrieved."""
        expected_size = (93, 101)
        mask = pygame.mask.Mask(expected_size)

        self.assertEqual(mask.get_size(), expected_size)

    def test_get_at(self):
        """Ensure individual mask bits are correctly retrieved."""
        width, height = 5, 7
        mask0 = pygame.mask.Mask((width, height))
        mask1 = pygame.mask.Mask((width, height), fill=True)
        mask0_expected_bit = 0
        mask1_expected_bit = 1
        pos = (width - 1, height - 1)

        # Check twice to make sure bits aren't toggled.
        self.assertEqual(mask0.get_at(pos), mask0_expected_bit)
        self.assertEqual(mask0.get_at(pos), mask0_expected_bit)
        self.assertEqual(mask1.get_at(pos), mask1_expected_bit)
        self.assertEqual(mask1.get_at(pos), mask1_expected_bit)

    def test_get_at__out_of_bounds(self):
        """Ensure get_at() checks bounds."""
        width, height = 11, 3
        mask = pygame.mask.Mask((width, height))

        with self.assertRaises(IndexError):
            mask.get_at((width, 0))

        with self.assertRaises(IndexError):
            mask.get_at((0, height))

        with self.assertRaises(IndexError):
            mask.get_at((-1, 0))

        with self.assertRaises(IndexError):
            mask.get_at((0, -1))

    def test_set_at(self):
        """Ensure individual mask bits are set to 1."""
        width, height = 13, 17
        mask0 = pygame.mask.Mask((width, height))
        mask1 = pygame.mask.Mask((width, height), fill=True)
        mask0_expected_count = 1
        mask1_expected_count = mask1.count()
        expected_bit = 1
        pos = (width - 1, height - 1)

        mask0.set_at(pos, expected_bit)  # set 0 to 1
        mask1.set_at(pos, expected_bit)  # set 1 to 1

        self.assertEqual(mask0.get_at(pos), expected_bit)
        self.assertEqual(mask0.count(), mask0_expected_count)
        self.assertEqual(mask1.get_at(pos), expected_bit)
        self.assertEqual(mask1.count(), mask1_expected_count)

    def test_set_at__to_0(self):
        """Ensure individual mask bits are set to 0."""
        width, height = 11, 7
        mask0 = pygame.mask.Mask((width, height))
        mask1 = pygame.mask.Mask((width, height), fill=True)
        mask0_expected_count = 0
        mask1_expected_count = mask1.count() - 1
        expected_bit = 0
        pos = (width - 1, height - 1)

        mask0.set_at(pos, expected_bit)  # set 0 to 0
        mask1.set_at(pos, expected_bit)  # set 1 to 0

        self.assertEqual(mask0.get_at(pos), expected_bit)
        self.assertEqual(mask0.count(), mask0_expected_count)
        self.assertEqual(mask1.get_at(pos), expected_bit)
        self.assertEqual(mask1.count(), mask1_expected_count)

    def test_set_at__default_value(self):
        """Ensure individual mask bits are set using the default value."""
        width, height = 3, 21
        mask0 = pygame.mask.Mask((width, height))
        mask1 = pygame.mask.Mask((width, height), fill=True)
        mask0_expected_count = 1
        mask1_expected_count = mask1.count()
        expected_bit = 1
        pos = (width - 1, height - 1)

        mask0.set_at(pos)  # set 0 to 1
        mask1.set_at(pos)  # set 1 to 1

        self.assertEqual(mask0.get_at(pos), expected_bit)
        self.assertEqual(mask0.count(), mask0_expected_count)
        self.assertEqual(mask1.get_at(pos), expected_bit)
        self.assertEqual(mask1.count(), mask1_expected_count)

    def test_set_at__out_of_bounds(self):
        """Ensure set_at() checks bounds."""
        width, height = 11, 3
        mask = pygame.mask.Mask((width, height))

        with self.assertRaises(IndexError):
            mask.set_at((width, 0))

        with self.assertRaises(IndexError):
            mask.set_at((0, height))

        with self.assertRaises(IndexError):
            mask.set_at((-1, 0))

        with self.assertRaises(IndexError):
            mask.set_at((0, -1))

    def todo_test_overlap(self):

        # __doc__ (as of 2008-08-02) for pygame.mask.Mask.overlap:

          # Mask.overlap(othermask, offset) -> x,y
          # Returns the point of intersection if the masks overlap with the
          # given offset - or None if it does not overlap.

          # The overlap tests uses the following offsets (which may be negative):
          #    +----+----------..
          #    |A   | yoffset
          #    |  +-+----------..
          #    +--|B
          #    |xoffset
          #    |  |
          #    :  :

        self.fail()

    def todo_test_overlap_area(self):

        # __doc__ (as of 2008-08-02) for pygame.mask.Mask.overlap_area:

          # Mask.overlap_area(othermask, offset) -> numpixels
          # Returns the number of overlapping 'pixels'.
          #
          # You can see how many pixels overlap with the other mask given.  This
          # can be used to see in which direction things collide, or to see how
          # much the two masks collide.

        self.fail()

    def test_overlap_mask(self):
        """Ensure overlap_mask's mask has correct bits set."""
        mask = pygame.mask.Mask((50, 50), fill=True)
        mask2 = pygame.mask.Mask((300, 10), fill=True)
        mask3 = mask.overlap_mask(mask2, (-1, 0))

        for i in range(50):
            for j in range(10):
                self.assertEqual(mask3.get_at((i, j)), 1,
                                 '({}, {})'.format(i, j))

        for i in range(50):
            for j in range(11, 50):
                self.assertEqual(mask3.get_at((i, j)), 0,
                                 '({}, {})'.format(i, j))

    def test_overlap_mask__count(self):
        """Ensure overlap_mask's mask has the correct count."""
        mask1 = pygame.mask.Mask((65, 3), fill=True)
        mask2 = pygame.mask.Mask((66, 4), fill=True)

        # Using rects to help determine the expected count of the overlapping
        # mask.
        rect1 = pygame.Rect((0, 0), mask1.get_size())
        rect2 = pygame.Rect((0, 0), mask2.get_size())
        offsets = ((0, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1))

        for offset in offsets:
            rect2.topleft = offset
            overlap_rect = rect1.clip(rect2)
            expected_count = overlap_rect.w * overlap_rect.h

            overlap_mask = mask1.overlap_mask(mask2, offset)

            self.assertEqual(overlap_mask.count(), expected_count,
                             'offset={}'.format(offset))

    def test_mask_access( self ):
        """ do the set_at, and get_at parts work correctly?
        """
        m = pygame.Mask((10,10))
        m.set_at((0,0), 1)
        self.assertEqual(m.get_at((0,0)), 1)
        m.set_at((9,0), 1)
        self.assertEqual(m.get_at((9,0)), 1)

        #s = pygame.Surface((10,10))
        #s.set_at((1,0), (0, 0, 1, 255))
        #self.assertEqual(s.get_at((1,0)), (0, 0, 1, 255))
        #s.set_at((-1,0), (0, 0, 1, 255))

        # out of bounds, should get IndexError
        self.assertRaises(IndexError, lambda : m.get_at((-1,0)) )
        self.assertRaises(IndexError, lambda : m.set_at((-1,0), 1) )
        self.assertRaises(IndexError, lambda : m.set_at((10,0), 1) )
        self.assertRaises(IndexError, lambda : m.set_at((0,10), 1) )

    def test_fill(self):
        """Ensure a mask can be filled."""
        width, height = 11, 23
        expected_count = width * height
        mask = pygame.mask.Mask((width, height))

        mask.fill()

        self.assertEqual(mask.count(), expected_count)

    def test_clear(self):
        """Ensure a mask can be cleared."""
        expected_count = 0
        mask = pygame.mask.Mask((13, 27), fill=True)

        mask.clear()

        self.assertEqual(mask.count(), expected_count)

    def todo_test_invert(self):
        """Ensure a mask can be inverted."""
        self.fail()

    def todo_test_scale(self):
        """Ensure a mask can be scaled."""
        self.fail()

    def todo_test_draw(self):
        """Ensure a mask can be drawn onto another mask."""
        self.fail()

    def test_erase(self):
        """Ensure erase() clears bits."""
        mask1 = pygame.mask.Mask((65, 3))
        mask2 = pygame.mask.Mask((66, 4), fill=True)

        # Using rects to help determine the overlapping area.
        rect1 = pygame.Rect((0, 0), mask1.get_size())
        rect2 = pygame.Rect((0, 0), mask2.get_size())
        rect1_area = rect1.w * rect1.h
        offsets = ((0, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1))

        for offset in offsets:
            rect2.topleft = offset
            overlap_rect = rect1.clip(rect2)
            expected_count = rect1_area - (overlap_rect.w * overlap_rect.h)
            mask1.fill()  # Ensure it's filled for testing each offset.

            mask1.erase(mask2, offset)

            self.assertEqual(mask1.count(), expected_count,
                             'offset={}'.format(offset))

    def test_count(self):
        """Ensure a mask's set bits are correctly counted."""
        side = 67
        mask = pygame.mask.Mask((side, side))
        expected_count = 0

        for i in range(side):
            expected_count += 1
            mask.set_at((i, i))

        self.assertEqual(mask.count(), expected_count)

    def test_count__full_mask(self):
        """Ensure a full mask's set bits are correctly counted."""
        width, height = 17, 97
        expected_count = width * height

        mask = pygame.mask.Mask((width, height), fill=True)

        self.assertEqual(mask.count(), expected_count)

    def test_count__empty_mask(self):
        """Ensure an empty mask's set bits are correctly counted."""
        expected_count = 0

        mask = pygame.mask.Mask((13, 27))

        self.assertEqual(mask.count(), expected_count)

    def todo_test_centroid(self):
        """Ensure a mask's centroid is correctly calculated."""
        self.fail()

    def todo_test_centroid__empty_mask(self):
        """Ensure an empty mask's centroid is correctly calculated."""
        self.fail()

    def todo_test_angle(self):
        """Ensure a mask's orientation angle is correctly calculated."""
        self.fail()

    def todo_test_angle__empty_mask(self):
        """Ensure an empty mask's angle is correctly calculated."""
        self.fail()

    def test_drawing(self):
        """ Test fill, clear, invert, draw, erase
        """
        m = pygame.Mask((100,100))
        self.assertEqual(m.count(), 0)

        m.fill()
        self.assertEqual(m.count(), 10000)

        m2 = pygame.Mask((10, 10), fill=True)
        m.erase(m2, (50,50))
        self.assertEqual(m.count(), 9900)

        m.invert()
        self.assertEqual(m.count(), 100)

        m.draw(m2, (0,0))
        self.assertEqual(m.count(), 200)

        m.clear()
        self.assertEqual(m.count(), 0)

    def test_outline(self):
        """
        """

        m = pygame.Mask((20,20))
        self.assertEqual(m.outline(), [])

        m.set_at((10,10), 1)
        self.assertEqual(m.outline(), [(10,10)])

        m.set_at((10,12), 1)
        self.assertEqual(m.outline(10), [(10,10)])

        m.set_at((11,11), 1)
        self.assertEqual(m.outline(), [(10,10), (11,11), (10,12), (11,11), (10,10)])
        self.assertEqual(m.outline(2), [(10,10), (10,12), (10,10)])

        #TODO: Test more corner case outlines.

    def test_convolve__size(self):
        sizes = [(1,1), (31,31), (32,32), (100,100)]
        for s1 in sizes:
            m1 = pygame.Mask(s1)
            for s2 in sizes:
                m2 = pygame.Mask(s2)
                o = m1.convolve(m2)
                for i in (0,1):
                    self.assertEqual(o.get_size()[i],
                                     m1.get_size()[i] + m2.get_size()[i] - 1)

    def test_convolve__point_identities(self):
        """Convolving with a single point is the identity, while convolving a point with something flips it."""
        m = random_mask((100,100))
        k = pygame.Mask((1,1))
        k.set_at((0,0))

        self.assertMaskEquals(m,m.convolve(k))
        self.assertMaskEquals(m,k.convolve(k.convolve(m)))

    def test_convolve__with_output(self):
        """checks that convolution modifies only the correct portion of the output"""

        m = random_mask((10,10))
        k = pygame.Mask((2,2))
        k.set_at((0,0))

        o = pygame.Mask((50,50))
        test = pygame.Mask((50,50))

        m.convolve(k,o)
        test.draw(m,(1,1))
        self.assertMaskEquals(o, test)

        o.clear()
        test.clear()

        m.convolve(k,o, (10,10))
        test.draw(m,(11,11))
        self.assertMaskEquals(o, test)

    def test_convolve__out_of_range(self):
        full = pygame.Mask((2, 2), fill=True)

        self.assertEqual(full.convolve(full, None, ( 0,  3)).count(), 0)
        self.assertEqual(full.convolve(full, None, ( 0,  2)).count(), 3)
        self.assertEqual(full.convolve(full, None, (-2, -2)).count(), 1)
        self.assertEqual(full.convolve(full, None, (-3, -3)).count(), 0)

    def test_convolve(self):
        """Tests the definition of convolution"""
        m1 = random_mask((100,100))
        m2 = random_mask((100,100))
        conv = m1.convolve(m2)

        for i in range(conv.get_size()[0]):
            for j in range(conv.get_size()[1]):
                self.assertEqual(conv.get_at((i,j)) == 0,
                                 m1.overlap(m2, (i - 99, j - 99)) is None)

    def _draw_component_pattern_box(self, mask, size, pos, inverse=False):
        # Helper method to create/draw a 'box' pattern for testing.
        #
        # 111
        # 101  3x3 example pattern
        # 111
        pattern = pygame.mask.Mask((size, size), fill=True)
        pattern.set_at((size // 2, size // 2), 0)

        if inverse:
            mask.erase(pattern, pos)
            pattern.invert()
        else:
            mask.draw(pattern, pos)

        return pattern

    def _draw_component_pattern_x(self, mask, size, pos, inverse=False):
        # Helper method to create/draw an 'X' pattern for testing.
        #
        # 101
        # 010  3x3 example pattern
        # 101
        pattern = pygame.mask.Mask((size, size))

        ymax = size - 1
        for y in range(size):
            for x in range(size):
                if x == y or x == ymax - y:
                    pattern.set_at((x, y))

        if inverse:
            mask.erase(pattern, pos)
            pattern.invert()
        else:
            mask.draw(pattern, pos)

        return pattern

    def _draw_component_pattern_plus(self, mask, size, pos, inverse=False):
        # Helper method to create/draw a '+' pattern for testing.
        #
        # 010
        # 111  3x3 example pattern
        # 010
        pattern = pygame.mask.Mask((size, size))

        xmid = ymid = size // 2
        for y in range(size):
            for x in range(size):
                if x == xmid or y == ymid:
                    pattern.set_at((x, y))

        if inverse:
            mask.erase(pattern, pos)
            pattern.invert()
        else:
            mask.draw(pattern, pos)

        return pattern

    def test_connected_component(self):
        """Ensure a mask's connected component is correctly calculated."""
        width, height = 41, 27
        expected_size = (width, height)
        original_mask = pygame.mask.Mask(expected_size)
        patterns = []  # Patterns and offsets.

        # Draw some connected patterns on the original mask.
        offset = (0, 0)
        pattern = self._draw_component_pattern_x(original_mask, 3, offset)
        patterns.append((pattern, offset))

        size = 4
        offset = (width - size, 0)
        pattern = self._draw_component_pattern_plus(original_mask, size,
                                                    offset)
        patterns.append((pattern, offset))

        # Make this one the largest connected component.
        offset = (width // 2, height // 2)
        pattern = self._draw_component_pattern_box(original_mask, 7, offset)
        patterns.append((pattern, offset))

        expected_pattern, expected_offset = patterns[-1]
        expected_count = expected_pattern.count()
        original_count = sum(p.count() for p, _ in patterns)

        mask = original_mask.connected_component()

        self.assertEqual(mask.count(), expected_count)
        self.assertEqual(mask.get_size(), expected_size)
        self.assertEqual(mask.overlap_area(expected_pattern, expected_offset),
                         expected_count)

        # Ensure the original mask is unchanged.
        self.assertEqual(original_mask.count(), original_count)
        self.assertEqual(original_mask.get_size(), expected_size)

        for pattern, offset in patterns:
            self.assertEqual(original_mask.overlap_area(pattern, offset),
                             pattern.count())

    def test_connected_component__full_mask(self):
        """Ensure a mask's connected component is correctly calculated
        when the mask is full."""
        expected_size = (23, 31)
        original_mask = pygame.mask.Mask(expected_size, fill=True)
        expected_count = original_mask.count()

        mask = original_mask.connected_component()

        self.assertEqual(mask.count(), expected_count)
        self.assertEqual(mask.get_size(), expected_size)

        # Ensure the original mask is unchanged.
        self.assertEqual(original_mask.count(), expected_count)
        self.assertEqual(original_mask.get_size(), expected_size)

    def test_connected_component__empty_mask(self):
        """Ensure a mask's connected component is correctly calculated
        when the mask is empty."""
        expected_size = (37, 43)
        original_mask = pygame.mask.Mask(expected_size)
        original_count = original_mask.count()
        expected_count = 0

        mask = original_mask.connected_component()

        self.assertEqual(mask.count(), expected_count)
        self.assertEqual(mask.get_size(), expected_size)

        # Ensure the original mask is unchanged.
        self.assertEqual(original_mask.count(), original_count)
        self.assertEqual(original_mask.get_size(), expected_size)

    def test_connected_component__one_set_bit(self):
        """Ensure a mask's connected component is correctly calculated
        when the coordinate's bit is set with a connected component of 1 bit.
        """
        width, height = 71, 67
        expected_size = (width, height)
        original_mask = pygame.mask.Mask(expected_size, fill=True)
        xset, yset = width // 2, height // 2
        set_pos = (xset, yset)
        expected_offset = (xset - 1, yset - 1)

        # This isolates the bit at set_pos from all the other bits.
        expected_pattern = self._draw_component_pattern_box(original_mask, 3,
            expected_offset, inverse=True)
        expected_count = 1
        original_count = original_mask.count()

        mask = original_mask.connected_component(set_pos)

        self.assertEqual(mask.count(), expected_count)
        self.assertEqual(mask.get_size(), expected_size)
        self.assertEqual(mask.overlap_area(expected_pattern, expected_offset),
                         expected_count)

        # Ensure the original mask is unchanged.
        self.assertEqual(original_mask.count(), original_count)
        self.assertEqual(original_mask.get_size(), expected_size)
        self.assertEqual(original_mask.overlap_area(
            expected_pattern, expected_offset), expected_count)

    def test_connected_component__multi_set_bits(self):
        """Ensure a mask's connected component is correctly calculated
        when the coordinate's bit is set with a connected component of > 1 bit.
        """
        expected_size = (113, 67)
        original_mask = pygame.mask.Mask(expected_size)
        p_width, p_height = 11, 13
        set_pos = xset, yset = 11, 21
        expected_offset = (xset - 1, yset - 1)
        expected_pattern = pygame.mask.Mask((p_width, p_height), fill=True)

        # Make an unsymmetrical pattern. All the set bits need to be connected
        # in the resulting pattern for this to work properly.
        for y in range(3, p_height):
            for x in range(1, p_width):
                if x == y or x == y - 3 or x == p_width - 4:
                    expected_pattern.set_at((x, y), 0)

        expected_count = expected_pattern.count()
        original_mask.draw(expected_pattern, expected_offset)

        mask = original_mask.connected_component(set_pos)

        self.assertEqual(mask.count(), expected_count)
        self.assertEqual(mask.get_size(), expected_size)
        self.assertEqual(mask.overlap_area(expected_pattern, expected_offset),
                         expected_count)

        # Ensure the original mask is unchanged.
        self.assertEqual(original_mask.count(), expected_count)
        self.assertEqual(original_mask.get_size(), expected_size)
        self.assertEqual(original_mask.overlap_area(
            expected_pattern, expected_offset), expected_count)

    def test_connected_component__unset_bit(self):
        """Ensure a mask's connected component is correctly calculated
        when the coordinate's bit is unset.
        """
        width, height = 109, 101
        expected_size = (width, height)
        original_mask = pygame.mask.Mask(expected_size, fill=True)
        unset_pos = (width // 2, height // 2)
        original_mask.set_at(unset_pos, 0)
        original_count = original_mask.count()
        expected_count = 0

        mask = original_mask.connected_component(unset_pos)

        self.assertEqual(mask.count(), expected_count)
        self.assertEqual(mask.get_size(), expected_size)

        # Ensure the original mask is unchanged.
        self.assertEqual(original_mask.count(), original_count)
        self.assertEqual(original_mask.get_size(), expected_size)
        self.assertEqual(original_mask.get_at(unset_pos), 0)

    # The skip() can be removed when issue #841 is fixed/closed.
    @unittest.skip('can cause segmentation fault')
    def test_connected_component__out_of_bounds(self):
        """Ensure connected_component() checks bounds."""
        width, height = 19, 11
        original_size = (width, height)
        original_mask = pygame.mask.Mask(expected_size, fill=True)
        original_count = original_mask.count()

        for pos in ((0, -1), (-1, 0), (0, height + 1), (width + 1, 0)):
            with self.assertRaises(IndexError):
                mask = original_mask.connected_component(pos)

            # Ensure the original mask is unchanged.
            self.assertEqual(original_mask.count(), original_count)
            self.assertEqual(original_mask.get_size(), original_size)

    def test_connected_components(self):
        """
        """

        m = pygame.Mask((10,10))
        self.assertEqual(repr(m.connected_components()), "[]")

        comp = m.connected_component()
        self.assertEqual(m.count(), comp.count())

        m.set_at((0,0), 1)
        m.set_at((1,1), 1)
        comp = m.connected_component()
        comps = m.connected_components()
        comps1 = m.connected_components(1)
        comps2 = m.connected_components(2)
        comps3 = m.connected_components(3)
        self.assertEqual(comp.count(), comps[0].count())
        self.assertEqual(comps1[0].count(), 2)
        self.assertEqual(comps2[0].count(), 2)
        self.assertEqual(repr(comps3), "[]")

        m.set_at((9, 9), 1)
        comp = m.connected_component()
        comp1 = m.connected_component((1, 1))
        comp2 = m.connected_component((2, 2))
        comps = m.connected_components()
        comps1 = m.connected_components(1)
        comps2 = m.connected_components(2)
        comps3 = m.connected_components(3)
        self.assertEqual(comp.count(), 2)
        self.assertEqual(comp1.count(), 2)
        self.assertEqual(comp2.count(), 0)
        self.assertEqual(len(comps), 2)
        self.assertEqual(len(comps1), 2)
        self.assertEqual(len(comps2), 1)
        self.assertEqual(len(comps3), 0)

    def test_get_bounding_rects(self):
        """
        """

        m = pygame.Mask((10,10))
        m.set_at((0,0), 1)
        m.set_at((1,0), 1)

        m.set_at((0,1), 1)

        m.set_at((0,3), 1)
        m.set_at((3,3), 1)

        r = m.get_bounding_rects()

        self.assertEqual(
                repr(r),
                "[<rect(0, 0, 2, 2)>, <rect(0, 3, 1, 1)>, <rect(3, 3, 1, 1)>]")

        #1100
        #1111
        m = pygame.Mask((4,2))
        m.set_at((0,0), 1)
        m.set_at((1,0), 1)
        m.set_at((2,0), 0)
        m.set_at((3,0), 0)

        m.set_at((0,1), 1)
        m.set_at((1,1), 1)
        m.set_at((2,1), 1)
        m.set_at((3,1), 1)

        r = m.get_bounding_rects()
        self.assertEqual(repr(r), "[<rect(0, 0, 4, 2)>]")

        #00100
        #01110
        #00100
        m = pygame.Mask((5,3))
        m.set_at((0,0), 0)
        m.set_at((1,0), 0)
        m.set_at((2,0), 1)
        m.set_at((3,0), 0)
        m.set_at((4,0), 0)

        m.set_at((0,1), 0)
        m.set_at((1,1), 1)
        m.set_at((2,1), 1)
        m.set_at((3,1), 1)
        m.set_at((4,1), 0)

        m.set_at((0,2), 0)
        m.set_at((1,2), 0)
        m.set_at((2,2), 1)
        m.set_at((3,2), 0)
        m.set_at((4,2), 0)

        r = m.get_bounding_rects()
        self.assertEqual(repr(r), "[<rect(1, 0, 3, 3)>]")

        #00010
        #00100
        #01000
        m = pygame.Mask((5,3))
        m.set_at((0,0), 0)
        m.set_at((1,0), 0)
        m.set_at((2,0), 0)
        m.set_at((3,0), 1)
        m.set_at((4,0), 0)

        m.set_at((0,1), 0)
        m.set_at((1,1), 0)
        m.set_at((2,1), 1)
        m.set_at((3,1), 0)
        m.set_at((4,1), 0)

        m.set_at((0,2), 0)
        m.set_at((1,2), 1)
        m.set_at((2,2), 0)
        m.set_at((3,2), 0)
        m.set_at((4,2), 0)

        r = m.get_bounding_rects()
        self.assertEqual(repr(r), "[<rect(1, 0, 3, 3)>]")

        #00011
        #11111
        m = pygame.Mask((5,2))
        m.set_at((0,0), 0)
        m.set_at((1,0), 0)
        m.set_at((2,0), 0)
        m.set_at((3,0), 1)
        m.set_at((4,0), 1)

        m.set_at((0,1), 1)
        m.set_at((1,1), 1)
        m.set_at((2,1), 1)
        m.set_at((3,1), 1)
        m.set_at((3,1), 1)

        r = m.get_bounding_rects()
        #TODO: this should really make one bounding rect.
        #self.assertEqual(repr(r), "[<rect(0, 0, 5, 2)>]")

    def test_negative_size_mask(self):
        mask = pygame.Mask((100, 100))
        with self.assertRaises(ValueError):
            mask.scale((-1, -1))
        with self.assertRaises(ValueError):
            mask.scale((-1, 10))
        with self.assertRaises(ValueError):
            mask.scale((10, -1))

    def test_zero_mask(self):
        mask = pygame.mask.Mask((0, 0))
        self.assertEqual(mask.get_size(), (0, 0))

        mask = pygame.mask.Mask((100, 0))
        self.assertEqual(mask.get_size(), (100, 0))

        mask = pygame.mask.Mask((0, 100))
        self.assertEqual(mask.get_size(), (0, 100))

    def test_zero_mask_overlap(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask2 = pygame.mask.Mask((100, 100))
            self.assertEqual(mask.overlap(mask2, (0, 0)), None)
            self.assertEqual(mask2.overlap(mask, (0, 0)), None)

    def test_zero_mask_overlap_area(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask2 = pygame.mask.Mask((100, 100))
            self.assertEqual(mask.overlap_area(mask2, (0, 0)), 0)
            self.assertEqual(mask2.overlap_area(mask, (0, 0)), 0)

    def test_zero_mask_overlap_mask(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask2 = pygame.mask.Mask((100, 100))

            overlap_mask = mask.overlap_mask(mask2, (0, 0))
            overlap_mask2 = mask2.overlap_mask(mask, (0, 0))

            self.assertEqual(mask.get_size(), overlap_mask.get_size())
            self.assertEqual(mask2.get_size(), overlap_mask2.get_size())

    def test_zero_mask_fill(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size, fill=True)
            self.assertEqual(mask.count(), 0)

    def test_zero_mask_clear(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask.clear()
            self.assertEqual(mask.count(), 0)

    def test_zero_mask_flip(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask.invert()
            self.assertEqual(mask.count(), 0)

    def test_zero_mask_scale(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask2 = mask.scale((2, 3))
            self.assertEqual(mask2.get_size(), (2, 3))

    def test_zero_mask_draw(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask2 = pygame.mask.Mask((100, 100), fill=True)
            before = [mask2.get_at((x, y)) for x in range(100) for y in range(100)]
            mask.draw(mask2, (0, 0))
            after = [mask2.get_at((x, y)) for x in range(100) for y in range(100)]
            self.assertEqual(before, after)

    def test_zero_mask_erase(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            mask2 = pygame.mask.Mask((100, 100), fill=True)
            before = [mask2.get_at((x, y)) for x in range(100) for y in range(100)]
            mask.erase(mask2, (0, 0))
            after = [mask2.get_at((x, y)) for x in range(100) for y in range(100)]
            self.assertEqual(before, after)

    def test_zero_mask_count(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size, fill=True)
            self.assertEqual(mask.count(), 0)

    def test_zero_mask_centroid(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            self.assertEqual(mask.centroid(), (0, 0))

    def test_zero_mask_angle(self):
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            mask = pygame.mask.Mask(size)
            self.assertEqual(mask.angle(), 0.0)


class MaskModuleTest(unittest.TestCase):
    def test_from_surface(self):
        """  Does the mask.from_surface() work correctly?
        """

        mask_from_surface = pygame.mask.from_surface

        surf = pygame.Surface((70,70), SRCALPHA, 32)

        surf.fill((255,255,255,255))

        amask = pygame.mask.from_surface(surf)
        #amask = mask_from_surface(surf)

        self.assertEqual(amask.get_at((0,0)), 1)
        self.assertEqual(amask.get_at((66,1)), 1)
        self.assertEqual(amask.get_at((69,1)), 1)

        surf.set_at((0,0), (255,255,255,127))
        surf.set_at((1,0), (255,255,255,128))
        surf.set_at((2,0), (255,255,255,0))
        surf.set_at((3,0), (255,255,255,255))

        amask = mask_from_surface(surf)
        self.assertEqual(amask.get_at((0,0)), 0)
        self.assertEqual(amask.get_at((1,0)), 1)
        self.assertEqual(amask.get_at((2,0)), 0)
        self.assertEqual(amask.get_at((3,0)), 1)

        surf.fill((255,255,255,0))
        amask = mask_from_surface(surf)
        self.assertEqual(amask.get_at((0,0)), 0)

        #TODO: test a color key surface.

    def test_from_threshold(self):
        """ Does mask.from_threshold() work correctly?
        """

        a = [16, 24, 32]

        for i in a:
            surf = pygame.surface.Surface((70,70), 0, i)
            surf.fill((100,50,200),(20,20,20,20))
            mask = pygame.mask.from_threshold(surf,(100,50,200,255),(10,10,10,255))

            rects = mask.get_bounding_rects()

            self.assertEqual(mask.count(), 400)
            self.assertEqual(mask.get_bounding_rects(), [pygame.Rect((20,20,20,20))])

        for i in a:
            surf = pygame.surface.Surface((70,70), 0, i)
            surf2 = pygame.surface.Surface((70,70), 0, i)
            surf.fill((100,100,100))
            surf2.fill((150,150,150))
            surf2.fill((100,100,100), (40,40,10,10))
            mask = pygame.mask.from_threshold(surf, (0,0,0,0), (10,10,10,255), surf2)

            self.assertEqual(mask.count(), 100)
            self.assertEqual(mask.get_bounding_rects(), [pygame.Rect((40,40,10,10))])

    def test_zero_size_from_surface(self):
        zero_w_mask = pygame.mask.from_surface(pygame.Surface((0, 100)))
        self.assertEqual(zero_w_mask.get_size(), (0, 100))

        zero_h_mask = pygame.mask.from_surface(pygame.Surface((100, 0)))
        self.assertEqual(zero_h_mask.get_size(), (100, 0))

        zero_mask = pygame.mask.from_surface(pygame.Surface((0, 0)))
        self.assertEqual(zero_mask.get_size(), (0, 0))

    def test_zero_size_from_threshold(self):
        a = [16, 24, 32]
        sizes = ((100, 0), (0, 100), (0, 0))

        for size in sizes:
            for i in a:
                surf = pygame.surface.Surface(size, 0, i)
                surf.fill((100, 50, 200), (20, 20, 20, 20))
                mask = pygame.mask.from_threshold(surf, (100, 50, 200, 255), (10, 10, 10, 255))

                self.assertEqual(mask.count(), 0)

                rects = mask.get_bounding_rects()
                self.assertEqual(rects, [])

            for i in a:
                surf = pygame.surface.Surface(size, 0, i)
                surf2 = pygame.surface.Surface(size, 0, i)
                surf.fill((100, 100, 100))
                surf2.fill((150, 150, 150))
                surf2.fill((100, 100, 100), (40, 40, 10, 10))
                mask = pygame.mask.from_threshold(surf, (0, 0, 0, 0), (10, 10, 10, 255), surf2)

                self.assertEqual(mask.count(), 0)

                rects = mask.get_bounding_rects()
                self.assertEqual(rects, [])

if __name__ == '__main__':
    unittest.main()
