import actions.yuhun as yuhun
import actions.miwen as miwen
import win32api
import win32con
import win32gui
import utils
from loguru import logger


def main():
    # 通过窗口标题查找句柄
    handle = utils.get_window_handle("阴阳师-网易游戏")
    #handle = utils.get_window_handle("雷电模拟器")
    x, y, x2, y2 = win32gui.GetWindowRect(handle)

    logger.info(f"位置: ({x}, {y}), 大小: ({x2 - x}, {y2 - y})")
    select_mode()
    return


def select_mode():
    """
    选择游戏模式
    """
    # client_input = input("选择客户端：1=桌面版，2=模拟器")
    # try:
    #     client = int(client_input)
    # except:
    #     logger.success('请输入数字')
    #     select_mode()
    # if client not in [1, 2]:
    #     logger.error('请正确输入要选择的客户端：1=桌面版，2=模拟器')

    utils.gl_client_mode = 1
    utils.gl_images = None

    print('功能菜单：\n'
          f'1 {utils.reset_window_size.__doc__}\n'
          f'2 {yuhun.dan_ren.__doc__}\n'
          f'3 {yuhun.si_ji.__doc__}\n'
          f'4 {yuhun.da_shou.__doc__}\n'
          f'5 {miwen.common.__doc__}\n')
    mode = input("选择功能模式：")
    try:
        index = int(mode)
    except:
        logger.error('请输入数字')
        select_mode()

    modes = [quit, utils.reset_window_size, yuhun.dan_ren, yuhun.si_ji, yuhun.da_shou, miwen.common]
    try:
        command = modes[index]
    except:
        logger.error('数字超出范围')
        select_mode()

    if (index == 0):
        quit(0)
    else:
        logger.success(f'启动功能：【{command.__doc__}】')
        command()
        select_mode()
    return


if __name__ == '__main__':
    main()
