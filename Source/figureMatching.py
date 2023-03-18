import cv2
import pygame
import numpy as np
from Source.frame_to_mask import frame_to_mask

import matplotlib.pyplot as plt

body_mask = None
wall_mask = None

def padding(wall_mask, size, BB):
    h_max, w_max = size
    new_wall_mask = np.zeros(size)
    x, y, w, h = int(BB[0]), int(BB[1]), int(BB[2]), int(BB[3])
    wall_mask = cv2.resize(wall_mask, (w, h))
    if wall_mask.shape[0]> min(h_max-y, h) or wall_mask.shape[1]> min(w_max-x, w):
        wall_mask = wall_mask[0:min(h_max-y, h), 0:min(w_max-x, w), :]
    new_wall_mask[y:min(h_max, y + h), x:min(w_max, x + w)] = wall_mask[:, :, 1]
    return new_wall_mask

def PointsGrading(wall, image, ref, BB):#input:np array of wall mask and body mask, output: points given
    global body_mask
    global wall_mask
    body_mask = frame_to_mask(image, ref)

    wall_mask = pygame.surfarray.array3d(wall)
    wall_mask = wall_mask.swapaxes(0, 1)
    wall_mask = abs(255-wall_mask)
    wall_mask = padding(wall_mask, body_mask.shape, BB)
    _, wall_mask = cv2.threshold(wall_mask, 200, 1, cv2.THRESH_BINARY)

    # #FIXME - debug
    # plt.imshow(wall_mask + body_mask)
    # plt.show()

    wall_count = wall_mask.sum()

    body_count = body_mask.sum()
    inside = wall_mask*body_mask
    out_of_bound = body_mask-inside
    inside_count = inside.sum()
    out_of_bound_count = out_of_bound.sum()
    good_points = int((inside_count/wall_count)*100) # 100 if perfectly inside, 0 if only out of bound, close to zero if too small
    bad_points = int((out_of_bound_count/(wall_count+body_count))*100) #0 if no out of bound, 50 if body is only out of bound
    print(f"bad point: {bad_points}")
    if bad_points >= 12:
        return 0
    else:
        return good_points

def MarkMistake():
    '''
    :param wall_mask:
    :param body_mask:
    :return: contours
    '''
    global body_mask
    global wall_mask
    # body_mask = frame_to_mask(image,ref)
    out_of_bound = (body_mask - wall_mask * body_mask).astype(np.uint8)
    contours, _ = cv2.findContours(out_of_bound, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    areas = [cv2.minEnclosingCircle(c) for c in contours]
    areas = np.array([areas[i][1] for i in range(0, len(areas))])
    areas[areas > 100] = 0

    if len(areas) == 0:
        return []
    max_index = np.argmax(areas)
    cnt_1 = contours[max_index]
    (x, y), r = cv2.minEnclosingCircle(cnt_1)
    x = int(x)
    y = int(y)
    r = int(r)
    if len(areas) > 1:
        areas = np.delete(areas, max_index)
        max_index = np.argmax(areas)
        cnt_2 = contours[max_index]
        (x2, y2), r2 = cv2.minEnclosingCircle(cnt_2)
        x2 = int(x2)
        y2 = int(y2)
        r2 = int(r2)
        return [[(x, y), r], [(x2, y2), r2]]
    return [[(x, y), r]]

def is_hand(BB, image, ref):
    body = frame_to_mask(image, ref)
    box = np.zeros(np.shape(body))
    x, y, w, h = int(BB[0]), int(BB[1]), int(BB[2]), int(BB[3])
    box[y:y + h, x:x + w] = 1
    # FIXME - debug
    # plt.imshow(box + body)
    # plt.show()

    mask_out = (box * body).astype(np.uint8)
    ratio = mask_out.sum() / box.sum()
    if ratio >= 0.1:
        return True
    else:
        return False


def is_in_pos(BB, image, ref):
    body = frame_to_mask(image, ref)
    box = np.zeros(np.shape(body))
    x, y, w, h = int(BB[0]), int(BB[1]), int(BB[2]), int(BB[3])
    box[y:y + h, x:x + w] = 1
    mask_out = (box * body).astype(np.uint8)
    ratio = mask_out.sum()/box.sum()
    if ratio >= 0.3:
        return True
    else:
        return False