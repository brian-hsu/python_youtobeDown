import os
import re
from pytube import YouTube as yt
from ffmpy import FFmpeg as ff
from pytube.exceptions import RegexMatchError as reME
from pytube.helpers import safe_filename

yt_url = input(u"複製 youtube 網址 並右鍵貼上:")


def go_pytube():
    try:
        go_yt = yt(yt_url)
        name = safe_filename(go_yt.title)
        print(u'名稱:', name)
        return go_yt, name
    except reME:
        print(u'不正常的網址...')
        e = input(u'按下 Enter按鍵 離開')
        exit()


go_yt = go_pytube()
stream = go_yt[0].streams.filter(video_codec='', audio_codec='').first()
str_stream = str(stream)
stream_type = re.sub(
            r".*mime_type=\".*/(.*)\" res=.*",
            r"\1",
            str_stream
)

to_mp3 = input(u"如需要轉 mp3 檔, 打上 \"y\":")
to_mpeg = input(u"如需要轉 mpeg 檔, 打上 \"y\":")
save_mp4 = input(u"如需要保留原 mp4 檔, 打上 \"y\":")

print(u"開始下載... %s.%s" % (go_yt[1], stream_type))

# stream.download(filename='1_~23')
stream.download()

file_path = os.getcwd() + '\\' + go_yt[1] + '.' + stream_type

ff_file = os.getcwd() + "\\ffmpeg.exe"
if to_mp3 == 'y':
    tomp3 = ff(
        executable=ff_file,
        # inputs={os.getcwd() + '\\' + dl.title + '.mp4': None},
        inputs={file_path: '-y '},
        # outputs={os.getcwd() + '\\' + dl.title + '.mp3': '-ab 320k'}
        outputs={os.getcwd() + '\\' + go_yt[1] + '.mp3': '-ab 192k'}
    )
    # print(tomp3.cmd)
    print(u'%s.%s 轉mp3' % (go_yt[1], stream_type))
    tomp3.run()

if to_mpeg == 'y':
    tompeg = ff(
        # executable=(r"D:\ffmpeg-20180619\bin\ffmpeg.exe"),
        executable=ff_file,
        # inputs={os.getcwd() + '\\' + dl.title + '.mp4': None},
        inputs={file_path: '-y '},
        # outputs={os.getcwd() + '\\' + dl.title + '.mp3': '-ab 320k'}
        outputs={os.getcwd() + '\\' + go_yt[1] + '.mpeg': '-ac 2'}
    )
    # print(tompeg.cmd)
    print(u'%s.%s 轉mpeg' % (go_yt[1], stream_type))
    tompeg.run()

if (save_mp4 != 'y') and (to_mpeg == 'y'):
    os.remove(file_path)

e = input(u'按下 Enter按鍵 離開')
exit()
