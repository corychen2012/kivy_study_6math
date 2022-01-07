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
        self.tic_start=time.time()

    def tran_color(self, text, code):
        if(code == 'pink'):
            return '[color=#FF60AF]'+text+'[/color]'
        if(code == 'green'):
            return '[color=#28FF28]'+text+'[/color]'
        if(code == 'red'):
            return '[color=#FF0000]'+text+'[/color]'
        return text

    def next_equa(self, dt):
        if(len(self.mathlist) > 0):
            math_equation = self.mathlist.pop()
        elif(len(self.wrong_list) > 0):
            math_equation = self.wrong_list.pop()
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
        self.total_label.text = str(len(self.mathlist))+'/'+self.total_count
        self.wrong_label.text = str(
            len(self.wrong_list))+'/'+self.total_wrong_count

    def do_calc(self, result):
        if(result == self.result_part):
            self.display_label.text = self.tran_color(
                self.math_equation, 'green')
        else:
            self.display_label.text = self.tran_color(
                self.math_equation, 'red')
            self.wrong_list.append(self.math_equation)
            self.total_wrong_count = str(len(self.wrong_list))
        Clock.schedule_once(self.next_equa, 1)

    def gen_mathlist(self):
        self.mathlist = []
        for i in range(1, 2):
            for j in range(0, i+1):
                math = str(i)+'-'+str(j)+'='+str(i-j)
                self.mathlist.append(math)
            for j in range(0, i+1):
                math = str(i-j)+'+'+str(j)+'='+str(i)
                self.mathlist.append(math)
        random.shuffle(self.mathlist)
        return self.mathlist


class MathApp(App):
    def build(self):
        return Math()


if __name__ == "__main__":
    MathApp().run()
