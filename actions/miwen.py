"""
作者: YaKun9
最后更新: 2023-2-19 19:03:14
描述: 这里定义了秘闻副本的功能实现
"""

import utils
from loguru import logger


def common():
    "秘闻副本-通用挂机"
    images = utils.load_images()
    logger.success("秘闻副本-通用挂机")
    utils.random_delay(0.1, 0.1, False)
    try:
        input_value = input("需要打几关？")
        count = int(input_value)
    except:
        print('请输入数字 1~10 之间的值')
        common()

    if count > 11 or count < 1:
        print('请输入数字 1~11 之间的值')
        common()
    logger.success(f'开始挑战秘闻副本，剩余{count}关')
    succ_count = 0
    fail_count = 0
    while count > 0:
        screen = utils.screenshot()
        for i in ['tiaozhan_mw', 'zhunbei', 'shibai', 'ying', 'jiangli']:
            want = images[i]
            size = want[0].shape
            h, w, ___ = size
            target = screen
            pts = utils.locate(target, want, 0)
            if not len(pts) == 0:
                if i == 'shibai':
                    fail_count = fail_count + 1
                    if fail_count >= 3:
                        logger.success(f'挑战失败，已重试{fail_count}次，脚本自动终止，请调整阵容后重试')
                        exit()
                    else:
                        logger.success(f'挑战失败，已重试{fail_count}次，将继续重试')
                if i == 'ying':
                    fail_count = 0
                    succ_count = succ_count + 1
                    count = count - 1
                xy = utils.get_random_coordinate(pts[0], w, h - 10)
                utils.click(xy, i)
                utils.random_delay(1.5, 4)
                logger.success(f'挑战次数：{succ_count}，剩余次数{count}')
                break
    return
