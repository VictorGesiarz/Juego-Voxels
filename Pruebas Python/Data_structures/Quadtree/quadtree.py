
class Pixel:
    def __init__(self, x, y, s) -> None:
        self.x = x
        self.y = y
        self.s = s


class Rectangle:

    def __init__(self, x, y, s) -> None:
        self.x = x
        self.y = y
        self.s = s



class Quadtree:

    def __init__(self, boundry, pixel=None, q1=None, q2=None, q3=None, q4=None) -> None:
        
        self.boundry = boundry
        self.devided = False

        self.pixel = pixel
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    def subdivide(self):

        """
        FUNCTION TO SUBDIVIDE A DIVISION OF THE TREE IF IT IS NEEDED.
        """

        s = self.boundry.s / 2
        r1 = Rectangle(self.boundry.x, self.boundry.y, s)
        self.q1 = Quadtree(r1)
        r2 = Rectangle(self.boundry.x + s, self.boundry.y, s)
        self.q2 = Quadtree(r2)
        r3 = Rectangle(self.boundry.x, self.boundry.y + s, s)
        self.q3 = Quadtree(r3)
        r4 = Rectangle(self.boundry.x + s, self.boundry.y + s, s)
        self.q4 = Quadtree(r4)

    def insert(self, pixel):

        """
        FUNCTION TO INSERT A NEW PIXEL INTO THE QUADTREE
        """

        if (pixel.x >= self.boundry.x and
            pixel.y >= self.boundry.y and
            pixel.x < self.boundry.x + self.boundry.s and
            pixel.y < self.boundry.y + self.boundry.s):

            if pixel.s == self.boundry.s:
                self.pixel = pixel
            else:
                if not self.devided:
                    self.subdivide()
                    self.devided = True
                self.q1.insert(pixel)
                self.q2.insert(pixel)
                self.q3.insert(pixel)
                self.q4.insert(pixel)
            
    def find_pixels_in_square(self, boundary):

        """
        FUNCTION TO FIND ALL THE PIXELS INSIDE OF A SQUARED BOUNDARY.
        """

        self_right = self.boundry.x + self.boundry.s
        self_bottom = self.boundry.y + self.boundry.s
        boundary_right = boundary.x + boundary.s
        boundary_bottom = boundary.y + boundary.s

        if self.boundry.x < boundary_right and self_right > boundary.x and self.boundry.y < boundary_bottom and self_bottom > boundary.y:
            if self.devided:
                p1, c1 = self.q1.find_pixels_in_square(boundary)
                p2, c2 = self.q2.find_pixels_in_square(boundary)
                p3, c3 = self.q3.find_pixels_in_square(boundary)
                p4, c4 = self.q4.find_pixels_in_square(boundary)
                return p1 + p2 + p3 + p4, c1 + c2 + c3 + c4 + 1
            elif self.pixel is not None:
                return [self.pixel], 1
        return [], 1

    def get_boundaries(self):

        """
        DRAW FUNCTION. RETURNS THE BOUNDARIES OF THE DIFFERENT DIVISION AND THE PIXELS. 
        """

        q0 = self.boundry

        if self.devided:
            q1, p1 = self.q1.get_boundaries()
            q2, p2 = self.q2.get_boundaries()
            q3, p3 = self.q3.get_boundaries()
            q4, p4 = self.q4.get_boundaries()
        
            return [q0] + q1 + q2 + q3 + q4, p1 + p2 + p3 + p4
        
        if self.pixel is not None:
            return [q0], [self.pixel]
        
        return [q0], []