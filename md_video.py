"""
Video block for python-markdown

This is aimed to provide best output even without this extension

Title is case insensitive, title is no use, can also be `[video]`.
This is only to avoid the quick reference link

Format:

    [Video: Title of the Video]
    ![poster](http://link.to.poster/link.png)
    [download.mp4](http://link.to.video/file.mp4)
    [download.ogg](http://link.to.video/file.ogv)
    [download.webm](http://link.to.video/file.webm)
    [subtitle.en-US.vtt](http://link.to.subtitle/en_us.vtt "English")
    [subtitle.zh.vtt](http://link.to.subtitle/zh.vtt "Chinese")

Output:

    <video controls="controls" poster="http://link.to.poster/link.png">
      <source src="http://link.to.video/file.mp4" type="video/mp4" />
      <source src="http://link.to.video/file.ogv" type="video/ogg" />
      <source src="http://link.to.video/file.webm" type="video/webm" />
      <track src="http://link.to.subtitle/en_us.vtt" kind="subtitles" srclang="en-US" label="English" default="default" />
      <track src="http://link.to.subtitle/zh.vtt" kind="subtitles" srclang="zh" label="Chinese" />
      Your browser does not support the <code>video</code> element
    </video>

"""

import re
from markdown.util import etree
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
import logging

__version__ = '0.0.3',
__author__ = 'dJabber<dJabber@gmail.com>'

logger = logging.getLogger('MARKDOWN.video')


class VideoProcessor(BlockProcessor):
    HEADER_RE = re.compile(
        r'\[video\]|\[video: .*\]',
        re.IGNORECASE
    )

    LINK_RE = re.compile(
        r'(?P<is_img>\!?)\[(?P<text>.*?)\]'
        r'('
            r'\('
                r'(?P<href>.+)'
            r'\)'
        r'|'
            r'\[(?P<ref>.*?)\]'
        r')'
    )

    def __init__(self, *a, **k):
        self._cross_origin = k.pop('cross_origin', None)
        super(VideoProcessor, self).__init__(*a, **k)

    def test(self, parent, block):
        if not self.HEADER_RE.match(block):
            logger.debug('not match')
            return False

        result = self.result = self.parse(block)

        if result is None:
            logger.debug('not in format')
            return False

        return True

    def run(self, parent, blocks):
        result = getattr(self, 'result', None)
        if result is None:
            result = self.parser(blocks[0])

        blocks.pop(0)

        poster, sources, subtitles = result

        video = etree.SubElement(parent, 'video')
        video.set('controls', 'controls')
        video.set('autoplay', 'autoplay')
        video.set('loop', 'loop')
        video.set('class','md-video')

        cross_origin = self._cross_origin
        if cross_origin is not None:
            video.set('crossorigin', cross_origin)
        video.text = ('Your browser does not support the '
                      '<code>video</code> element')

        if poster:
            video.set('poster', poster)

        for src, type_ in sources:
            source = etree.SubElement(video, 'source')
            source.set('src', src)
            source.set('type', type_)

        for index, (src, lang, label) in enumerate(subtitles):
            track = etree.SubElement(video, 'track')
            track.set('src', src)
            track.set('kind', 'subtitles')
            if lang:
                track.set('srclang', lang)
            if label:
                track.set('label', label)

            if index == 0:
                track.set('default', 'default')


        return True

    def parse(self, block):

        lines = block.splitlines()
        lines.pop(0)
        poster = None
        sources = []  # src, type
        subtitles = []  # src, lang, label

        for line in lines:
            result = self.parse_link(line)
            if result is None:
                logger.debug('line %r not in format', line)
                return None

            # logger.debug(result)

            name, link, title = result

            if name == 'poster':
                poster = link
            elif name.startswith('subtitle'):
                split_name = name.split('.')
                if len(split_name) < 3:
                    logger.debug('subtitle %r not in format', line)
                    return None

                lang_type = split_name[1]
                subtitles.append((link, lang_type, title))
            else:
                split_type = name.split('.')
                if len(split_type) < 2:
                    logger.debug('source %r not in format', line)
                    return None

                type_ = 'video/%s' % split_type[-1]

                sources.append((link, type_))

        return poster, sources, subtitles

    def parse_link(self, md_str):
        match = self.LINK_RE.match(md_str)
        if match is None:
            logger.debug('%r not in format', md_str)
            return None

        group = match.groupdict()

        text = group['text']
        href_mix = group['href']
        if href_mix:
            if group['is_img']:
                sep = href_mix.split(maxsplit=1)
                if len(sep) == 1:
                    href = sep[0]
                    title = None
                else:
                    href, title = sep
            else:
                sep = href_mix.rsplit(maxsplit=1)
                if len(sep) == 1:
                    href = sep[0]
                    title = None
                else:
                    href, title = sep
                    if not title or len(title) < 2:
                        href = href_mix
                    else:
                        if title[0] == title[-1] and title[0] in '\'"':
                            title = title[1:-1]
                        else:
                            href = href_mix

                if href.startswith('<') and href.endswith('>'):
                    href = href[1:-1]

        else:
            ref = group['ref']
            if ref is None or ref not in self.parser.markdown.references:
                logger.debug('ref %r not found', ref)
                return None

            href, title = self.parser.markdown.references[ref]

        return text, href, title

class VideoExtension(Extension):
    """ Add definition lists to Markdown. """

    def __init__(self, **configs):
        self.config = {'crossorigin':
                        [configs.get('crossorigin', None), 'cross origin']}
        super(VideoExtension, self).__init__(**configs)

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of DefListProcessor to BlockParser. """
        cross_origin = self.getConfig('crossorigin', None)
        md.parser.blockprocessors.add('video',
                                      VideoProcessor(
                                        md.parser,
                                        cross_origin=cross_origin),
                                      '>empty')
def makeExtension(**configs):
    return VideoExtension(**configs)


if __name__ == '__main__':
    import markdown
    logging.basicConfig(
        level=logging.DEBUG,
        format='\033[32m%(levelname)1.1s\033[0m[%(lineno)3s]%(message)s')

    md = """
[Video: Title of the Video]
![poster](http://link.to.poster/link.png)
[download.mp4](http://link.to.video/fil e.mp4)
[download.ogg](http://link.to.video/fil e.ogv)
[download.webm](http://link.to.video/fil e.webm)
[subtitle.en-US.vtt](http://link.to.sub title/en_us.vtt "English")
[subtitle.zh.vtt](http://link.to.subtit le/zh.vtt "Chinese")
"""

    result = markdown.markdown(md,
                               extensions=[
                                makeExtension(crossorigin="anonymous")])
    print(result)
