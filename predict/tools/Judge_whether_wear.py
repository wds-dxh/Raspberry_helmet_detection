from typing import Any
import cv2

class Judge_whether_wear:
    def __init__(self):
        print('初始化，判断是否佩戴头盔')
        pass
    def __call__(self, cls) -> Any:
        #如果有类别0就是有人，有2-5就是有头盔
        #当有0的时候没有2-5就是没有佩戴头盔
        for i in cls:
            if i == 0:
                if 2 in cls or 3 in cls or 4 in cls or 5 in cls:
                    return True
                else:
                    return False