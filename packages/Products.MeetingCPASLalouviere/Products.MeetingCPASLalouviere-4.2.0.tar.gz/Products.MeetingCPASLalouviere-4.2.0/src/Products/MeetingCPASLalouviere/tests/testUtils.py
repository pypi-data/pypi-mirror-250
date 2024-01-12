# -*- coding: utf-8 -*-
#
# File: testUtils.py
#
# Copyright (c) 2017 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.MeetingCPASLalouviere.tests.MeetingCPASLalouviereTestCase import MeetingCPASLalouviereTestCase
from Products.MeetingCommunes.tests.testUtils import testUtils as mctu


class testUtils(MeetingCPASLalouviereTestCase, mctu):
    ''' '''

    def _default_permission_mail_recipents(self):
        return [u'M. Budget Impact Editor <budgetimpacteditor@plonemeeting.org>',
                u'M. PMCreator One <pmcreator1@plonemeeting.org>',
                u'M. PMCreator One bee <pmcreator1b@plonemeeting.org>',
                u'M. PMObserver One <pmobserver1@plonemeeting.org>',
                u'M. PMReviewer Level One <pmreviewerlevel1@plonemeeting.org>',
                u'M. PMReviewer Level Two <pmreviewerlevel2@plonemeeting.org>',
                u'M. PMReviewer One <pmreviewer1@plonemeeting.org>',
                u'M. Power Observer1 <powerobserver1@plonemeeting.org>',
                u'Site administrator <siteadmin@plonemeeting.org>',
                u'pmN1 <user@plonemeeting.org>',
                u'pmN2 <user@plonemeeting.org>',
                u'pmPresident <user@plonemeeting.org>',
                u'pmSecretaire <user@plonemeeting.org>']

    def _modify_permission_mail_recipents(self):
        return [u'M. PMCreator One <pmcreator1@plonemeeting.org>',
                u'M. PMCreator One bee <pmcreator1b@plonemeeting.org>',
                u'M. PMReviewer Level One <pmreviewerlevel1@plonemeeting.org>',
                u'M. PMReviewer Level Two <pmreviewerlevel2@plonemeeting.org>',
                u'M. PMReviewer One <pmreviewer1@plonemeeting.org>',
                u'Site administrator <siteadmin@plonemeeting.org>',
                u'pmN1 <user@plonemeeting.org>',
                u'pmN2 <user@plonemeeting.org>',
                u'pmPresident <user@plonemeeting.org>',
                u'pmSecretaire <user@plonemeeting.org>']


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUtils, prefix='test_pm_'))
    return suite
