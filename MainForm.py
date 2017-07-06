import subprocess
import sys
import os.path
from tkinter import ttk
import tkinter as tk
import time
import random
import requests

#win = ttk.Tk()
#lbfac = ttk.Label(win, textvariable=var)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    if col == 'Сумма':
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
    else:
        l.sort(key=lambda t: t[0], reverse=reverse)
    for index, (val, k) in enumerate(l): 
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

class Form:

    def __init__(self, parent):
        super().__init__()
        self.initUI()

    def initUI(self):
        win.geometry("%dx%d+0+0" % (win.winfo_screenwidth(), win.winfo_screenheight()))
        win.resizable(width=0, height=0)
    

        tk.Entry(win).grid(sticky='we')
        win.grid_columnconfigure(0, weight=1)
        
        style = ttk.Style(win)
        style.configure('Treeview', rowheight=48)
        self.tree = ttk.Treeview(win, selectmode='browse', height=int(win.winfo_screenheight()/48) - 3)
        self.tree.grid(row = 0, column = 0, rowspan = 20, columnspan = 11)
        self.tree['show'] = 'headings'
        self.tree.heading('#0', text='Name\n')
        self.tree["columns"] = ["ФИО", "Оригинал документа\nоб образовании", "Согласие на\nзачисление", "Предмет 1", "Предмет 2", "Предмет 3", "Предмет 4", "Доп. баллы", "Сумма", "Статус", "Направление"]
        #tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.tree.column("ФИО", anchor='c', stretch = True)
        self.tree.column("Оригинал документа\nоб образовании", anchor='c', stretch = True, width = 150)
        self.tree.column("Согласие на\nзачисление", anchor='c', stretch = True, width = 100)
        self.tree.column("Предмет 1", anchor='c', stretch = True, width = 100)
        self.tree.column("Предмет 2", anchor='c', stretch = True, width = 100)
        self.tree.column("Предмет 3", anchor='c', stretch = True, width = 100)
        self.tree.column("Предмет 4", anchor='c', stretch = True, width = 100)
        self.tree.column("Доп. баллы", anchor='c', stretch = True, width = 100)
        self.tree.column("Сумма", anchor='c', stretch = True, width = 100)
        self.tree.column("Статус", anchor='c', stretch = True, width = 100)
        self.tree.column("Направление", anchor='c', stretch = True, width = 200)
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Оригинал документа\nоб образовании", text="Оригинал документа\nоб образовании")
        self.tree.heading("Согласие на\nзачисление", text="Согласие на\nзачисление")
        self.tree.heading("Предмет 1", text="Предмет 1")
        self.tree.heading("Предмет 2", text="Предмет 2")
        self.tree.heading("Предмет 3", text="Предмет 3")
        self.tree.heading("Предмет 4", text="Предмет 4")
        self.tree.heading("Доп. баллы", text="Доп. баллы")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Статус", text="Статус")
        self.tree.heading("Направление", text="Направление")
        self.vsb = ttk.Scrollbar(win, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row = 0, column = 12, rowspan = 20, sticky = 'NS')
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.hsb = ttk.Scrollbar(win, orient="horizontal", command=self.tree.xview)
        self.hsb.grid(row = 20, column = 0, sticky = 'WE')
        self.tree.configure(xscrollcommand=self.hsb.set)

        self.lbfac = tk.Label(win, text = 'Готовность - 0%')
        self.lbfac.grid(row = 0, column = 13, sticky = 'NW', columnspan = 7)

        columns = ("ФИО", "Оригинал документа\nоб образовании", "Согласие на\nзачисление", "Предмет 1", "Предмет 2", "Предмет 3", "Предмет 4", "Доп. баллы", "Сумма", "Статус", "Направление")

        for col in columns:
            self.tree.heading(col, text=col, command=lambda col_ = col: treeview_sort_column(self.tree, col_, False))

def readlist(a):
    l = []
    if not os.path.isfile('Isu_Prof_Table.ProfTab'):
        a.lbfac['text'] = 'Загружается таблица\nфакультетов...'
        os.system('pyhton Get_Prof_Table.py')
    f = open('Isu_Prof_Table.ProfTab', 'r', encoding = 'UTF-8')
    count = 0
    for str in f:
        if str.find('<link>') != -1:
            l.append(str[str.find('<link>') + 6: str.find('</link>')])
            count = count + 1
    f.close()
    a.lbfac['text'] = 'Таблица загружена\nЗагружается список абитуриентов\nГотовность - 0%'
    return l, count

def fill_table(a, l, count):
    c = 0

    #l = ['isu.ru/Abitur/ru/rating/table.html?group=c6bd587445be0bd9de3892b7bac8d496']
    f = open('test.test','w',encoding = 'UTF-8')

    for i in l:
        rq = requests.get('http://'+i)
        q = rq.text
        q = q[q.find('<table'):]
        q = q[q.find('</tr>'):]
        q = q[q.find('</td>') + 1:]
        dir = q[q.find('<td>') + 4 : q.find('</td>')]
        dir = dir[:dir.find(' ')]
        q = q[q.find('</table>') + 1:]
        q = q[q.find('<table'):q.find('</table>')]
        q = q[q.find('</tr>') + 1:]
        obj = q[q.find('<tr>') + 4:q.find('</tr>')]
        obj_list = []
        while(obj.find('<th') != -1):
            obj_list.append(obj[obj.find('>') + 1:obj.find('</th>')])
            obj = obj[obj.find('</th>') + 5:]
        c = len(obj_list)
        while len(obj_list) < 4:
                obj_list.append('-')
        q = q[q.find('</tr>') + 1:]
        while q.find('<tr') != -1 :
            pers = q[q.find('<tr') + 4 : q.find('</tr>')]
            q = q[q.find("</tr>") + 1 : ]
            pers = pers[pers.find('</td>') + 1 : ]
            fio = pers[pers.find('<td>') + 4 : pers.find('</td>')]
            fio = fio.replace(' ','\n')
            pers = pers[pers.find('</td>') + 1:]
            orig = pers[pers.find('<td>') + 4:pers.find('</td>')]
            pers = pers[pers.find('</td>') + 1:]
            agg = pers[pers.find('<td>') + 4:pers.find('</td>')]
            marks = []
            for i in range(0, c):
                pers = pers[pers.find('</td>') + 1:]
                if pers[pers.find('<td>') + 4 : pers.find('</td>')] == 'Проверка результатов' or len(pers[pers.find('<td>') + 4 : pers.find('</td>')]) < 2 :
                    marks.append(0)
                else:
                    marks.append(pers[pers.find('<td>') + 4 : pers.find('</td>')])
                    
            while len(marks) < 4:
                marks.append('0')
            pers = pers[pers.find('</td>') + 1:]
            add = pers[pers.find('<td>') + 4:pers.find('</td>')]
            pers = pers[pers.find('</td>') + 1:]
            sum = pers[pers.find('<td>') + 4:pers.find('</td>')]
            pers = pers[pers.find('</td>') + 1:]
            stat = pers[pers.find('<td>') + 4:pers.find('</td>')]
            stat = stat.replace(' ','\n')
            a.tree.insert("","end",values = (fio, orig, agg, str(marks[0]) + '\n' + obj_list[0], str(marks[1]) + '\n' + obj_list[1], str(marks[2]) + '\n' + obj_list[2], str(marks[3]) + '\n' + obj_list[3], add, sum, stat, dir))

    #f.close()

        # c = c + 1
        # a.lbfac['text'] = 'Таблица загружена\nЗагружается список абитуриентов\nГотовность - ' + str(int(c / count * 100))+ '%'
        # random.seed()
        # tm = random.random() / 5
        # time.sleep(tm)

if __name__ == '__main__':
    win = tk.Tk()
    a = Form(win)
    l, count = readlist(a)
    fill_table(a, l, count)

    win.mainloop()
