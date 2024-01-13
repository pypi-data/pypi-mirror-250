#!/usr/bin/python3

import os
import fitz
import re

def toImage(file_path, png_path, getName=False):

    # 打开pdf
    doc = fitz.open(file_path)

    # pdf文件名
    name = re.sub(r'\.pdf$','',os.path.basename(file_path))

    # 总页数
    total = doc.page_count

    for index in range(total):

        # 读取内容
        page = doc.load_page(index)
        texts = page.get_text("text").split("\n")

        zoom = 300  # 值越大，分辨率越高，文件越清晰
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).prerotate(0)

        pm = page.get_pixmap(matrix=trans, alpha=False)

        # 建立目标文件夹
        if not os.path.exists(png_path):
            os.mkdir(png_path)

        # 图片名称
        filename=name
        if getName:
            filename=getName(name, texts, index, total)
        elif total>1:
            filename=name+"_"+str(index)

        # 保存
        save = os.path.join(png_path, '%s.jpg' %filename)
        pm.save(save)

    # 关闭pdf
    doc.close()
