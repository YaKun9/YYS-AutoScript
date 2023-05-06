## 项目已停止维护，因为做了GUI版的
# YYS-AutoScript

### 依赖环境安装

1. 安装`python 3.10`

    1. 手动下载安装：https://www.python.org/downloads/release/python-31010/ ，在最下面选择适合自己系统的版本，一般选[64位安装包](https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe)，一路下一步即可。
    2. 应用商店安装（win10/11），在应用商店搜索python，安装3.10版本即可。

2. 安装依赖包，打开命令行工具，执行以下命令：

    ```
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

### 脚本使用

1. 在项目根目录下打开命令行工具
2. 输入命令`python main.py` 
3. 按提示选择功能享用

### 构建打包

```
Pyinstaller --onefile --add-data "imgs/*;imgs/" --name liberate main.py 
```



### 功能列表

- [x] 御魂单刷/业原火/日轮之陨
- [x] 御魂司机
- [x] 御魂打手
- [x] 秘闻副本





### 使用说明

1. **所有功能都需要手动开启加成；挑战次数计算仅供参考，并不一定准确；桌面版使用默认分辨率（1136x640），安卓模拟器使用1280x720，DPI 240**
2. 御魂单刷/业原火/日轮之陨 等功能，需要手动到挑战界面锁定好阵容之后启动
3. 御魂司机需要手动打一局，然后默认继续邀请队友之后，回到组队页面时启动，脚本暂时不会自动邀请好友
4. 御魂打手可以直接开启，会自动接受


### 参考项目
[YYS https://github.com/lisai9093/YYS](https://github.com/lisai9093/YYS)
