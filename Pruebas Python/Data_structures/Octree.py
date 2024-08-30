
from typing import Tuple, Literal, Union, List


class Voxel:

    def __init__(self, x: int, y: int, z: int, size: int = 1, 
                 color: Tuple[Literal[0, 255], Literal[0, 255], Literal[0, 255]] = (0, 0, 0)):
        
        self.x = x
        self.y = y
        self.z = z
        self.size = size

        self.color = color



class Boundary:
    pass

class Boundary:

    def __init__(self, x: int, y: int, z: int, size: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.size = size

    def __contains__(self, item: Union[Voxel, Boundary]):
        if isinstance(item, Voxel):
            return (
                self.x <= item.x < self.x + self.size and
                self.y <= item.y < self.y + self.size and
                self.z <= item.z < self.z + self.size
            )
        elif isinstance(item, Boundary):
            return not (
                item.x >= self.x + self.size or
                item.x + item.size <= self.x or
                item.y >= self.y + self.size or
                item.y + item.size <= self.y or
                item.z >= self.z + self.size or
                item.z + item.size <= self.z
            )


class Octree:
    
    def __init__(self, boundary: Boundary, v: Union[None, Voxel, List[Boundary]] = None) -> None:
        self.boundary = boundary
        self.divided = False
        
        self.pixel = False
        self.v = v


    def subdivide(self) -> None:
        self.divided = True
        s = self.boundary.size
        s_ = int(s / 2)
        
        x, y, z = self.boundary.x, self.boundary.y, self.boundary.z

        v = []
        for i in range(0, s, s_):
            for j in range(0, s, s_):
                for k in range(0, s, s_):
                    r = Boundary(x + i, y + j, z + k, s_)
                    v.append(Octree(r))
        self.v = v


    def insert(self, voxel: Voxel) -> None:
        if voxel in self.boundary:
            if voxel.size == self.boundary.size:
                self.v = voxel
            else:
                if not self.divided:
                    self.subdivide()
                
                for i in self.v:
                    i.insert(voxel)


    def find_near_voxels(self, boundary: Boundary) -> list[Voxel]:
        if boundary in self.boundary:
            if self.divided:
                voxels, count = [], 0

                for i in self.v:
                    voxel, c = i.find_near_voxels(boundary)
                    voxels += voxel
                    count += c
                return voxels, count

            elif isinstance(self.v, Voxel):
                return [self.v], 1
            
        return [], 1


    def get_boundaries(self) -> (list[Union[Boundary, Voxel]]):
        if isinstance(self.v, Voxel):
            return self.v

        boundaries = [self.boundary]
        if self.divided:
            for i in self.v:
                boundaries += i.get_boundaries()
        return boundaries


def create_octree(size, num):
    boundary = Boundary(0, 0, 0, size)
    voxels = [Voxel(i, j, 0, 1, (255, 255, 255)) for i in range(num) for j in range(num)]
    O = Octree(boundary)
    for voxel in voxels:
        O.insert(voxel)
    return O