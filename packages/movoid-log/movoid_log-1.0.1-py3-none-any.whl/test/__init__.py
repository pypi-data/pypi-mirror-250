#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : __init__.py
# Author        : Sun YiFan-Movoid
# Time          : 2024/1/11 23:25
# Description   : 
"""
import pathlib

a = pathlib.Path('pathlib.png').resolve()
print(a.stat().st_ctime)
print(a.suffix, a.suffixes, a.stem)
b = a.parent / a.stem
c = str(b) + '.log'
print(b)
print(c)
# print(a.resolve().mkdir(parents=True,exist_ok=True))

if __name__ == '__main__':
    pass
