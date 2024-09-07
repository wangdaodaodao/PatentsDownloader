# PatentsDownloader

PatentsDownloader 是一个用于自动化下载中国专利文档的Python工具。它能够通过关键词搜索专利信息,并根据专利号下载对应的PDF文件。

## 功能特点

- 通过关键词在万方数据库搜索专利信息
- 根据专利号从药物在线网站下载PDF格式的专利文件
- 自动处理验证码页面(需要手动输入验证码)
- 显示下载进度条

## 系统要求

- Python 3.6+
- 依赖库: requests, click, blackboxprotobuf (详见 requirements.txt)

## 安装

1. 克隆仓库:
   ```
   git clone https://github.com/yourusername/PatentsDownloader.git
   cd PatentsDownloader
   ```

2. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

## 使用方法



## 项目结构

- `main.py`: 主程序入口,提供用户交互界面
- `patentdetail.py`: 实现从万方数据库搜索专利信息的功能
- `patentdown.py`: 实现从药物在线网站下载专利PDF的功能
- `config.py`: 存储各种配置信息,如URL和请求头

## 更新日志

- 2022.6.13: 修改get方法,实现protobuf方法访问万方数据库页面
- 2020.5.23: 项目更新

## 待实现功能

- 自动识别验证码
- 区分下载单个专利和批量下载的功能

## 贡献

欢迎提交问题和功能请求。如果您想贡献代码,请fork本仓库并提交pull request。

## 许可证

[MIT License](LICENSE)

## 联系方式

如有任何问题或建议,请联系 [您的邮箱地址]。
