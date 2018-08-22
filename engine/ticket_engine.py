# -*- coding: utf-8 -*-
from ticket.ticket_factory import TicketFactory


class TicketEngine(object):
    def run(self, req):
        ticket = TicketFactory.newTicket(req)
        if not ticket:
            result = {"status": 3, "message": "not found ipcc"}
            return result
        return ticket.get_ticket_result()
