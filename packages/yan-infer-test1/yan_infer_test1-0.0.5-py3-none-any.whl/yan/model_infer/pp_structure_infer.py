import json
from copy import deepcopy

import cv2
import html2text
import numpy as np
import paddle

paddle.device.set_device('cpu')
from paddleocr import (PaddleOCR,
                       PPStructure)


def combine_box(box1, box2, type1, type2):  # 合并bbox以及类型
    x0 = min(box1[0], box2[0])
    y0 = min(box1[1], box2[1])
    x1 = max(box1[2], box2[2])
    y1 = max(box1[3], box2[3])
    if type1 == type2:
        new_type = type1
    elif 'table' in type1 or 'table' in type2:
        new_type = 'table'
    elif 'figure' in type1 or 'figure' in type2:
        new_type = 'figure'
    else:
        new_type = 'text'
    return ([x0, y0, x1, y1], new_type)
    # [x0,y0,x1,y1]，其中(x0,y0)为left-top坐标，(x1,y1)为right-bottom坐标。
    # new_type是新类型，使用以下规则：表>图>文字


def IoU(box1, box2):  # 有交集返回True
    in_h = min(box1[2], box2[2]) - max(box1[0], box2[0])
    in_w = min(box1[3], box2[3]) - max(box1[1], box2[1])
    is_common = False if in_h < 0 or in_w < 0 else True
    return is_common


# lang-->language:[`ch`, `en`, `fr`, `german`, `korean`, `japan`,...]
# use_anle_cls--->是否使用文字方向分类器，默认为False
def layout_table_analysis(img: np.ndarray, lang: str = 'ch', use_gpu: bool = True, return_html: bool = True,
                          return_md: bool = False, return_text: bool = True, use_angle_cls=False):
    assert (return_html | return_md) == True

    ####################################
    # 第一阶段：目标检测+合并
    ####################################
    table_engine = PPStructure(show_log=False, table=True, use_gpu=use_gpu, ocr=False,
                               structure_version="PP-StructureV2")
    sub_images, sub_tables, sub_texts = [], [], []
    size = img.shape
    height, width = size[0], size[1]
    result = table_engine(img)
    # 先按照面积排序/不排序也可以
    # 'bbox':[左上x,左上y,右下x,右下y],后面返回值内的bbox均为这种格式
    result = sorted(result, key=lambda x: (x['bbox'][2] - x['bbox'][0]) * (x['bbox'][3] - x['bbox'][1]), reverse=True)
    copy = img.copy()
    for box in enumerate(result):
        x1, y1, x2, y2 = box[1]['bbox']
        cv2.rectangle(copy, (x1, y1), (x2, y2), (0, 0, 255), 6)
        # 保存图像
        cv2.imwrite('image_with_box.jpg', copy)

    s, L = set(), len(result)
    for j in range(L):
        if j in s:
            continue
        for k in range(j + 1, L):
            if k < L:  # 避免越界
                box1, box2 = result[j]['bbox'], result[k]['bbox']
                if IoU(box1, box2):
                    type1, type2 = result[j]['type'], result[k]['type']
                    Box, Type = combine_box(box1, box2, type1, type2)
                    result[j] = {'type': Type, 'bbox': Box}
                    s.add(k)

        if result[j]['type'] == 'table':
            sub_tables.append(result[j])
        elif result[j]['type'] == 'figure':
            sub_images.append(result[j])
        else:
            sub_texts.append(result[j])

    ####################################
    # 第二阶段：分类识别：图->记录位置 表->记录位置+html/md 文字->记录位置+ocr结果
    ####################################
    res = {'tables': [], 'figures': [], 'texts': []}
    if len(sub_images) > 0:
        for image in sub_images:
            res['figures'].append(image['bbox'])

    if len(sub_tables) > 0:
        table_engine1 = PPStructure(show_log=False, use_gpu=use_gpu, layout=False, table=True, ocr=False)

        for table in sub_tables:
            left_top_x, left_top_y, right_bottom_x, right_bottom_y = table['bbox'][0], table['bbox'][1], table['bbox'][
                2], table['bbox'][3]
            tmp_res = table_engine1(img[left_top_y:right_bottom_y, left_top_x:right_bottom_x, :])[0]  # 这一步很耗时
            temp = {'bbox': table['bbox'], 'html': None, 'md': None}
            if return_html:
                temp['html'] = tmp_res['res']['html']
            if return_md:
                temp['md'] = html2text.html2text(tmp_res['res']['html'])
            res['tables'].append(deepcopy(temp))

    if return_text:
        if len(sub_texts) > 0:
            ocr = PaddleOCR(use_gpu=use_gpu, use_angle_cls=use_angle_cls, lang=lang, show_log=False)

            copy = img.copy()
            for text in sub_texts:
                x1, y1, x2, y2 = text['bbox'][0], text['bbox'][1], text['bbox'][
                    2], text['bbox'][3]
                cv2.rectangle(copy, (x1, y1), (x2, y2), (0, 0, 255), 4)
                # 保存图像
                cv2.imwrite('image_with_box1.jpg', copy)

            for text in sub_texts:
                left_top_x, left_top_y, right_bottom_x, right_bottom_y = text['bbox'][0], text['bbox'][1], text['bbox'][
                    2], text['bbox'][3]
                px = 50
                crop_img = img[left_top_y - px:right_bottom_y + px, left_top_x - px:right_bottom_x + px, :]
                cv2.imwrite('1.jpg', crop_img)
                temp = ocr.ocr(crop_img, cls=use_angle_cls)
                temp_text = []
                if temp == [] or temp[0] is None:
                    continue
                for idx in range(len(temp)):
                    for line in temp[idx]:
                        temp_text.append(line[1][0])
                res['texts'].append({'bbox': text['bbox'], 'text': temp_text[:]})
    # res ->{'tables':[{'bbox':[x0,y0,x1,y1],'html':a,'md':a},...,{}],'figures':List[List],'texts':[{'bbox':a,'text':List[str]},...,{}]}
    # 'bbox'：[x0,y0,x1,y1]，其中(x0,y0)为left-top坐标，(x1,y1)为right-bottom坐标。
    return json.dumps(res)


def layout_analysis(img: np.ndarray, use_gpu=True):
    table_engine = PPStructure(table=False, ocr=False, show_log=False, use_gpu=use_gpu)
    result = table_engine(img)
    temp = {'res': []}
    for res in result:
        res.pop('img')
        res.pop('res')
        res.pop('img_idx')
        temp['res'].append(deepcopy(res))
    # temp ={'res':[res,...,res]}
    # res ---- {'type':str,'bbox':List[int]}
    # 'bbox'：[x0,y0,x1,y1]，其中(x0,y0)为left-top坐标，(x1,y1)为right-bottom坐标。
    return json.dumps(temp)


def ocr(img: np.ndarray, use_gpu: bool = True, lang: str = 'ch', use_angle_cls: bool = False) -> str:
    ocr = PaddleOCR(use_gpu=use_gpu, use_angle_cls=use_angle_cls, lang=lang, show_log=False)
    result = ocr.ocr(img, cls=use_angle_cls)
    temp = {'res': []}
    for idx in range(len(result)):
        for line in result[idx]:
            temp['res'].append({'bbox': line[0][0] + line[0][2], "text": line[1][0]})  # 只返回左上，右下
    # Dict[List[Dict]]
    # {'res': [{'bbox':[935.0, 190.0, 1053.0, 224.0]],'text': '二三四五'},...,{}]}
    # 'bbox'：[x0,y0,x1,y1]，其中(x0,y0)为left-top坐标，(x1,y1)为right-bottom坐标。
    return json.dumps(temp)


if __name__ == '__main__':
    img_path = '1.png'
    # img_path = 'ocr_img/table_2.png'
    img = cv2.imread(img_path)
    #
    table_analysis = layout_table_analysis(img, return_text=True, return_md=True)
    print(table_analysis)

    # temp = ocr(img)
    # print(temp)
