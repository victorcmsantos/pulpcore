# -*- coding: utf-8 -*-
#
# Copyright © 2013 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import functools
import unittest

from pulp.plugins.model import Unit


unit_key_factory = functools.partial(dict, a='foo', b='bar', c=3)
unit_factory = functools.partial(Unit, 'my_type', unit_key_factory(), {}, '')


class TestUnit(unittest.TestCase):
    def test_hashequality(self):
        unit1 = unit_factory()
        unit2 = unit_factory()
        self.assertEqual(hash(unit1), hash(unit2))

    def test_hash_inequality(self):
        unit1 = unit_factory()
        unit2 = unit_factory()
        unit2.unit_key = unit_key_factory(a='xyz')
        self.assertNotEqual(hash(unit1), hash(unit2))

    def test_equal_unit_key_instances(self):
        unit1 = unit_factory()
        unit2 = unit_factory()
        # give unit2 a new instance of unit_key
        unit2.unit_key = unit_key_factory()
        self.assertEqual(hash(unit1), hash(unit2))

    def test_type_in_hash(self):
        unit1 = unit_factory()
        unit2 = unit_factory()
        unit2.type_id = 'xyz'
        self.assertNotEqual(hash(unit1), hash(unit2))

    def test_metadata_not_in_hash(self):
        unit1 = unit_factory()
        unit2 = unit_factory()
        unit2.metadata = {'a':'foo'}
        self.assertEqual(hash(unit1), hash(unit2))

    def test_path_not_in_hash(self):
        unit1 = unit_factory()
        unit2 = unit_factory()
        unit2.storage_path = '/foo/bar'
        self.assertEqual(hash(unit1), hash(unit2))
