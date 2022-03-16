# pysilk-mod

[![Upload to pypi](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-publish.yml/badge.svg)](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-publish.yml)
[![Build test](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-build-test.yml/badge.svg)](https://github.com/DCZYewen/Python-Silk-Module/actions/workflows/python-build-test.yml)

**支持功能**
 - 非阻塞异步处理
 - 完整的silk/pcm转换
 - 部分支持wav to pcm
 - 跨平台

# 环境准备

```shell
# 使用pip安装(推荐)
pip install pysilk-mod
# 从源码安装
# 在继续之前，请确保你的环境支持编译C/C++文件
pip install git+https://github.com/DCZYewen/Python-Silk-Module
```

# 使用方式

## 通过import调用

```python
import pysilk

# 编码部分，输出silk
pysilk.encode(pcm_data: bytes)
pysilk.encode_file(open("mopemope.pcm", "rb"))
# 解码部分，输出pcm
# to_wav为True时输出wav文件
pysilk.decode(silk_data: bytes, to_wav = False)
pysilk.decode_file(open("brainpower.pcm", "rb"), to_wav=False)

# 异步部分，只要往函数前面加上async_即可
# 如：await pysilk.async_encode(pcm_data: bytes)
```

## 通过shell调用

```shell
# pcm wav转silk文件
python3 -m pysilk input.wav output.silk
python3 -m pysilk input.pcm output.silk
# silk转pcm wav
python3 -m pysilk input.silk output.pcm
python3 -m pysilk input.silk output.wav
# pcm和wav互相转换
python3 -m pysilk input.wav output.pcm
# pcm转wav时，采样率默认设置为24000
# 你可以通过添加-r选项来修改它
python3 -m pysilk -r 24000 input.wav output.pcm
```