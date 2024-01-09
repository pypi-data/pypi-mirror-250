# -*- coding: utf-8 -*-
# :Project:   PatchDB -- Patch tests
# :Created:   mer 24 feb 2016 16:44:43 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2023 Lele Gaifax
#

import pytest
import fixtures


def test_patch():
    from metapensiero.sphinx.patchdb.manager import PatchManager
    from metapensiero.sphinx.patchdb.patch import make_patch, parse_deps, DependencyError

    pm = PatchManager()
    first = make_patch('first', 'script',
                       dict(revision=1, language='test',
                            depends='second',
                            preceeds='third'))
    pm['first'] = first

    # __str__
    second = make_patch('second', 'script',
                        dict(revision=2, language='test'))
    pm['second'] = second
    assert str(second) == 'script "second@2"'

    third = make_patch('third', 'script',
                       dict(depends='second@1',
                            brings='second@2',
                            preceeds='fourth@2',
                            language='test'))
    pm['third'] = third
    assert str(third) == 'patch "third@1"'

    fourth = make_patch('fourth', 'script',
                        dict(depends='unknown'))
    pm['fourth'] = fourth

    # adjustUnspecifiedRevisions
    context = {}
    first = pm['first']
    assert first.depends == [('second', None)]
    assert first.preceeds == [('third', None)]
    first.adjustUnspecifiedRevisions(pm, context)
    assert first.depends == [('second', 2)]
    assert first.preceeds == [('third', 1)]
    third = pm['third']
    assert third.preceeds == [('fourth', 2)]
    third.adjustUnspecifiedRevisions(pm, context)

    try:
        fourth.adjustUnspecifiedRevisions(pm, context)
    except DependencyError as e:
        assert 'script "fourth@1"' in str(e)
        assert 'depends on non existing "unknown@None"' in str(e)
    else:
        assert False, "should raise a DependencyError"

    fifth = make_patch('fifth', 'script',
                       dict(depends="second@*"))
    pm['fifth'] = fifth

    context = {'second': 1}
    fifth.adjustUnspecifiedRevisions(pm, context)
    assert fifth.depends == [('second', 1)]

    # parse_deps
    assert parse_deps('patchid@10') == [('patchid', 10)]
    assert parse_deps('patchid@10, other') == [('other', None), ('patchid', 10)]
    assert (parse_deps(' z, x , y@10 , a,c') ==
            [('a', None), ('c', None), ('x', None), ('y', 10), ('z', None)])

    with pytest.raises(ValueError):
        make_patch('invalid', 'script', dict(brings="second@*"))

    with pytest.raises(ValueError):
        make_patch('invalid', 'script', dict(drops="second@*"))

    with pytest.raises(ValueError):
        make_patch('invalid', 'script', dict(preceeds="second@*"))


class TestPatchNonExistingDepends(fixtures.BaseTestCase):
    TEST_TXT = """
    New table, replacing old table
    ==============================

    .. patchdb:script:: Create new_table

       create table new_table (
         id integer primary key,
         value varchar(10)
       )

    .. patchdb:script:: Replace old_table with new_table
       :depends: Create old_table
       :brings: Create new_table

       create table new_table (
         id integer primary key,
         value varchar(10)
       )
       ;;
       drop table old_table
    """

    def test(self):
        super().test()
        self.assertIn('depends on an unknown script "create old_table"', self.build_warning)
