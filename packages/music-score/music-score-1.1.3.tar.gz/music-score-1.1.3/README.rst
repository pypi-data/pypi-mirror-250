music_score - ʹ��reģ���������(����),winsoundģ�鲥�������ĳ���

�����ĺ��� Functions:

music()::

    ʹ��reģ��������׵�������
    notation:һ�μ���
    duration:һ���������ŵ�ʱ��

ʾ������:

.. code-block:: python

    import music_score,winsound
    # ����
    my_music="123 3 3 345 5 5  54321"
    for freq,duration in music_score.music(my_music,250):
        winsound.Beep(freq,duration)

github�ϵ�Դ����: https://github.com/qfcy/Python/blob/main/music.py

���� Author: �߷ֳ��� qq:3076711200