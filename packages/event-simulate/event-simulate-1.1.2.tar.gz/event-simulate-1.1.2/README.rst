ģ������: event (����ʹ��import event_simulate) !

���
====

event-simulate��һ��ģ�����,����¼���Python��, ����ģ����굥����˫��, ���̰��µȸ��ֲ���,

�����PyInstaller��exe�ļ�ʱ���С�ɡ������ڱ�д�Զ������� (����Ϸ��ҵ�)��


������ģ�� Included modules: 
============================

event.key - ģ������¼�
""""""""""""""""""""""""
�����ĺ��� Functions:

keydown(keycode_or_keyname)::

    ģ������¡�
    keycode_or_keyname:�������ƻ�ð����ļ���ֵ

keypress(keycode_or_keyname, delay=0.05)::

    ģ�ⰴ����
    keycode_or_keyname:�������ƻ�ð����ļ���ֵ
    delay:���������ͷ�֮��ĵļ��ʱ��,���ʱ��ԽС,�����ٶ�Խ�졣

keyup(keycode_or_keyname)::

    ģ����ͷš�
    keycode_or_keyname:�������ƻ�ð����ļ���ֵ


event.mouse - ģ������¼�
""""""""""""""""""""""""""
�����ĺ��� Functions:

click()::

    ģ������������

dblclick(delay=0.25)::

    ģ��������˫��

get_screensize()::

    ��ȡ��ǰ��Ļ�ֱ��ʡ�

getpos()::

    ��ȡ��ǰ���λ�á�
    ����ֵΪһ��Ԫ��,��(x,y)��ʽ��ʾ��

move(x, y)::

    ģ���ƶ���ꡣ
    ��goto��ͬ,move()����һ������¼���

right_click()::

    ģ������Ҽ�������

wheel(delta)::

    ģ����������֡�
	delta: �����ľ���, ��ֵΪ���Ϲ���, ��ֵΪ���¹�����

����: leftdown(),leftup(),rightdown(),rightup(),middledown(),middleup()ģ����갴�º��ͷš�



ʾ������1:

.. code-block:: python

    #ģ�ⰴ��Alt+F4�رյ�ǰ����
    from event.key import *
    keydown("Alt")
    keydown("f4")
    keyup("f4")
    keyup("alt")


ʾ������2:

.. code-block:: python

    #ʹ��Aero PeekԤ�����档(Win7������ϵͳ)
    from event import mouse
    x,y=mouse.get_screensize()
    mouse.move(x,y) #�����������Ļ���½�
    mouse.click() #ģ�������


�������� New Features: 

1.1.2: event.keyģ�������˰�����, ����PyWinHook�⡣������ʾ��:¼�Ƽ����¼�(��Ŀ¼\\examples\\¼�Ƽ����¼�.py)

˵��: ʹ��ʾ��"¼�Ƽ����¼�.py" �谲װpywinhook�⡣

1.0.3:�޸��˵���API����ʱ���� ``ValueError`` ��bug��

1.0.2:������ʾ��:��������(��Ŀ¼\\examples\\mouseController.py)

Դ���� Source: https://github.com/qfcy/Python/tree/main/event

���� Author:

qfcy qq:3076711200 �ٶ������˺�:qfcy\_

����CSDN��ҳ: https://blog.csdn.net/qfcy\_/