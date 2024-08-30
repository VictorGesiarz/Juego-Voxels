
"""

Implementation of the ray tracing algorithm. Algorithm inspired from https://www.youtube.com/watch?v=NbSee-XM7WA. 

1. The first function is the ray tracing itself.
2. The other functions are made by me to do diferent functionalities, like ray tracing in all directions or only in a specific FOV. 

"""



import numpy as np
import numba as nb
from math import sqrt


# arg_types = List(uint16, reflected=True), List(float32, reflected=True), List(List(uint8), reflected=True), List(uint8, reflected=True), uint8
# ret_type = List(float32, reflected=True)
# sig = ret_type(*arg_types) 


@nb.njit(cache=True)
def ray_trace_direction(start_point: np.ndarray, direction: np.ndarray, distance: int, map: np.ndarray, grid_size: np.ndarray, pixel_size: int) -> np.ndarray:
    vRayStart = start_point
    vRayDir = direction
    
    # How much distance we travel through the ray by going 1 on X and how much if we go 1 on Y
    if vRayDir[0] != 0:
        step_x = sqrt(1 + (vRayDir[1] / vRayDir[0]) * (vRayDir[1] / vRayDir[0]))
    else:
        step_x = 1e9 
    if vRayDir[1] != 0:
        step_y = sqrt(1 + (vRayDir[0] / vRayDir[1]) * (vRayDir[0] / vRayDir[1]))
    else:
        step_y = 1e9  
    vRayUnitStepSize = (step_x, step_y)

    vMapCheck = np.trunc(vRayStart).astype(np.uint16)
    vRayLength1D = np.array([0, 0], dtype=np.float32)
    vStep = np.array([0, 0], dtype=np.int8)

    if vRayDir[0] < 0:
        vStep[0] = -1
        vRayLength1D[0] = (vRayStart[0] - float(vMapCheck[0])) * vRayUnitStepSize[0]
    else:
        vStep[0] = 1
        vRayLength1D[0] = (float(vMapCheck[0] + 1) - vRayStart[0]) * vRayUnitStepSize[0]

    if vRayDir[1] < 0:
        vStep[1] = -1
        vRayLength1D[1] = (vRayStart[1] - float(vMapCheck[1])) * vRayUnitStepSize[1]
    else:
        vStep[1] = 1
        vRayLength1D[1] = (float(vMapCheck[1] + 1) - vRayStart[1]) * vRayUnitStepSize[1]
    

    bTileFound = False
    fDistance = 0.0
    fMaxDistance = distance
    iters = 0
    visible_pixel = (-1, -1)
    while (not bTileFound) and (fDistance < fMaxDistance):
        iters += 1
        if (vRayLength1D[0] < vRayLength1D[1]):
            vMapCheck[0] += vStep[0]
            fDistance = vRayLength1D[0]
            
            # El siguiente IF sirve para que no se pase en ningun momento de la fMaxDistance y dar un efeccto ciruclar a la linterna,
            # ELIMINAR SI NO HACE FALTA Y SE QUIERE OPTIMIZAR UN POCO EL CÓDIGO
            if (vRayLength1D[0] + vRayUnitStepSize[0]) < fMaxDistance:
                vRayLength1D[0] += vRayUnitStepSize[0]
            else:
                vRayLength1D[0] = fMaxDistance

        else:
            vMapCheck[1] += vStep[1]
            fDistance = vRayLength1D[1]

            # El siguiente IF sirve para que no se pase en ningun momento de la fMaxDistance y dar un efeccto ciruclar a la linterna,
            # ELIMINAR SI NO HACE FALTA Y SE QUIERE OPTIMIZAR UN POCO EL CÓDIGO
            if (vRayLength1D[1] + vRayUnitStepSize[1]) < fMaxDistance:
                vRayLength1D[1] += vRayUnitStepSize[1]
            else:
                vRayLength1D[1] = fMaxDistance

        if vMapCheck[0] >= 0 and vMapCheck[0] < grid_size[0] and vMapCheck[1] >= 0 and vMapCheck[1] < grid_size[1]:
            if map[vMapCheck[1], vMapCheck[0]]:
                bTileFound = True
                visible_pixel = (vMapCheck[0], vMapCheck[1])
                break
        else: break


    return (vRayStart + vRayDir * fDistance) * pixel_size, visible_pixel



@nb.njit(cache=True)
def calculate_direction(start_point, end_point, pixel_size):
    vRayStart = start_point / pixel_size
    mousePos = end_point / pixel_size
    vector = mousePos - vRayStart
    norm = np.sqrt(np.sum(vector**2))
    vRayDir = vector / norm
    return vRayStart, vRayDir



@nb.njit(cache=True)
def ray_trace_start_end(start_point: np.ndarray, end_point: np.ndarray, distance: int, map_: np.ndarray, grid_size: np.ndarray, pixel_size: int) -> np.ndarray:
    vRayStart, vRayDir = calculate_direction(start_point, end_point, pixel_size)
    return ray_trace_direction(vRayStart, vRayDir, distance, map_, grid_size, pixel_size)



@nb.njit(cache=True)
def ray_trace_all_directions(point: np.ndarray, distance: int, num_rays: int, map_: np.ndarray, grid_size: np.ndarray, pixel_size: int):
    rays = np.empty((num_rays, point.shape[0]), dtype=np.float32)
    draw_map = set()

    vRayStart = point / pixel_size
    for i in range(num_rays):
        angle = i * (2 * np.pi / num_rays) 
        vRayDir = np.array([np.cos(angle), np.sin(angle)], dtype=np.float32)
        ray, vMapCheck = ray_trace_direction(vRayStart, vRayDir, distance, map_, grid_size, pixel_size)
        rays[i, :] = ray

        if vMapCheck != (-1, -1):
            draw_map.add(vMapCheck)
    return rays, draw_map



@nb.njit(cache=True)
def ray_trace_field_of_view(player_position: np.ndarray, mouse_position: np.ndarray, fov: float, distance: int, num_rays: int, map_: np.ndarray, grid_size: np.ndarray, pixel_size: int):
    vRayStart, vRayCenter = calculate_direction(player_position, mouse_position, pixel_size)
    rays = np.empty((num_rays, player_position.shape[0]), dtype=np.float32)
    draw_map = set()

    vRayCenter = np.arctan2(vRayCenter[1], vRayCenter[0])
    angle_step = fov / (num_rays - 1) 
    for i in range(num_rays):
        angle_offset = angle_step * (i - (num_rays - 1) / 2)
        angle = vRayCenter + angle_offset
        vRayDir = np.array([np.cos(angle), np.sin(angle)], dtype=np.float64)
        ray, vMapCheck = ray_trace_direction(vRayStart, vRayDir, distance, map_, grid_size, pixel_size)
        rays[i, :] = ray

        if vMapCheck != (-1, -1):
            draw_map.add(vMapCheck)
    return rays, draw_map
