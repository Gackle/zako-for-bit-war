# Zako For Bit War

此项目是 **比特大战** 的在线平台，主要使用 Python 3 + Flask + Semantic UI + MySQL 实现。

其中项目包含了一个内置的 Zako 语言解释器，主要使用 Python 的 Ply 库实现词法分析、抽象语法树生成以及语义分析。

## 如何运行

1. 使用 pip 安装依赖

    ``` shell
    pip install -r requirements.txt
    ```

2. (可选)添加预置数据

    ``` shell
    python manage.py setup
    ```

3. 运行开发服务器

    ``` shell
    python manage.py server
    ```

## 关于 **比特大战**

**比特大战** 的构想来自于《自私的基因》一书，博弈双方可以根据各自定义的策略在每一回合选择 *合作* 与 *背叛* ，回合的博弈结果以得分的形式累计，在足够长的回合之后，得分较高的一方为博弈的胜者。

## 关于 Zako

Zako 语言的名字来自于项目最初的合作人 Zack 和 Gakho 的缩写，是一门用于给对战方实现自己策略的语言。平台提供了 Zako 语言的手册，以及 *.sg* 文件的托管与运行（即策略对战模拟）。