# MathGUI_kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT


import random
import time

LabelBase.register(DEFAULT_FONT, './font/simhei.ttf')


class Math(BoxLayout):
    display_label = ObjectProperty(None)
    total_label = ObjectProperty(None)
    wrong_label = ObjectProperty(None)
    wrong_list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mathlist = self.gen_mathlist()
        self.total_count = str(len(self.mathlist))
        self.total_wrong_count = '0'
        self.next_equa(1)
        self.tic_start = time.time()

    def tran_color(self, text, code):
        if(code == 'pink'):
            return '[color=#FF60AF]'+text+'[/color]'
        if(code == 'green'):
            return '[color=#28FF28]'+text+'[/color]'
        if(code == 'red'):
            return '[color=#FF0000]'+text+'[/color]'
        if(code == 'aqua'):
            return '[color=#00FFFF]'+text+'[/color]'
        return text

    def next_equa(self, dt):
        self.input_result = ''
        if(len(self.mathlist) > 0):
            math_equation = self.mathlist.pop()
            total_count_str = str(
                len(self.mathlist))+'/'+self.total_count
            wrong_count_str = str(
                len(self.wrong_list))+'/'+self.total_wrong_count
            self.total_label.text = self.tran_color(total_count_str, 'aqua')
            self.wrong_label.text = self.tran_color(wrong_count_str, '')
        elif(len(self.wrong_list) > 0):
            math_equation = self.wrong_list.pop()
            total_count_str = str(
                len(self.mathlist))+'/'+self.total_count
            wrong_count_str = str(
                len(self.wrong_list))+'/'+self.total_wrong_count
            self.total_label.text = self.tran_color(total_count_str, '')
            self.wrong_label.text = self.tran_color(wrong_count_str, 'aqua')
        else:
            tic_end = time.time()
            during_time = tic_end-self.tic_start
            math_equation = "真棒!\n用了"+str(round(during_time))+"秒"
            self.display_label.text = self.tran_color(
                math_equation, 'pink')
            return
        self.math_equation = math_equation
        self.display_part = math_equation[:math_equation.index("=")+1]
        self.result_part = math_equation[math_equation.index("=")+1:]
        self.display_label.text = self.tran_color(
            self.display_part, 'pink')

    def do_input(self, input_num):
        self.display_part = self.display_part+str(input_num)
        self.input_result = self.input_result+str(input_num)
        self.display_label.text = self.tran_color(
            self.display_part, 'pink')

    def do_calc(self):
        if(self.input_result == self.result_part):
            self.display_label.text = self.tran_color(
                self.math_equation, 'green')
        else:
            self.display_label.text = self.tran_color(
                self.math_equation, 'red')
            self.wrong_list.append(self.math_equation)
            self.total_wrong_count = str(len(self.wrong_list))
        Clock.schedule_once(self.next_equa, 1)

    def gen_mathlist(self):
        mathlist = []
        for i in range(1, 10):
            for j in range(10-i, 10):
                math = str(i)+'+'+str(j)+'='+str(i+j)
                mathlist.append(math)
                math = str(i+j)+'-'+str(j)+'='+str(i)
                mathlist.append(math)
        random.shuffle(mathlist)
        return mathlist


class Math2App(App):
    def build(self):
        return Math()


if __name__ == "__main__":
    Math2App().run()
