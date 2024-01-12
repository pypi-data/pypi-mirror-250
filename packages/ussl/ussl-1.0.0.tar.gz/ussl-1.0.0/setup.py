#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('description.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ussl',
    author='ussc soc dev team',
    author_email='iushangaraev@ussc.ru, pbikkuzhina@ussc.ru',
    description='Пакет разработчиков USSC-SOC для упрощения взаимодействия с АРМ, серверами и сетевыми устройствами',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.0',
    packages=[
        'ussl',
        'ussl.model',
        'ussl.postprocessing',
        'ussl.protocol',
        'ussl.transport',
        'ussl.utils',
        ],
    install_requires=[
        'pywinrm ==0.4.1',
        'paramiko ==2.7.2',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8'
    ]
)
