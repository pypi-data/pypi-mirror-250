# 英文单词书制作

### 介绍
这是一个自然语言处理工具集，主要用于文本处理、分词、词形还原等任务。该工具集可以处理英文文本，提取英文文本中的单词生成单词书，并支持文本的批量处理和保存。


### 安装教程

```bash
pip install -r requirements.txt
```

### 使用说明
```bash
usage: main.py [-h] [-d DIRECTORY] [-f FILE_PATH] [-s START] [-e END]
               [--text TEXT]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        文件夹路径, 处理该文件夹内的文本。
  -f FILE_PATH, --file_path FILE_PATH
                        文档文件路径，处理单个文件。
  -s START, --start START
                        处理单个文件时或直接处理一大段文本时，正则匹配起点。
  -e END, --end END     处理单个文件时或直接处理一大段文本时，正则匹配终点。
  --text TEXT           直接处理一大段文本。
```

### 注意事项
在使用该工具集之前，请确保已经安装了所有必要的Python库。
COCA列表应该是一个文本文件，其中每行包含一个单词。
该工具集默认使用UTF-8编码处理文本。
### 贡献
欢迎任何形式的贡献，包括代码、文档、建议等。请通过GitHub上的issues或者pull requests与我联系。
### 许可证
该软件使用MIT许可证发布。请确保在分发或使用该软件时遵守相应的许可协议。
