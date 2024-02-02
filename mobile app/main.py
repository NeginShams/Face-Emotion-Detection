from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.loader import Loader
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
import arabic_reshaper
from bidi.algorithm import get_display
from kivy import Config

import os
import urllib
import json
import cv2
import numpy as np
import time

english = True


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    load_text = ""
    cancel_text = ""

    def pre(self):
        if english:
            self.load_text = "Load"
            self.cancel_text = "Cancel"
        else:
            load_txt = arabic_reshaper.reshape("انتخاب")
            self.load_text = get_display(load_txt)

            cancel_txt = arabic_reshaper.reshape("لغو")
            self.cancel_text = get_display(cancel_txt)

        self.load_btn.text = self.load_text
        self.cancel_btn.text = self.cancel_text


class MainWindow(Screen):
    # pass

    eng = ObjectProperty(True)
    fa = ObjectProperty(False)

    def checked(self, instance, value):
        global english
        if value:
            english = False
        else:
            english = True
        # print(english)


class SecondWindow(Screen):
    loadfile = ObjectProperty(None)
    first_time = True
    go_to_main = True

    back_text = ""
    choose_file_text = ""

    def pre(self):
        if english:
            self.back_text = 'back'
            self.choose_file_text = 'Open File Explorer'
        else:
            back_txt = arabic_reshaper.reshape("بازگشت")
            self.back_text = get_display(back_txt)

            choose_file_txt = arabic_reshaper.reshape("بارگذاری فایل تصویر")
            self.choose_file_text = get_display(choose_file_txt)

        # print(self.back_text)

        self.back_btn.text = self.back_text
        self.file_btn.text = self.choose_file_text

    def go_back(self):
        if self.go_to_main == True:
            self.manager.current = 'main'
        else:
            self.go_to_main = True
            self.my_image.source = 'images\surprise.png'
            self.my_label.text = ''
            if english:
                choose_text = 'Open File Explorer'
            else:
                choose_txt = arabic_reshaper.reshape("بارگذاری فایل تصویر")
                choose_text = get_display(choose_txt)

            file_btn = Button(size_hint=(
                0.4, 0.1), text=choose_text, pos_hint={'x': .3, 'y': .2}, font_name='FontsFree-Net-ir_sans')
            file_btn.id = 'file_btn'
            self.file_btn = file_btn
            self.first_time = False
            file_btn.bind(on_press=self.show_load)
            self.add_widget(file_btn)

        # print(english)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, obj):

        if self.first_time == False:
            content = LoadDialog(load=self.load1, cancel=self.dismiss_popup)
        else:
            content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
            # self.remove_widget(self.ok_btn)

        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_load1(self):
        #self.first_time = False
        content = LoadDialog(load=self.load1, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def person_posted(self, req, result):

        self.go_to_main = False
        self.remove_widget(self.loader_image)
        if english:
            self.my_label.text = result
        else:
            if result == 'neutral':
                result_txt = arabic_reshaper.reshape("خنثی")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'happy':
                result_txt = arabic_reshaper.reshape("خوشحال")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'sad':
                result_txt = arabic_reshaper.reshape("غمگین")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'angry':
                result_txt = arabic_reshaper.reshape("عصبانی")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'disgust':
                result_txt = arabic_reshaper.reshape("نفرت")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'fear':
                result_txt = arabic_reshaper.reshape("ترس")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'surprise':
                result_txt = arabic_reshaper.reshape("متعجب")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'face not detected':
                result_txt = arabic_reshaper.reshape("چهره تشخیص داده نشد")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

    def send_request(self, obj):
        picture_array = cv2.imread(self.my_image.source)
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        data = {'arr': picture_array.tolist()}

        # picture_array = cv2.imread(self.my_image.source)
        # picture_array2 = cv2.resize(picture_array, (100, 100))
        # headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        # data = {'arr': picture_array2.tolist()}

        self.remove_widget(self.ok_btn)
        self.remove_widget(self.retry_btn)

        # self.ids.float.remove_widget(self.ids.ok_btn)

        loader_image = Image(source='images\loader2.gif', anim_delay=0.08, size_hint=(
            0.6, 0.4), pos_hint={'x': .2, 'y': .1})
        loader_image.id = 'loader_image'
        self.loader_image = loader_image
        self.add_widget(loader_image)

        req = UrlRequest('http://127.0.0.1:5000/post_person',
                         on_success=self.person_posted, req_body=json.dumps(data), req_headers=headers)

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.my_image.source = filename[0]

        self.my_label.text = ""
        self.dismiss_popup()

    def load1(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.my_image.source = filename[0]

        self.my_label.text = ""
        # self.remove_widget(self.ok_btn)
        # self.remove_widget(self.retry_btn)

        # self.remove_widget(self.file_btn)

        if self.first_time == True:
            self.ids.float.remove_widget(self.ids.file_btn)

        else:
            self.remove_widget(self.file_btn)

        if english:
            retry_text = 'Retry'
        else:
            retry_txt = arabic_reshaper.reshape("تغییر تصویر")
            retry_text = get_display(retry_txt)

        retry_btn = Button(text=retry_text, size_hint=(
            0.3, 0.1), pos_hint={'x': .55, 'y': .1}, font_name='FontsFree-Net-ir_sans')
        retry_btn.id = 'retry_btn'
        self.retry_btn = retry_btn
        retry_btn.bind(on_release=self.show_load)
        self.add_widget(retry_btn)

        if english:
            ok_text = 'OK'
        else:
            ok_txt = arabic_reshaper.reshape("تایید")
            ok_text = get_display(ok_txt)

        ok_btn = Button(text=ok_text, size_hint=(
            0.3, 0.1), pos_hint={'x': .15, 'y': .1}, font_name='FontsFree-Net-ir_sans')
        ok_btn.id = 'ok_btn'
        self.ok_btn = ok_btn
        ok_btn.bind(on_release=self.send_request)
        self.add_widget(ok_btn)

        self.dismiss_popup()


class ThirdWindow(Screen):
    picture_address = ""
    back_text = ""
    first_time = True

    def pre(self):
        if english:
            self.back_text = 'back'
        else:
            back_txt = arabic_reshaper.reshape("بازگشت")
            self.back_text = get_display(back_txt)

        # print(self.back_text)

        self.back_btn.text = self.back_text

    def go_back(self):
        if self.first_time:
            self.manager.current = 'main'
        else:
            self.first_time = True
            camera = self.ids['camera']
            camera.play = True
            self.my_label.text = ''

            cap_btn = Button(size_hint=(0.15, 0.2), pos_hint={
                             'x': .44, 'y': .2}, background_normal='images\cap5.png')
            cap_btn.id = 'cap_btn'
            self.cap_btn = cap_btn
            #self.first_time = False
            cap_btn.bind(on_press=self.capture2)
            self.add_widget(cap_btn)

    def retry_def(self, obj):
        self.first_time = True
        camera = self.ids['camera']
        camera.play = True
        self.remove_widget(self.ok_btn)
        self.remove_widget(self.retry_btn)
        cap_btn = Button(size_hint=(0.15, 0.2), pos_hint={
            'x': .44, 'y': .2}, background_normal='images\cap5.png')
        cap_btn.id = 'cap_btn'
        self.cap_btn = cap_btn
        #self.first_time = False
        cap_btn.bind(on_press=self.capture2)
        self.add_widget(cap_btn)

    def person_posted(self, req, result):
        #self.go_to_main = False
        self.remove_widget(self.loader_image)
        if english:
            self.my_label.text = result
        else:
            if result == 'neutral':
                result_txt = arabic_reshaper.reshape("خنثی")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'happy':
                result_txt = arabic_reshaper.reshape("خوشحال")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'sad':
                result_txt = arabic_reshaper.reshape("غمگین")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'angry':
                result_txt = arabic_reshaper.reshape("عصبانی")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'disgust':
                result_txt = arabic_reshaper.reshape("نفرت")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'fear':
                result_txt = arabic_reshaper.reshape("ترس")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'surprise':
                result_txt = arabic_reshaper.reshape("متعجب")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

            elif result == 'face not detected':
                result_txt = arabic_reshaper.reshape("چهره تشخیص داده نشد")
                result_text = get_display(result_txt)
                self.my_label.text = result_text

    def send_request(self, obj):
        picture_array = cv2.imread(self.picture_address)
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        data = {'arr': picture_array.tolist()}

        self.remove_widget(self.ok_btn)
        self.remove_widget(self.retry_btn)

        loader_image = Image(source='images\loader2.gif', anim_delay=0.08, size_hint=(
            0.6, 0.4), pos_hint={'x': .2, 'y': .1})
        loader_image.id = 'loader_image'
        self.loader_image = loader_image
        self.add_widget(loader_image)

        req = UrlRequest('http://127.0.0.1:5000/post_person',
                         on_success=self.person_posted, req_body=json.dumps(data), req_headers=headers)

    def capture(self):
        self.first_time = False
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        self.picture_address = "IMG_{}.png".format(timestr)
        camera.play = False
        self.ids.float2.remove_widget(self.ids.cap_btn)

        if english:
            ok_text = 'OK'
            retry_text = 'Retry'
        else:
            ok_txt = arabic_reshaper.reshape("تایید")
            ok_text = get_display(ok_txt)

            retry_txt = arabic_reshaper.reshape('تلاش مجدد')
            retry_text = get_display(retry_txt)

        ok_btn = Button(size_hint=(
            0.2, 0.1), text=ok_text, pos_hint={'x': .27, 'y': .2}, font_name='FontsFree-Net-ir_sans')
        ok_btn.id = 'ok_btn'
        self.ok_btn = ok_btn
        #self.first_time = False
        ok_btn.bind(on_press=self.send_request)
        self.add_widget(ok_btn)

        retry_btn = Button(size_hint=(
            0.2, 0.1), text=retry_text, pos_hint={'x': .55, 'y': .2}, font_name='FontsFree-Net-ir_sans')
        retry_btn.id = 'retry_btn'
        self.retry_btn = retry_btn
        #self.first_time = False
        retry_btn.bind(on_press=self.retry_def)
        self.add_widget(retry_btn)

    def capture2(self, obj):
        self.first_time = False
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        self.picture_address = "IMG_{}.png".format(timestr)
        camera.play = False
        self.remove_widget(self.cap_btn)

        if english:
            ok_text = 'OK'
            retry_text = 'Retry'
        else:
            ok_txt = arabic_reshaper.reshape("تایید")
            ok_text = get_display(ok_txt)

            retry_txt = arabic_reshaper.reshape('تلاش مجدد')
            retry_text = get_display(retry_txt)

        ok_btn = Button(size_hint=(
            0.2, 0.1), text=ok_text, pos_hint={'x': .27, 'y': .2}, font_name='FontsFree-Net-ir_sans')
        ok_btn.id = 'ok_btn'
        self.ok_btn = ok_btn
        #self.first_time = False
        ok_btn.bind(on_press=self.send_request)
        self.add_widget(ok_btn)

        retry_btn = Button(size_hint=(
            0.2, 0.1), text=retry_text, pos_hint={'x': .55, 'y': .2}, font_name='FontsFree-Net-ir_sans')
        retry_btn.id = 'retry_btn'
        self.retry_btn = retry_btn
        #self.first_time = False
        retry_btn.bind(on_press=self.retry_def)
        self.add_widget(retry_btn)


class WindowManager(ScreenManager):
    pass


Factory.register('SecondWindow', cls=SecondWindow)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('ThirdWindow', cls=ThirdWindow)

kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
