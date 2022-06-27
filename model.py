from dbnet_infer import DBNET
from CRNN import CRNNHandle
import numpy as np
from utils import draw_bbox, crop_rect, sorted_boxes, get_rotate_crop_image
from PIL import Image
import numpy as np
import cv2
import copy
import time
import traceback
import os

filt_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(filt_path) + os.path.sep + ".")

# dbnet 参数
dbnet_max_size = 6000 #长边最大长度
pad_size = 0 #检测是pad尺寸，有些文档文字充满整个屏幕检测有误，需要pad

# crnn参数
crnn_lite = True
#model_path = os.path.join(father_path, "models/dbnet.onnx")
is_rgb = True
#crnn_model_path = os.path.join(father_path, "models/crnn_lite_lstm.onnx")



# angle
angle_detect = False
angle_detect_num = 30
#angle_net_path = os.path.join(father_path, "models/angle_net.onnx")


max_post_time = 100 # ip 访问最大次数

from keys import alphabetChinese as alphabet


white_ips = [] #白名单
version = 'api/v1'


class OcrHandle(object):
    def __init__(self, db_model_path, crnn_model_path):
        self.text_handle = DBNET(db_model_path)
        self.crnn_handle = CRNNHandle(crnn_model_path)


    def crnnRecWithBox(self,im, boxes_list,score_list):
        """
        crnn模型，ocr识别
        @@model,
        @@converter,
        @@im:Array
        @@text_recs:text box
        @@ifIm:是否输出box对应的img

        """
        results = []
        boxes_list = sorted_boxes(np.array(boxes_list))

        line_imgs = []
        for index, (box, score) in enumerate(zip(boxes_list[:angle_detect_num], score_list[:angle_detect_num])):
            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))
            partImg = Image.fromarray(partImg_array).convert("RGB")
            line_imgs.append(partImg)

        angle_res = False
        if angle_detect:
            angle_res = self.angle_handle.predict_rbgs(line_imgs)

        count = 1
        for index, (box ,score) in enumerate(zip(boxes_list,score_list)):

            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))


            partImg = Image.fromarray(partImg_array).convert("RGB")

            if angle_detect and angle_res:
                partImg = partImg.rotate(180)


            if not is_rgb:
                partImg = partImg.convert('L')

            try:
                if is_rgb:
                    simPred = self.crnn_handle.predict_rbg(partImg)  ##识别的文本
                else:
                    simPred = self.crnn_handle.predict(partImg)  ##识别的文本
            except Exception as e:
                print(traceback.format_exc())
                continue

#             if simPred.strip() != '':
#                 results.append([tmp_box,"{}、 ".format(count)+  simPred,score])
#                 count += 1
            if simPred.strip() != '':
                results.append([tmp_box,simPred,score])
                count += 1

        return results


    def text_predict(self,img,short_size):
        boxes_list, score_list = self.text_handle.process(np.asarray(img).astype(np.uint8),short_size=short_size)
        result = self.crnnRecWithBox(np.array(img), boxes_list,score_list)
        
        return result