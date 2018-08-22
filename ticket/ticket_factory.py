# -*- coding: utf-8 -*-
from ticket._it.ticket_info import ITiger
from ticket._spring.ticket_info import Spring


class TicketFactory(object):
    @staticmethod
    def newTicket(req):
        if req.ipcc == 'TTW_F':
            return ITiger(req)
        if req.ipcc == '9C_F':
            return Spring(req)
        if req.ipcc == 'BDFZ_F':
            return Spring(req)
        if req.ipcc == 'BDIJ_F':
            return Spring(req)
        if req.ipcc == 'BDTK_F':
            return Spring(req)
