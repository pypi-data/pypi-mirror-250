# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.transaction import Transaction
from trytond.pool import PoolMeta


class IrActWindow(metaclass=PoolMeta):
    __name__ = 'ir.action.act_window'

    @classmethod
    def __register__(cls, module_name):
        super(IrActWindow, cls).__register__(module_name)

        # migrate: domain --> context_domain
        records = cls.search([
            ('res_model', '=', 'cashbook_report.eval_line'),
            ('domain', '!=', None),
            ('context_domain', '=', None),
            ('context_model', '=', None)])
        if records:
            to_write = []
            for record in records:
                to_write.extend([
                    [record],
                    {
                        'context_domain': record.domain,
                        'domain': None,
                    }])
            cls.write(*to_write)

# end IrActWindow
