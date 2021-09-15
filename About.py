from tkinter import END, BOTH, YES, Label
from tkinter.scrolledtext import ScrolledText

import tk as tk

#关于我们
class About:
    def __init__(self, win):
        self.win = win
        pass

    def initAbout(self):
        # 文本域
        aboutText = "基于android monkey自带的性能测试工具整合的GUI测试工具\n"
        aboutText += "版本：1.0.0.123\n"
        aboutText += "Copyright © lion.vinno All rights reserved.\n"
        label = Label(self.win, text=aboutText,
                         bg='#ffffff', fg='black',  # bg为背景色，fg为前景色
                         width=200, height=10,  # width为标签的宽，height为高
                         # wraplength = 150,  # 设置多少单位后开始换行
                         anchor='center',  # 东南西北中
                         padx=20,
                         pady=20)  # 设置文本在标签中显示的位置
        label.pack()
