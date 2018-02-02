import requests

import sys, time

class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 50 #进度条的长度

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps):
        self.max_steps = max_steps
        self.i = 0
        self.show_process()

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                    + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边        
        # process_bar = '[' + '>' * num_arrow + '-' * num_line + ']' + '\r'
        sys.stdout.write(process_bar) #这两句打印字符到终端
        sys.stdout.flush()

    def close(self):
        words = '下载完毕!!!!' + ' '*self.max_arrow
        sys.stdout.write(words)
        sys.stdout.flush()
        self.i = 0
        print()

def down_file(url, filename):
    response = requests.get(url, stream=True)
    max_steps =   int(response.headers['content-length'])/1024 # 内容体总大小
    print('专利号：{}  文件大小:{:.2f}k'.format(filename.split('\\')[-1],max_steps))
    process_bar = ShowProcess(max_steps)
    with open(filename, "wb") as file:
        for data in response.iter_content(chunk_size=1024):
            
            file.write(data)
            process_bar.show_process()
    process_bar.close()
            
# down_file('http://pub.bcbay.com/upload_files/image/201605/20160514_14632806993828.jpg', '1.jpg')