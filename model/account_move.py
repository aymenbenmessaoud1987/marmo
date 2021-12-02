#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

# -*- coding: utf-8 -*-
from odoo import models, fields, api ,_
from odoo.http import request
from .qr_generator import generateQrCode
from odoo.tools import html2plaintext
import codecs
from uttlv import TLV
import base64
import time
import datetime
from fatoora import Fatoora



class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"
    einv_amount_sale_total = fields.Monetary(string="Amount sale total", compute="_compute_total", store='True',
                                             help="")
    einv_amount_discount_total = fields.Monetary(string="Amount discount total", compute="_compute_total", store='True',
                                                 help="")
    einv_amount_tax_total = fields.Monetary(string="Amount tax total", compute="_compute_total", store='True', help="")

    qr_image = fields.Binary("QR Code", compute='_generate_qr_code',store='True')
    # amount_invoiced = fields.Float(string="Amount tax total", help="")
    # qrcode = fields.Char(string="QR", help="")


    def _generate_qr_code(self):

                fatoora_obj = Fatoora(
                    seller_name=self.company_id.name,
                    tax_number=self.company_id.vat,  # or "1234567891"
                    invoice_date=str((datetime.datetime.strptime(str(self.create_date.strftime("%d-%b-%Y-%H:%M:%S")), "%d-%b-%Y-%H:%M:%S").timestamp())),  # Timestamp
                    total_amount=self.amount_tax_signed,  # or 100.0, 100.00, "100.0", "100.00"
                    tax_amount=self.amount_total,  # or 15.0, 15.00, "15.0", "15.00"
                )


                self.qr_image = generateQrCode.generate_qr_code(fatoora_obj.base64)
                print(self.qr_image)




class AccountMoveLineInherit(models.Model):
    _inherit = 'account.invoice.line'

    tax_amount = fields.Float(string="Tax Amount", compute="_compute_tax_amount")




    @api.depends('invoice_line_tax_ids', 'price_unit','quantity')
    def _compute_tax_amount(self):
        for line in self:
            if line.invoice_line_tax_ids:
                line.tax_amount = line.price_total - line.price_subtotal
            else:
                line.tax_amount = 0.0
