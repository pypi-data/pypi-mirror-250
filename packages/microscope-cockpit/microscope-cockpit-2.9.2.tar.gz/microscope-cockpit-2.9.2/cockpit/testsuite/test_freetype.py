#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright (C) 2021 University of Oxford
##
## This file is part of Cockpit.
##
## Cockpit is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Cockpit is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Cockpit.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import cockpit.gui.freetype
from cockpit.testsuite.test_gui import WxTestCase


class FaceTestCase(WxTestCase):
    def setUp(self):
        super().setUp()
        self.face = cockpit.gui.freetype.Face(self.frame, 18)

    def test_render(self):
        ## Not sure how to actual test if it gets rendered, but this
        ## should at least not error.
        self.face.render('foobar')
