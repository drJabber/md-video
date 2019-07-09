from setuptools import setup
import os
import sys

if sys.version_info[0] < 3:
    from codecs import open

with open(os.path.join(os.path.dirname(__file__), 'README.md'),
          'r', encoding='utf-8') as f:
    long_description = f.read()
    try:
        import pypandoc
        long_description = pypandoc.convert(
                long_description, 'rst', format='md')
    except BaseException as e:
        print(("DEBUG: README in Markdown format. It's OK if you're only "
               "installing this program. (%s)") % e)

setup(
    name='md_video',
    py_modules=['md_video'],
    package_data={
        '': [
            'README.md',
            'LICENSE',
        ]
    },
    version='0.0.3',
    author='dJabber',
    author_email='dJabber@gmail.com',
    url='https://github.com/drJabber/md-video',
    download_url='http://github.com/drJabber/md-video/zipball/addition/',
    license='MIT',
    description='Markdown Video Block',
    keywords='markdown video',
    long_description=long_description,
    install_requires=[
        'markdown'
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
)
