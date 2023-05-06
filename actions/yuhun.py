"""
作者: YaKun9
最后更新: 2023-2-18 23:18:53
描述: 这里定义了御魂的功能实现
"""

import utils
from loguru import logger


def si_ji():
    "御魂司机"
    images = utils.load_images()
    logger.success("当司机，邀请好友")
    succ_count = 0
    fail_count = 0
    while True:
        screen = utils.screenshot()

        for i in ['yuhun_gd', 'queren_zs', 'queren_yh', 'queren_yh2', 'tiaozhan2', 'zhunbei', 'shibai', 'jiangli',
                  'jixu', 'ying']:
            want = images[i]
            size = want[0].shape
            h, w, ___ = size
            target = screen
            pts = utils.locate(target, want, 0)
            if not len(pts) == 0:
                if i == 'yuhun_gd':
                    logger.warning('御魂已经达到上限，脚本终止，请先清理一下')
                    exit()
                if i == 'shibai':
                    fail_count = fail_count + 1
                if i == 'jiangli':
                    succ_count = succ_count + 1
                if i == 'jixu':
                    xy = utils.get_random_coordinate_for_jixu()
                else:
                    xy = utils.get_random_coordinate(pts[0], w, h - 10)
                utils.click(xy, i)
                utils.random_delay(1.5, 4)
                logger.success(f'挑战次数：{succ_count}，失败次数：{fail_count}')
                break
    return


def da_shou():
    "御魂打手"
    images = utils.load_images()
    logger.success("当打手，被邀请，需要锁定阵容")
    succ_count = 0
    fail_count = 0
    while True:
        screen = utils.screenshot()

        for i in ['yuhun_gd', 'queren_zs', 'queren_yh', 'queren_yh2', 'shibai', 'ying', 'jiangli']:
            want = images[i]
            size = want[0].shape
            h, w, ___ = size
            target = screen
            pts = utils.locate(target, want, 0)
            if not len(pts) == 0:
                if i == 'yuhun_gd':
                    logger.warning('御魂已经达到上限，脚本终止，请先清理一下')
                    exit()
                if i == 'shibai':
                    fail_count = fail_count + 1
                if i == 'jiangli':
                    succ_count = succ_count + 1
                if i == 'jixu':
                    xy = utils.get_random_coordinate_for_jixu()
                else:
                    xy = utils.get_random_coordinate(pts[0], w, h - 10)
                utils.click(xy, i)
                utils.random_delay(1.5, 4)
                logger.success(f'挑战次数：{succ_count}，失败次数：{fail_count}')
                break
    return


def dan_ren():
    "御魂单刷/业原火/日轮之陨"
    images = utils.load_images()
    logger.success(f"当前模式：{dan_ren.__doc__}，无队友，需要锁定阵容")
    succ_count = 0
    fail_count = 0
    while True:
        screen = utils.screenshot()

        # want = images['notili']
        # size = want[0].shape
        # h, w, ___ = size
        # target = screen
        # pts = utils.locate(target, want, 0)
        # if not len(pts) == 0:
        #     logger.success('体力不足')
        #     exit(0)

        for i in ['yuhun_gd', 'tiaozhan', 'shibai', 'jixu', 'jiangli']:
            want = images[i]
            size = want[0].shape
            h, w, ___ = size
            target = screen
            pts = utils.locate(target, want, 0)
            if not len(pts) == 0:
                if i == 'yuhun_gd':
                    logger.warning('御魂已经达到上限，脚本终止，请先清理一下')
                    exit()
                if i == 'shibai':
                    fail_count = fail_count + 1
                if i == 'jiangli':
                    succ_count = succ_count + 1
                if i == 'jixu':
                    xy = utils.get_random_coordinate_for_jixu()
                else:
                    xy = utils.get_random_coordinate(pts[0], w, h - 10)
                utils.click(xy, i)
                utils.random_delay(1.5, 4)
                logger.success(f'挑战次数：{succ_count}，失败次数：{fail_count}')
                break
    return
