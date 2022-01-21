'''
Qlabel
Extend the functionality
Mouse move event
'''

import copy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np

AREA_SIZE = 240
MAX_EXPAND = 4


class ExpandLabel(QLabel):
    change_judge_num = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.data = []
        self.data_color = []
        self.move_data = None
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.flag = False
        self.mode = 0
        self.single = 1
        self.setMouseTracking(True)
        self.pixmap = QPixmap()
        self.mypixmap = QPixmap()
        self.now_x = 0
        self.now_y = 0
        self.expend_num = MAX_EXPAND
        self.flag2 = 0
        self.light = 0
        self.contrast = 1
        self.light = 0
        self.contrast_num = 0
        self.light_num = 0
        self.flag3 = 1
        self.judge_num = 0
        self.enter_mouse = self.mode
        self.press_list = []
        self.signal_check_options = 0

    def set_img(self, img_src):
        '''
            设置label中的图片显示
        '''
        self.img = cv2.imread(img_src, 0)
        showImage = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_Indexed8)
        self.setPixmap(QPixmap.fromImage(showImage))

    def changeBloack(self, img_src):
        '''
            设置反色
        '''
        gray = cv2.imread(img_src, 0)
        if self.flag2 == 1:
            dst = 255 - gray
            showImage = QImage(dst.data, dst.shape[1], dst.shape[0], QImage.Format_Indexed8)
            self.setPixmap(QPixmap.fromImage(showImage))
            self.flag2 = 0
        else:
            showImage = QImage(gray.data, gray.shape[1], gray.shape[0], QImage.Format_Indexed8)
            self.setPixmap(QPixmap.fromImage(showImage))
            self.flag2 = 1

    def changeLight(self, img_src):
        '''
        改变亮度
        '''
        img = cv2.imread(img_src, 0)
        img_light = np.uint8(np.clip((cv2.add(self.contrast * img, self.light)), 0, 255))
        showImage = QImage(img_light.data, img_light.shape[1], img_light.shape[0], QImage.Format_Indexed8)
        self.setPixmap(QPixmap.fromImage(showImage))

    def changeContrast(self, img_src):
        '''
        改变对比度
        '''
        img = cv2.imread(img_src, 0)
        img_light = np.uint8(np.clip((cv2.add(self.contrast * img, self.light)), 0, 255))
        showImage = QImage(img_light.data, img_light.shape[1], img_light.shape[0], QImage.Format_Indexed8)
        self.setPixmap(QPixmap.fromImage(showImage))

    def slot_expend_num_add(self):
        '''
        放大倍数 +
        '''
        if self.expend_num >= MAX_EXPAND:
            pass
        else:
            self.expend_num += 1
        self.init_paint_expand()

    def slot_expend_num_reduce(self):
        '''
        放大倍数 -
        '''
        if self.expend_num <= 1:
            pass
        else:
            self.expend_num -= 1
        self.init_paint_expand()

    def init_paint_expand(self):
        '''
        放大状态下，放大框中图像显示比例计算
        '''
        if self.enter_mouse == 1:
            expand_var = AREA_SIZE / self.expend_num
            rect = QRect(self.x2 - expand_var / 2, self.y2 - expand_var / 2, expand_var, expand_var)
            self.mode = 0
            self.mypixmap = self.grab(rect)
            self.width = self.mypixmap.width()
            self.height = self.mypixmap.height()
            self.pixmap = self.mypixmap.scaled((self.width * self.expend_num), (self.height * self.expend_num),
                                               Qt.KeepAspectRatio)
            self.mode = 1
            self.update()

    def init_color(self):
        '''
        默认红框
        '''
        if self.mode == 0:
            for i in range(len(self.data_color)):
                self.data_color[i] = Qt.red

    def check_opt(self):
        '''
        Check the new drop-down position
        '''
        # Avoid changing the length of self.movedata when deleting it
        move_data = copy.deepcopy(self.move_data)
        temp_list = []
        small_list = []
        large_list = []
        for i in self.data:
            # Check whether it is a small frame
            if self.move_data[0] >= i[0] and self.move_data[1] >= i[1] and self.move_data[2] <= i[2] \
                    and self.move_data[3] <= i[3]:
                small_list.append(i)
            # Check whether it is a big frame
            elif self.move_data[0] < i[0] and self.move_data[1] < i[1] and self.move_data[2] > i[2] \
                    and self.move_data[3] > i[3]:
                large_list.append(i)
            # Overlap frame, partial overlap frame, outer frame
            else:
                temp_list.append(i)
        # Internal small box (Do not operate)
        if len(small_list) > 0 and len(small_list) <= len(self.data):
            self.move_data = None
            temp_list = []
        # big frame (Keep the large box drawn and delete the small inner box)
        if len(large_list) > 0 and len(large_list) <= len(self.data):
            for i in large_list:
                self.data.remove(i)
            self.judge_num -= (len(large_list))
            self.change_judge_num.emit(self.judge_num)
            # Non-global large frame
            if len(self.data) > 0:
                pass
            # global large frame
            else:
                self.data.append(self.move_data)
                self.judge_num += 1
                self.change_judge_num.emit(self.judge_num)
        self.move_data = None
        self.update()
        # Overlap frame, partial overlap frame, outer frame must be retained
        if len(temp_list) > 0 and len(temp_list) <= len(self.data):
            if self.move_data != None:
                self.setxy(self.move_data[0], self.move_data[1], self.move_data[2], self.move_data[3])
                self.judge_num += 1
                self.change_judge_num.emit(self.judge_num)
                self.move_data = None
            else:
                self.setxy(move_data[0], move_data[1], move_data[2], move_data[3])
                self.move_data = None
                self.judge_num += 1
                self.change_judge_num.emit(self.judge_num)
        # self.move_data = None
        self.flag = False
        self.update()

    def mouseReleaseEvent(self, event):
        # Left-click release event
        if event.button() == Qt.LeftButton:
            if self.judge_num >= 0 and self.judge_num < 10:
                self.init_color()
                self.x1 = event.x()
                self.y1 = event.y()
                if self.x1 < self.x0 or self.y1 < self.y0:
                    pass
                else:
                    # Click on the 15 by 15 box that appears
                    if self.x1 > self.x0 + 15 or self.y1 > self.y0 + 15:
                        if len(self.data) == 0 or self.data == []:
                            self.judge_num += 1
                            self.change_judge_num.emit(self.judge_num)
                            self.setxy(self.move_data[0], self.move_data[1], self.move_data[2], self.move_data[3])
                            self.move_data = None
                        else:
                            self.check_opt()
                    else:
                        if len(self.data) == 0 or self.data == []:
                            self.setxy(self.x0, self.y0, self.x0 + 15, self.y0 + 15)
                            self.move_data = None
                            self.judge_num += 1
                            self.change_judge_num.emit(self.judge_num)
                        else:
                            self.move_data = [self.x0, self.y0, self.x0 + 15, self.y0 + 15]
                            self.check_opt()
                self.flag = False
                self.update()
            else:
                pwd_messageBox = QMessageBox()
                pwd_messageBox.setWindowTitle("提示")
                pwd_messageBox.setText("报警次数超过最大限度")
                pwd_messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                button_yes = pwd_messageBox.button(QMessageBox.Yes)
                button_yes.setText("确定")
                button_no = pwd_messageBox.button(QMessageBox.No)
                button_no.setText("取消")
                pwd_messageBox.exec_()
                self.update()

    def mouseMoveEvent(self, event):
        '''
            mouseMoveEvent
        '''
        # Record the current mouse position
        self.now_x = event.x()
        self.now_y = event.y()
        expand_var = AREA_SIZE / self.expend_num
        self.single = 0
        if self.mode == 0:
            if self.flag == True:
                if self.now_x < self.x0 + 15 and self.now_y < self.y0 + 15:
                    pass
                else:
                    self.x1 = event.x()
                    self.y1 = event.y()
                    self.move_data = [self.x0, self.y0, self.x1, self.y1]
                    self.update()
            elif self.flag == False:
                self.x2 = event.x()
                self.y2 = event.y()
                self.init_color()
                for index, var in enumerate(self.data):
                    if (self.x2 >= var[0] and self.x2 <= var[2]) and (self.y2 >= var[1] and self.y2 <= var[3]):
                        self.data_color[index] = Qt.green
                    else:
                        self.data_color[index] = Qt.red
                self.update()
            else:
                pass
        if self.mode == 1:
            if self.flag == False:
                self.init_paint_expand()
                self.update()
                rect = QRect(self.x2 - expand_var / 2, self.y2 - expand_var / 2, expand_var, expand_var)
                self.mode = 0
                self.mypixmap = self.grab(rect)
                self.width = self.mypixmap.width()
                self.height = self.mypixmap.height()
                self.pixmap = self.mypixmap.scaled((self.width * self.expend_num), (self.height * self.expend_num),
                                                   Qt.KeepAspectRatio)
                self.mode = 1
                self.update()
                self.x2 = event.x()
                self.y2 = event.y()
                self.init_color()
                for index, var in enumerate(self.data):
                    if (self.x2 >= var[0] and self.x2 <= var[2]) and (self.y2 >= var[1] and self.y2 <= var[3]):
                        self.data_color[index] = Qt.green
                    else:
                        self.data_color[index] = Qt.red
                self.update()
            else:
                self.x2 = event.x()
                self.y2 = event.y()
                self.init_color()
                for index, var in enumerate(self.data):
                    if (self.x2 >= var[0] and self.x2 <= var[2]) and (self.y2 >= var[1] and self.y2 <= var[3]):
                        self.data_color[index] = Qt.green
                    else:
                        self.data_color[index] = Qt.red
                self.update()
                self.move_data = [self.x0, self.y0, self.x2, self.y2]
                rect = QRect(self.x2 - expand_var / 2, self.y2 - expand_var / 2, expand_var, expand_var)
                self.mode = 0
                self.mypixmap = self.grab(rect)
                self.width = self.mypixmap.width()
                self.height = self.mypixmap.height()
                self.pixmap = self.mypixmap.scaled((self.width * self.expend_num), (self.height * self.expend_num),
                                                   Qt.KeepAspectRatio)
                self.mode = 1
                self.update()

    def setxy(self, x1, y1, x2, y2):
        '''
        记录框位置
        '''
        data = [x1, y1, x2, y2]
        self.data.append(data)
        self.data_color.append(Qt.red)

    def paintEvent(self, event):
        '''
        绘图事件
        '''
        self.setScaledContents(True)
        super().paintEvent(event)
        self.painter = QPainter()
        self.painter.begin(self)
        for index, data in enumerate(self.data):
            rect = QRect(data[0], data[1], abs(data[2] - data[0]), abs(data[3] - data[1]))
            self.painter.setPen(QPen(self.data_color[index], 2, Qt.SolidLine))
            self.painter.drawRect(rect)
        if self.move_data is not None:
            rect = QRect(self.move_data[0], self.move_data[1], abs(self.move_data[2] - self.move_data[0]),
                         abs(self.move_data[3] - self.move_data[1]))
            self.painter.setPen(QPen(Qt.yellow, 2, Qt.SolidLine))
            self.painter.drawRect(rect)
        expand_var = AREA_SIZE / self.expend_num
        if self.mode == 1:
            if self.enter_mouse == 1:
                self.painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                self.painter.drawPixmap(self.now_x - expand_var * self.expend_num / 2,
                                        self.now_y - expand_var * self.expend_num / 2, self.pixmap)
                self.painter.drawLine(self.now_x - 10, self.now_y, self.now_x + 10, self.now_y)
                self.painter.drawLine(self.now_x, self.now_y - 10, self.now_x, self.now_y + 10)
        self.painter.end()

    def leaveEvent(self, *args, **kwargs):
        '''
        鼠标移出label事件
        '''
        if self.mode == 0:
            self.enter_mouse = 0
            self.update()
        else:
            if self.enter_mouse == 1:
                self.mode = 0
                self.enter_mouse = self.mode
                self.update()
            else:
                pass
            self.mode = 1

    def enterEvent(self, *args, **kwargs):
        '''
        鼠标移入label事件
        '''
        if self.mode == 1:
            self.enter_mouse = 1
        else:
            self.enter_mouse = 0

    def mousePressEvent(self, event):
        '''
        鼠标按下事件
        '''
        self.init_color()
        if event.button() == Qt.LeftButton:
            if self.judge_num < 10:
                self.flag = True
                self.x0 = event.x()
                self.y0 = event.y()
                if self.flag == True:
                    pass
                self.update()
        elif event.button() == Qt.RightButton:
            x0 = event.x()
            y0 = event.y()
            for index, var in enumerate(self.data):
                if (x0 >= var[0] and x0 <= var[2]) and (y0 >= var[1] and y0 <= var[3]):
                    self.data.remove(var)
                    if self.judge_num <= 10 and self.judge_num > 0:
                        pass
                        self.judge_num -= 1
                        self.change_judge_num.emit(self.judge_num)
                    else:
                        pwd_messageBox = QMessageBox()
                        pwd_messageBox.setWindowTitle("提示")
                        pwd_messageBox.setText("报警次数超过最大限度")
                        pwd_messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        button_yes = pwd_messageBox.button(QMessageBox.Yes)
                        button_yes.setText("确定")
                        button_no = pwd_messageBox.button(QMessageBox.No)
                        button_no.setText("取消")
                        pwd_messageBox.exec_()
                        self.update()
        self.update()
        if self.mode == 1 and event.button == Qt.LeftButton:
            expand_var = AREA_SIZE / self.expend_num
            rect = QRect(int(self.now_x) - expand_var / 2, int(self.now_y) - expand_var / 2, expand_var, expand_var)
            self.mode = 0
            self.update()
            self.mypixmap = self.grab(rect)
            width = self.mypixmap.width()
            height = self.mypixmap.height()
            self.pixmap = self.mypixmap.scaled(width * self.expend_num, height * self.expend_num, Qt.KeepAspectRatio)
            self.mode = 1
            self.update()
