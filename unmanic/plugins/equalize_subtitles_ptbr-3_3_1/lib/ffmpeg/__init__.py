#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic.__init__.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     30 Jul 2021, (12:12 PM)

    Copyright:
        Copyright (C) 2021 Josh Sunnex

        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
        Public License as published by the Free Software Foundation, version 3.

        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
        for more details.

        You should have received a copy of the GNU General Public License along with this program.
        If not, see <https://www.gnu.org/licenses/>.

"""

from __future__ import absolute_import
import warnings

from .parser import Parser
from .probe import Probe
from .stream_mapper import StreamMapper

__author__ = 'Josh.5 (jsunnex@gmail.com)'

__all__ = (
    'Parser',
    'Probe',
    'StreamMapper',
)
