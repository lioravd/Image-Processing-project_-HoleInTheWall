import cv2
import pygame
import numpy as np
from scipy import signal
from scipy import ndimage
import matplotlib.pyplot as plt


def fillhole(input_image):
    '''
    input gray binary image  get the filled image by floodfill method
    Note: only holes surrounded in the connected regions will be filled.
    :param input_image:
    :return:
    '''
    im_flood_fill = input_image.copy()
    h, w = input_image.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    im_flood_fill = im_flood_fill.astype("uint8")
    cv2.floodFill(im_flood_fill, mask, (0, 0), 1)
    im_flood_fill_inv = cv2.bitwise_not(im_flood_fill)+2
    img_out = input_image | im_flood_fill_inv
    return img_out

def filter_person(frame, calibration_image):   #
    (h_frame, w_frame, z) = frame.shape
    # ---- matrix subtract
    game_img = np.zeros(frame.shape)

    # ---- convert to HSV color space
    frame= cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    calibration_HSV = cv2.cvtColor(calibration_image, cv2.COLOR_RGB2HSV)

    # ---- reduce value from HSV image for shadow
    value = frame[:,:,2]
    cal_value = calibration_HSV[:,:,2]
    value[(value<0.2) & (cal_value>0.2)] += 0.05
    frame[:, :, 2] = value

    # ---- back to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)

    # ---- matrix subtract
    game_img[:, :, 0] = abs(frame[:, :, 0] - calibration_image[:, :, 0])
    game_img[:, :, 1] = abs(frame[:, :, 1] - calibration_image[:, :, 1])
    game_img[:, :, 2] = abs(frame[:, :, 2] - calibration_image[:, :, 2])

    # ---- threshold by channel
    ret, game_img[:, :, 0] = cv2.threshold(game_img[:, :, 0], 0.15, 1, cv2.THRESH_BINARY)
    ret, game_img[:, :, 1] = cv2.threshold(game_img[:, :, 1], 0.15, 1, cv2.THRESH_BINARY)
    ret, game_img[:, :, 2] = cv2.threshold(game_img[:, :, 2], 0.15, 1, cv2.THRESH_BINARY)

    # ---- median Filter
    game_img = cv2.medianBlur((game_img * 255).astype(np.uint8), 5) / 255


    # ---- convert to graysacle
    frame_mask = np.float32(game_img)
    frame_mask = cv2.cvtColor(frame_mask, cv2.COLOR_RGB2GRAY)

    # ---- histogram equaliziation
    frame_mask = cv2.equalizeHist((frame_mask * 255).astype(np.uint8)) / 255


    # ---- filtering and dilate grayscale image
    ret, frame_mask = cv2.threshold(frame_mask, 0.2, 1, cv2.THRESH_BINARY)
    frame_mask = signal.medfilt2d(frame_mask, (11, 9))  # filter noise
    frame_mask = cv2.dilate(frame_mask, np.ones((11, 9), np.float32))
    frame_mask = signal.medfilt2d(frame_mask, (7, 7))  # filter noise



    #find contures
    contours, hierarchy = cv2.findContours(image=(frame_mask * 255).astype(np.uint8), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    len_con = len(contours)


    #set frame to 0 where mask is 0
    if len(contours)>0:
        # if BOX area above minimum create box
        boxes = [cv2.boundingRect(contours[i]) for i in range(len_con) if cv2.boundingRect(contours[i])[3] * cv2.boundingRect(contours[i])[2]>11000]


    # create new matrix to extract BOX
    zero_frame = np.zeros((h_frame, w_frame))

    # ---- Cleaning small boxes from image
    if len_con and len(boxes) > 0:
        if len(boxes):
            for box in boxes:
                x,y,w,h = box
                zero_frame[y:y+h, x:x+w] = frame_mask[y:y+h,x:x+w]
                #cv2.rectangle(zero_frame, (x, y), (x + w, y + h), (1), thickness=2)

    frame_mask = zero_frame
    frame_mask = signal.medfilt2d(frame_mask, (5, 5))  # filter noise

    return frame_mask


def frame_to_mask(frame, calibration_image):
    frame = pygame.surfarray.array3d(frame)
    frame = frame.swapaxes(0, 1)
    calibration_image = pygame.surfarray.array3d(calibration_image)
    calibration_image = calibration_image.swapaxes(0, 1)
    calibration_image = np.float32(calibration_image)  # convert to float32 image
    calibration_image = calibration_image / 255  # normalize between [0,1]
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.float32(frame)
    frame = frame / 255
    frame_mask = filter_person(frame, calibration_image)
    return frame_mask
