music_score - 使用re模块解析曲谱(简谱),winsound模块播放声音的程序。

包含的函数 Functions:

music()::

    使用re模块解析曲谱的生成器
    notation:一段简谱
    duration:一个音符播放的时间

示例代码:

.. code-block:: python

    import music_score,winsound
    # 曲谱
    my_music="123 3 3 345 5 5  54321"
    for freq,duration in music_score.music(my_music,250):
        winsound.Beep(freq,duration)

github上的源程序: https://github.com/qfcy/Python/blob/main/music.py

作者 Author: 七分诚意 qq:3076711200