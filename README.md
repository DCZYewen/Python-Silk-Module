# pysilk-mod

[![Upload to pypi](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-publish.yml/badge.svg)](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-publish.yml)
[![Build test](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-build-test.yml/badge.svg)](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-build-test.yml)

**支持功能**
 - 非阻塞异步处理
 - 完整的silk/pcm转换
 - 部分支持wav to pcm
 - 跨平台

## 环境准备
```shell
# 从pypi安装
pip install pysilk-mod
# 从源码安装
pip install git+https://github.com/DCZYewen/Python-Silk-Module
```

## 使用方式
```python
import pysilk

#编码部分，输出silk
pysilk.encode(pcm_data: bytes)
pysilk.encode_file(open("mopemope.pcm", "rb"))
#解码部分，输出pcm
# to_wav为True时输出wav文件
pysilk.decode(silk_data: bytes, to_wav=False)
pysilk.decode_file(open("brainpower.pcm", "rb"), to_wav=False)

# 异步部分，只要往函数前面加上async_即可
# 如：await pysilk.async_encode(pcm_data: bytes)
```
