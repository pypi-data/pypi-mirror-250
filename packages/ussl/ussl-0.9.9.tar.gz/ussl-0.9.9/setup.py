#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='ussl',
    description='USSC SOAR SCRIPT LIB',
    author='ussc soc dev team',
    author_email='pbikkuzhina@ussc.ru',
    long_description='Пакет был разработан командой разработчиков USSC-SOC для \
упрощения взаимодействия с АРМ, серверами и сетевыми устройствами',
    version='0.9.9',
    packages=[
        'ussl',
        'ussl.model',
        'ussl.postprocessing',
        'ussl.protocol',
        'ussl.transport',
        'ussl.utils',
        'ussl.KSC',
        'ussl.KSC.KlAkOAPI',
        ],
    install_requires=[
        'pywinrm ==0.4.1',
        'paramiko ==2.7.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ]
)
