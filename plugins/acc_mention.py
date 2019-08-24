#!/Users/rikutakada/.pyenv/shims python
# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
from logger import getLog, subLog


@respond_to('fund')
def fund(message):
    with open('fund.txt', 'r') as f:
        replys(message, int(f.readline()))
        replys(message, ':sob:')


@respond_to('getlog(.*)')
def getlog(message, something):
    log = getLog().items()
    rpstring = '\n'
    if something.lstrip().isdigit():
        start = len(log) - int(something.lstrip())
    else:
        if len(something.lstrip()) > 0:
            message.reply('行数を認識できませんでした。\nすべて表示します')
        start = 0
    for tup in [(k, v) for k, v in sorted(log)][start:]:
        if int(tup[1][0]) >= 0:
            rpstring += '+ {0}\t{1}円\n\t備考：{2}\n\n'.format(tup[0], tup[1][0], tup[1][1])
        else:
            rpstring += '- {0}\t{1}円\n\t備考：{2}\n\n'.format(tup[0], tup[1][0], tup[1][1])
    message.reply(rpstring)


@respond_to('add (.*)')
def adds(message, something):
    a = something.split(' ', 1)
    if not a[0].replace('-', '').isdigit():
        message.reply('失敗しました')
        return
    if len(a) > 1:
        subLog(sub=a[0], memo=a[1])
    else:
        subLog(sub=a[0])
    with open('fund.txt', 'r') as f:
        tas = int(f.readline())
    with open('fund.txt', 'w') as f:
        tas += int(a[0])
        f.write(str(tas))
        replys(message, tas)


def replys(message, num):
    message.reply('残金は ' + str(num) + '円です')
