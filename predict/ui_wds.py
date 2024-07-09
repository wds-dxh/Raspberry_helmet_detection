#ui_wds.py
import sys
from PyQt6 import QtWidgets,QtCore,uic
from PyQt6.QtWidgets import QApplication,QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import cv2
from tools.ncnn_predict import yolov8_wds
from tools.Judge_whether_wear   import Judge_whether_wear


class ui_wds():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui: QtWidgets.QWidget = uic.loadUi("layout.ui")  # 加载ui文件
        #设置应用名称
        self.app.setApplicationName("头盔检测系统")   
        self.ui.setWindowTitle("头盔检测系统")
        self.ui.resize(600, 600)

        #指明label的格式
        self.label_vedio: QtWidgets.QLabel = self.ui.findChild(QtWidgets.QLabel, "label")
        self.label_image1: QtWidgets.QLabel = self.ui.findChild(QtWidgets.QLabel, "label_2")
        self.label_image2: QtWidgets.QLabel = self.ui.findChild(QtWidgets.QLabel, "label_3")
        self.button_start: QtWidgets.QPushButton = self.ui.findChild(QtWidgets.QPushButton, "pushButton")
        self.gridLayoutWidget: QtWidgets.QWidget = self.ui.findChild(QtWidgets.QWidget, "gridLayoutWidget")
        self.yolo = yolov8_wds(model_path=r'.\models\best.pt')
        self.judge = Judge_whether_wear()
        self.is_open_camera = False # 默认摄像头是关闭的
        self.video_cap = None
        self.camera_timer = QtCore.QTimer(self.ui)  # 创建读取摄像头图像的定时器
        self.camera_timer.timeout.connect(self.play_camera_video)   # 定时器超时信号连接到槽函数play_camera_video
        self.which_camera = 0 #判断该哪一个label显示图片

        #给label加上黑色边框
        self.label_vedio.setStyleSheet("border: 1px solid black")
        self.label_vedio.setMinimumSize(320, 240) 
        self.label_vedio.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 让标签要显示的内容居中
        self.label_image1.setStyleSheet("border: 1px solid black")
        self.label_image2.setStyleSheet("border: 1px solid black")
        
        self.button_start.setText("打开摄像头")
        if self.gridLayoutWidget is None:
            print("Error: gridLayoutWidget is None. Check your UI file.")
        else:
            # 使用布局管理器来管理窗口布局
            layout = QtWidgets.QVBoxLayout(self.ui)
            layout.addWidget(self.gridLayoutWidget)
            self.ui.setLayout(layout)


        #绑定按钮事件，控制摄像头
        self.button_start.clicked.connect(self.start_camera)


    def start_camera(self):
        if not self.is_open_camera: # 按下 打开摄像头 按钮
            self.video_cap = cv2.VideoCapture(r".\tools\test.mp4")  # 打开默认摄像头（索引为0）
            print('camera fps:', self.video_cap.get(cv2.CAP_PROP_FPS))
            self.camera_timer.start(20)  # 20毫秒刷新一次
            self.is_open_camera = True
            self.button_start.setText('关闭摄像头')
            print('打开摄像头')
        else:  # 按下 关闭摄像头 按钮
            self.camera_timer.stop()
            self.video_cap.release()
            self.video_cap = None
            self.label_vedio.clear()
            self.button_start.setText('打开摄像头')
            self.is_open_camera = False
            print('关闭摄像头')
    
    def play_camera_video(self):
        if self.is_open_camera:
            _, frame = self.video_cap.read()  # 读取视频流的每一帧
            frame, _, cls = self.yolo.process_frame(frame)
            height, width, channel = frame.shape  # 获取图像高度、宽度和通道数, 通常为为640x480x3
            img = QImage(frame.data, width, height, QImage.Format.Format_RGB888)
            img = img.rgbSwapped()  # 进行颜色通道交换，rgbSwapped是因为OpenCV读取的图像是BGR格式的，而QImage是RGB格式的
            pixmap = QPixmap.fromImage(img)  # 从QImage生成QPixmap对象
            pixmap = QPixmap(pixmap).scaled(
                self.label_vedio.width(), self.label_vedio.height(),
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.label_vedio.setPixmap(pixmap)  # 在标签上显示图片

            if self.judge(cls):
                print('有人佩戴头盔')
            else:
                print('有人未佩戴头盔')
                if self.which_camera == 0:
                    self.which_camera = 1
                    self.label_image1.setPixmap(pixmap)
                else:
                    self.which_camera = 0
                    self.label_image2.setPixmap(pixmap)
                
