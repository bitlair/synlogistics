#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from django.core.management import setup_environ
import settings

setup_environ(settings)

from invoicing.models import Invoice, TimeKeepingEntry
from moneyed import Money
from decimal import Decimal
from itertools import chain

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate, BaseDocTemplate, FrameBreak
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.fonts import tt2ps
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib import colors

class Normal(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('normal', fontName="DejaVu"))

class Center(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('center', fontName="DejaVu", alignment=TA_CENTER))

class AlignRight(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('alignright', fontName="DejaVu", alignment=TA_RIGHT))

class Bold(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('bold', fontName="DejaVu-Bold"))

class BoldRight(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('boldright', fontName="DejaVu-Bold", alignment=TA_RIGHT))

class TableHead(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('tablehead', fontName="DejaVu-Bold"))

class TableHeadRight(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('tableheadright', fontName="DejaVu-Bold", alignment=TA_RIGHT))

class Header1(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('header1', fontName="DejaVu-Bold", fontSize=20, leading=25))

class Header2(Paragraph):
    def __init__(self, text):
        Paragraph.__init__(self, text, PS('header2', fontName="DejaVu-Bold", fontSize=14, leading=16))


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Dejavu-Italic', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-BoldItalic', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-BoldOblique.ttf'))

from reportlab.lib.fonts import addMapping
addMapping('DejaVu', 0, 0, 'DejaVu')
addMapping('DejaVu', 0, 1, 'DejaVu-Italic')
addMapping('DejaVu', 1, 0, 'DejaVu-Bold')
addMapping('DejaVu', 1, 1, 'DejaVu-BoldItalic')

import reportlab.rl_config
reportlab.rl_config.canvas_basefontname = 'DejaVu'

import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')

import moneyed.localization


def format_money(money):
    return moneyed.localization._FORMATTER.format(money, locale="nl_NL")

for invoice in Invoice.objects.filter(number=sys.argv[1]):
    customer = invoice.customer
    frameleft = Frame(x1 = 0, y1= 250*mm, width=A4[0]*0.5, height=45*mm, leftPadding=15*mm, topPadding=15*mm)
    frameright = Frame(x1 = A4[0]*0.5, y1= 250*mm, width=A4[0]*0.5, height=45*mm, rightPadding=15*mm, topPadding=15*mm)
    framerest = Frame(x1 = 0, y1= 0, width=A4[0], height=A4[1]-50*mm, leftPadding=15*mm, rightPadding=15*mm)
    main = PageTemplate(frames=[frameleft, frameright, framerest])
    doc = BaseDocTemplate("invoices/%s.pdf" % invoice.full_invoice_no, pageTemplates=main)
    flowlist = []
    flowlist.append(Header1("Factuur"))
    flowlist.append(Spacer(0, 5*mm))
    flowlist.append(Normal("<br/>".join([customer.name, customer.postal_address, customer.postal_zip_code+" "+customer.postal_city])))
    flowlist.append(FrameBreak())
    flowlist.append(AlignRight("Pyzuka<br/>Van Hasseltlaan 91<br/>2625 HE Delft<br/><br/>KvK: 53159683<br/>BTW: NL179866382B01"))
    flowlist.append(FrameBreak())
    flowlist.append(Normal("Factuurnummer: %s" % invoice.full_invoice_no))
    flowlist.append(Normal("Factuurdatum: %s" % invoice.date))

    print invoice
    tot_ex = Money(0, 'EUR')
    tot_inc = Money(0, 'EUR')
    tot_btw = Money(0, 'EUR')
    itemlist = []
    for item in chain(invoice.timekeepingentry_set.order_by('date'), invoice.simple_items.all()):
        if isinstance(item, TimeKeepingEntry):
            if item.start_time:
                description = "%s: %s-%s %s" % (item.date, item.start_time.strftime("%H:%M"), item.end_time.strftime("%H:%M"), item.description)
            else:
                description = "%s: %s" % (item.date, item.description)
            count = item.hours
            price = item.rate.rate
            vat_percent = item.rate.vat.percent
        else:
            description = item.description
            count = item.count
            price = item.price
            vat_percent = item.vat.percent
        ex_btw = count * price
        btw = ex_btw * vat_percent/100
        print description
        print "%s x %s = %s ex btw" % (count, format_money(price), format_money(ex_btw))
        tot_ex += ex_btw
        tot_btw += btw
        itemlist.append([AlignRight(locale.format("%.2f", count)), AlignRight(format_money(price)), Normal(description), AlignRight(format_money(ex_btw))])

    tot_btw = tot_btw
    tot_inc = tot_ex + tot_btw
    print "tot %s tot inc %s tot btw %s" % (format_money(tot_ex), format_money(tot_inc), format_money(tot_btw))
    print
    flowlist.append(Spacer(0, 5*mm))
    if itemlist:
        table = Table([[Normal("Aantal"), Center("Prijs"), Normal("Beschrijving"), AlignRight("Totaal")]] +
                      itemlist + [[Bold("Subtotaal"), '', '', BoldRight(format_money(tot_ex))],
                                  ["BTW (19%)", '', '', AlignRight(format_money(tot_btw))],
                                  [Bold("Totaal"), '', '', BoldRight(format_money(tot_inc))]],
                      [15*mm, 20*mm, A4[0]-(15+20+28+15+15)*mm, 28*mm])
        table.setStyle(TableStyle([('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
                                   ('LINEABOVE', (0, -3), (-1, -3), 1, colors.black),
                                   ('VALIGN',(0,0),(-1,-1),'TOP')]))
        flowlist.append(table)


    flowlist.append(Spacer(0, 10*mm))
    flowlist.append(Normal(u"Gelieve het totaalbedrag van %s binnen 30 dagen te voldoen onder vermelding van factuurnummer "
                           u"%s op rekening 11.69.44.684 ten name van Pyzuka." % (format_money(tot_inc), invoice.full_invoice_no)))
    doc.build(flowlist)
