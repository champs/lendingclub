#!/usr/bin/env python

from distutils.core import setup

setup(name='LendingClub',
      version=open('lendingclub/VERSION').read(),
      description='Unofficial LendingClub SDK',
      author='Peerakit (Champ) Somsuk',
      author_email='pk.somsuk@gmail.com',
      url='https://github.com/champs/lendingclub',
      packages=['lendingclub'],
      license=open('LICENSE').read(),
     )