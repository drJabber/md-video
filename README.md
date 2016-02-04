md-video
========

video block(tag) extension for Python-Markdown

Install
-------

```bash
pip install -U git+git://github.com/TylerTemp/md-video.git
```

Usage
-----

```python
import markdown
import md_video

md = """
[Video: Title of the Video]
![poster](http://link.to.poster/link.png)
[download.mp4](http://link.to.video/file.mp4)
[download.ogg](http://link.to.video/file.ogv)
[download.webm](http://link.to.video/file.webm)
[subtitle.en-US.vtt](http://link.to.subtitle/en_us.vtt "English")
[subtitle.zh.vtt](http://link.to.subtitle/zh.vtt "Chinese")
"""

html = markdown.markdown(md, extensions=[makeExtension()])
print(html)
# <video controls="controls" poster="http://link.to.poster/link.png">Your browser does not support the <code>video</code> element<source src="http://link.to.video/file.mp4" type="video/mp4"></source><source src="http://link.to.video/file.ogv" type="video/ogg"></source><source src="http://link.to.video/file.webm" type="video/webm"></source><track default="default" kind="subtitles" label="English" src="http://link.to.subtitle/en_us.vtt" srclang="en-US"></track><track kind="subtitles" label="Chinese" src="http://link.to.subtitle/zh.vtt" srclang="zh"></track></video>
```

Note `poster` and `subtitle.` should not be changed

`poster` and `subtitle` is optional

