"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import sys, os

APP = ['main.py']
DATA_FILES = ['fonts', 'levels', 'sprites', 'tiles', 'pygame', 'ext_opt']
OPTIONS = {
'argv_emulation': False,
"compressed" : True,
"optimize":2 }

sys.path.insert(0, os.path.join(os.getcwd(), 'lib', 'python2.7','lib-dynload')) ## Added to fix dynlib bug

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
