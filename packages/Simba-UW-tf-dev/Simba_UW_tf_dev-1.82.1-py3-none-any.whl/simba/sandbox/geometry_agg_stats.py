import glob
from typing import List, Union
try:
    from typing import Literal
except:
    from typing_extensions import Literal
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from simba.utils.checks import check_iterable_length, check_instance
from simba.mixins.geometry_mixin import GeometryMixin
import cv2
import pandas as pd
from simba.utils.errors import CountError


def geometry_comparison(imgs: List[np.ndarray],
                        shapes: List[Union[Polygon, MultiPolygon]],
                        method: Literal['variance'] = 'variance'):

    if len(imgs) != len(shapes): raise CountError(msg=f'Images and shapes have to be the same size. imgs size: {len(imgs)}, shapes size: {len(shapes)}', source=geometries_descriptives.__name__)
    shared_shape = shapes[0]
    for i in range(1, len(shapes)+1): shared_shape = shapes[1].intersection(shared_shape)
    shared_shape_arr = np.array(shared_shape.exterior.coords).astype(np.int64)
    roi_imgs = []
    for img_cnt, img in enumerate(imgs):
        x, y, w, h = cv2.boundingRect(shared_shape_arr)
        roi_img = img[y:y + h, x:x + w].copy()
        mask = np.zeros(roi_img.shape[:2], np.uint8)
        cv2.drawContours(mask, [shared_shape_arr - shared_shape_arr.min(axis=0)], -1, (255, 255, 255), -1, cv2.LINE_AA)
        bg = np.ones_like(roi_img, np.uint8)
        cv2.bitwise_not(bg, bg, mask=mask)
        roi_img = bg + cv2.bitwise_and(roi_img, roi_img, mask=mask)
        if len(roi_img) > 2:
            roi_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        roi_imgs.append(roi_img)

    current_roi_img = roi_imgs[-1]
    mask_current_roi_img, diff = (current_roi_img != 0), 0
    for img_cnt in range(0, len(roi_imgs)-1):
        mask_previous = (roi_imgs[img_cnt] != 0)
        combined_mask = np.logical_or(mask_current_roi_img, mask_previous)
        non_zero_current, non_zero_previous = current_roi_img[combined_mask], roi_imgs[img_cnt][combined_mask]
        diff += np.sum(cv2.absdiff(non_zero_current, non_zero_previous).flatten())

    result = diff / len(roi_imgs)-1
    print(result)

frm_dir = '/Users/simon/Desktop/envs/troubleshooting/Emergence/project_folder/videos/Example_1_frames'
data_path = '/Users/simon/Desktop/envs/troubleshooting/Emergence/project_folder/csv/outlier_corrected_movement_location/Example_1.csv'
data = pd.read_csv(data_path, nrows=50, usecols=['Nose_x', 'Nose_y']).fillna(-1).values.astype(np.int64)
imgs = []
for file_path in glob.glob(frm_dir + '/*.png'): imgs.append(cv2.imread(file_path))

polygons = []
for frm_data in data: polygons.append(GeometryMixin().bodyparts_to_circle(frm_data, 10))

geometry_comparison(imgs=imgs, shapes=polygons)




