"""
:authors-Int
"""


import setuptools


version = '0.1.7'

long_description = """ Python text-to-speech module (tts) """

setuptools.setup(
    name='textto-speech-python',
    version=version,
    
    author='Int',
    author_email='games.a.matvey@gmail.com',
    
    description=(
        u'Python text-to-speech module (tts)',
        u'Int',
    ),
    long_description=long_description,
    
    url='',
    download_url=''.format(
        version
    ),
    
    license='Apache License, Version 2.0, see LICENSE file',
    
    packages=['textto-speech-python'],
    install_requires=['silero', 'sounddevice'],
    
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ]   
)