<img src="./logo.jpeg" />

# py3office
提供python3版本的自动化办公常用处理方法

<p>
    <a href="https://github.com/fragement-contrib/py3office" target='_blank'>
        <img alt="GitHub repo stars" src="https://img.shields.io/github/stars/fragement-contrib/py3office?style=social">
    </a>
</p>

<!-- pip3 install . -->

## 使用

首先需要进行安装：

```
pip3 install py3office
```

然后就可以使用了，下面列出所有可用内容：

### handler

```python
from py3office import handler
```

#### listFile

```python
handler.listFile(folder, callback)
```

callback有一个字典类型的参数fileInfo，格式如下：

```js
{
    "path": <文件路径> ,
    "folder": <当前文件所在文件夹>
}
```

### pdf

```python
from py3office import pdf
```

#### toImage

把pdf转成图片：

```python
pdf.toImage(pdfUrl, targetFolder)
```

你还可以传递一个函数来自定义图片名称：

```python
# 文件名、内容、页序号、页数
def getName(name, texts, index, total):
    return <新的名称>

pdf.toImage(pdfUrl, targetFolder, getName)
```

## 版权

MIT License

Copyright (c) [zxl20070701](https://zxl20070701.github.io/notebook/home.html) 走一步，再走一步
