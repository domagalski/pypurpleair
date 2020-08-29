#!/usr/bin/env python3

import glob
from distutils.core import setup

pkg_name = "pypurpleair"
setup(
    name=pkg_name,
    version="0.1.3",
    description="Simple API for reading PurpleAir sensors.",
    author="Rachel Simone Domagalski",
    license="GPL",
    packages=[pkg_name],
    scripts=glob.glob("scripts/*"),
)
