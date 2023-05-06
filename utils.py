import random
import time
import cv2
import os
import win32gui
import win32ui
import win32api
import win32con
import numpy
import mss
from loguru import logger

gl_window_handle = 0
gl_images = None
gl_client_mode = 0
"客户端类型 1=桌面版，2=模拟器"


def get_window_handle(window_title, retryDelay=2):
    """ 
    获取指定窗口的句柄
    :param window_title: 待查找的窗口标题
    :param retryDelay: 窗口不存在时的重试等待时间
    """
    global gl_window_handle
    if (gl_window_handle > 0):
        return gl_window_handle

    gl_window_handle = win32gui.FindWindow(None, window_title)
    while gl_window_handle == 0:
        logger.success(f"等待窗口 {window_title} 出现...")
        time.sleep(retryDelay)
        gl_window_handle = win32gui.FindWindow(None, window_title)
    return gl_window_handle


def click(xy, tag=""):
    """
    发送鼠标点击事件，模拟人类点击，按下到抬起在0.1-0.3秒之间随机
    :param xy: 点击坐标
    :param tag: 点击的标签，主要用于展示坐标来源图片
    """
    x, y = xy
    x = int(x)
    y = int(y)
    global gl_window_handle
    # 发送鼠标左键按下消息
    win32api.PostMessage(gl_window_handle, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
    random_delay(0.1, 0.3, False)
    # 发送鼠标左键弹起消息
    win32api.PostMessage(
        gl_window_handle, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y))

    logger.debug(f'点击{tag}坐标 {x}:{y}')
    return


def get_random_coordinate(img_point, img_width, img_height):
    """
    获取在指定图片范围内的随机坐标
    :param img_x: 图片原始坐标 x 坐标
    :param img_y: 图片原始坐标 y 坐标
    :param img_width: 图片宽度
    :param img_height: 图片高度
    :return: 随机坐标 (x, y)
    """

    img_x, img_y = img_point
    a = int(img_width / 3)
    b = int(img_height / 3)

    c = random.randint(-a, a)
    d = random.randint(-b, b)

    img_x = img_x + c
    img_y = img_y + d

    return img_x, img_y


def get_random_coordinate_for_jixu():
    "获取随机坐标，针对获取到的图片为jixu的情况，继续是可以点击全屏的，所以随机性大一点更安全"
    global gl_window_handle
    # 获取窗口的位置和尺寸
    left, top, right, bottom = win32gui.GetWindowRect(gl_window_handle)

    # 点击多个随机区域
    areas = [
        # 右侧区域
        [right - 230, top + 200, right - 30, bottom - 100],
    ]
    if (len(areas) > 1):
        index = 0
    else:
        index = random.randint(0, len(areas) - 1)
    area = areas[index]
    x = random.uniform(area[0], area[2])
    y = random.uniform(area[1], area[3])
    return x, y


def random_delay(min_delay=0.5, max_delay=10, print_log=False):
    """
    获取一个随机延迟时间（秒）
    :param min_delay: 最小延迟时间
    :param max_delay: 最大延迟时间
    :param print_log: 是否打印日志
    """
    delay = round(random.uniform(min_delay, max_delay), 2)
    if print_log:
        logger.debug(f'随机延迟 {delay} 秒')
    time.sleep(delay)


def load_images():
    """
    加载指定路径下的所有图片，并将它们存储在一个字典中，键是图片名称，值是包含图像和精度的列表。
    """
    global gl_images
    global gl_client_mode
    if (gl_images != None):
        return gl_images
    gl_images = {}
    # 拼接图片路径
    if gl_client_mode == 1:
        img_dir = 'imgs'
    elif gl_client_mode == 2:
        img_dir = 'imgs_mnq'
    else:
        logger.error('客户端模式初始化错误')
        exit()

    path = os.path.join(os.getcwd(), img_dir)
    # 获取所有文件
    file_list = os.listdir(path)
    for file in file_list:
        name = file.split('.')[0]
        file_path = path + '/' + file
        a = [cv2.imread(file_path), 0.95, name]
        gl_images[name] = a
    return gl_images


def screenshot(mode='win32'):
    """
    截图游戏窗口
    :param mode: 截图模式，win32 或 mss。win32 模式下窗口可以被遮挡；mss 模式下窗口不可以被遮挡。
    """
    # 测试结果大概分别在0.005和0.017秒识别结束，过快的识别完全没必要，小限制一下
    # time.sleep(0.2)
    if mode == 'win32':
        return screenshot_win32()
    else:
        return screenshot_mss()


def screenshot_mss():
    """
    截图游戏窗口，窗口不可以被遮挡（mss）
    """

    global gl_window_handle
    # 获取窗口的位置和尺寸
    try:
        window_rect = win32gui.GetWindowRect(gl_window_handle)
    except:
        logger.error('找不到窗口，窗口似乎已经关闭')
        exit()
    # 计算窗口的宽度和高度
    width = window_rect[2] - window_rect[0]
    height = window_rect[3] - window_rect[1]

    # 截图并处理
    sct = mss.mss()
    screenshot = sct.grab(
        {"left": window_rect[0], "top": window_rect[1], "width": width, "height": height})

    im = numpy.array(screenshot)
    screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
    return screen


def screenshot_win32():
    """截图指定窗口，窗口可以被遮挡，但不可最小化（pywin32）
    """
    global gl_window_handle
    hWnd = gl_window_handle

    # 获取句柄窗口的大小信息
    try:
        left, top, right, bot = win32gui.GetWindowRect(hWnd)
    except:
        logger.error('找不到窗口，窗口似乎已经关闭')
        exit()

    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # 获取位图信息
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd, hWndDC)
    # 生成图像
    img = numpy.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    # 将 BGRA 格式转换为 BGR 格式
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img



def locate(target, want, show=bool(0), msg=bool(0)):
    """在背景查找目标图片，并返回查找到的结果坐标列表，target是背景，want是要找目标
    """
    loc_pos = []
    want, accuracy, c_name = want[0], want[1], want[2]
    result = cv2.matchTemplate(target, want, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= accuracy)

    h, w = want.shape[:-1]

    n, ex, ey = 1, 0, 0
    for pt in zip(*location[::-1]):  # 其实这里经常是空的
        x, y = pt[0] + int(w / 2), pt[1] + int(h / 2)
        if (x - ex) + (y - ey) < 15:  # 去掉邻近重复的点
            continue
        ex, ey = x, y

        cv2.circle(target, (x, y), 10, (0, 0, 255), 3)

        x, y = int(x), int(y)

        loc_pos.append([x, y])

    if show:  # 在图上显示寻找的结果，调试时开启
        logger.debug('show action.locate')
        cv2.imshow('we get', target)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if len(loc_pos) == 0:
        pass
    # else:
    # logger.debug(f'找到图片 :{c_name} {loc_pos[0]}')

    return loc_pos


def reset_window_size():
    "重置游戏窗口大小到默认尺寸，其后需再次启动脚本"
    global gl_window_handle
    win32gui.MoveWindow(gl_window_handle, 0, 0, 1136, 640, True)
    logger.success('窗口大小已重置')
    return
