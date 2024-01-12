import numpy as np
import pandas as pd
import cv2
from simba.utils.enums import Keys
import ast

try:
    from typing import Literal
except:
    from typing_extensions import Literal

def get_geometry_brightness_intensity(img: np.ndarray,
                                     roi_vertices: np.ndarray,
                                     rois_type: Literal['rectangles', 'circle', 'polygons']) -> np.ndarray:
    """
    Calculate the average brightness intensity within a geometry / region-og-interest of an image.

    E.g., can be used with hardcoded thresholds or e.g., kmeans to detect if a light source is ON or OFF

    :param np.ndarray img: The input image.
    :param np.ndarray roi_vertices: An array containing the vertices of the ROIs if polygon or rectangles, or center and radius if circles.
    :param Literal['rectangles', 'polygons', 'circles'] rois_type: Type of ROIs, must be one of 'rectangles', 'polygons', or 'circles'.
    :returns np.ndarray: An array containing the average brightness intensity for each ROI.

    :example:
    >>> roi_df = pd.read_csv('/Users/simon/Desktop/envs/troubleshooting/khan/project_folder/logs/rectangles_20240108130230.csv', index_col=0)
    >>> rectangle_vertices = roi_df[['topLeftX', 'topLeftY', 'Bottom_right_X', 'Bottom_right_Y']].values
    >>> img = cv2.imread('/Users/simon/Desktop/envs/troubleshooting/khan/project_folder/videos/stitched_frames/0.png').astype(np.uint8)
    >>> get_geometry_brightness_intensity(img=img, roi_vertices=rectangle_vertices, rois_type='rectangles')
    >>> [152., 222., 169., 227.]
    >>> polygon_vertices = np.array([[[467 , 55],   [492, 177],   [797, 182],   [797, 50]],  [[35, 492],   [238, 502],   [253, 817],   [30, 812]],  [[1234, 497],   [1092, 497],   [1086, 812],   [1239, 827]],  [[452, 1249],   [467, 1046],   [772, 1066], [766, 1249]]])
    >>> get_geometry_brightness_intensity(img=img, roi_vertices=polygon_vertices, rois_type='polygons')
    >>> [110., 171., 115., 164.]
    """
    intensities = np.full(roi_vertices.shape[0], fill_value=np.nan)
    if rois_type == Keys.ROI_RECTANGLES.value:
        for roi_cnt, roi in enumerate(roi_vertices):
            roi_img = img[roi[1]:roi[3], roi[0]:roi[2]]
            intensities[roi_cnt] = np.ceil(np.average(roi_img))
    elif rois_type == Keys.ROI_POLYGONS.value:
        for roi_cnt, roi in enumerate(roi_vertices):
            x,y,w,h = cv2.boundingRect(roi)
            roi_img = img[y:y + h, x:x + w].copy()
            mask = np.zeros(roi_img.shape[:2], np.uint8)
            cv2.drawContours(mask, [roi - roi.min(axis=0)], -1, (255, 255, 255), -1, cv2.LINE_AA)
            bg = np.ones_like(roi_img, np.uint8)
            cv2.bitwise_not(bg, bg, mask=mask)
            roi_img = bg + cv2.bitwise_and(roi_img, roi_img, mask=mask)
            intensities[roi_cnt] = np.ceil(np.average(roi_img[roi_img != 0]))
    elif rois_type == Keys.ROI_CIRCLES.value:
        for roi_cnt, roi in enumerate(roi_vertices):
            roi_img = img[roi[1]:(roi[1] + 2 * roi[2]), roi[0]:(roi[0] + 2 * roi[2])]
            mask = np.zeros(roi_img.shape[:2], np.uint8)
            circle_img = cv2.circle(mask, (roi[0], roi[1]), roi[2], (255, 255, 255), thickness=-1)
            bg = np.ones_like(roi_img, np.uint8)
            cv2.bitwise_not(bg, bg, mask=mask)
            roi_img = bg + cv2.bitwise_and(roi_img, roi_img, mask=circle_img)
            intensities[roi_cnt] = np.ceil(np.average(roi_img[roi_img != 0]))
    return intensities
