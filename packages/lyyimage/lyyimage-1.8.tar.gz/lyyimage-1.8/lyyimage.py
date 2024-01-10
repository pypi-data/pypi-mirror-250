import base64
from PIL import Image
import numpy as np
import io
import requests


def preprocess_image(image_path):
    """
    对图片进行处理以便ocr识别

    Args:
        image_path (str): 文件路径

    Returns:
        _type_: image data of base64 str
    """
    # 打开图片
    image = Image.open(image_path)

    # 灰度化
    image = image.convert('L')

    # 二值化
    image = image.point(lambda x: 0 if x < 128 else 255, '1')

    # 将图片转换为 base64 编码
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    #image.save('preprocessed.png')#保存到硬盘
    img_byte = buffered.getvalue()
    return base64.b64encode(img_byte).decode('utf-8')


def encode_image(image_path):
    """
    将图片转换为 base64 编码
    
    """
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_byte = buffered.getvalue()
        return base64.b64encode(img_byte).decode('utf-8')


def ocr_img_file_to_text(image_path, debug=False):
    """
    识别图像文件，使用Umi-Ocr http方式

    Args:
        image_path (str): 图像文件路径
        debug (bool, optional): 是否打印详细处理过程中的信息. Defaults to False.

    Returns:
        _type_: 返回识别后的文本
    """
    if debug: print("------------------------------------ocr----------------------------------------")
    base64img = preprocess_image(image_path)

    url = "http://127.0.0.1:10024/api/ocr"
    data = {"base64": base64img, "ocr": {"language": "models/config_chinese.txt", "cls": False, "limit_side_len": 960, "tbpu": {"merge": "MergeLine"}}, "rapid": {"language": "简体中文", "angle": False, "maxSideLen": 1024, "tbpu": {"merge": "MergeLine"}}}
    if debug: print("post image data to umi-ocr")
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        text = ""
        result_data = result.get("data")
        if "No text" in result_data:  #No text found in image. Path: "base64"
            return False
        for i in result_data:
            t = i['text']
            #t= t+"\n"  if len(t)>10 else " "
            text += t
        if debug: print("ocr response result=，=", text)

    else:
        print("识别失败")
        return False
    return text


if __name__ == "__main__":

    # 测试
    base64_image = preprocess_image('/path/to/your/image.png')  # 替换为你的图片文件路径
    print(base64_image)
