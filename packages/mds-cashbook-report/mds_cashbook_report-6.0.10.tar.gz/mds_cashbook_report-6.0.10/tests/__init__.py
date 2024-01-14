# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_report.tests.test_report import ReportTestCase


__all__ = ['suite']


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ReportTestCase))
    return suite
