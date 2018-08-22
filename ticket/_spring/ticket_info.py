# -*- coding: utf-8 -*-
import json
import logging
import grequests
import sys

from conf import ticket_config

logger = logging.getLogger("lcc_ticket_info")


class Spring(object):
    __card_type = {"PP": 2, "TB": 3, "HX": 10, "GA": 13, "TW": 19}

    def card_type_num(self, type):
        return self.__card_type[type]

    def __init__(self, req):
        self._req = req

    def get_ticket_result(self):
        pnr = self._req.pnr
        req_passengers = self._req.passengers
        request_parms = []
        for req_passenger in req_passengers:
            request_parms.append(
                {"OrderNo": pnr, "CardType": self.__card_type[req_passenger["cardType"]],
                 "CardNo": req_passenger["cardNum"]})
        tasks = (grequests.post("https://en.ch.com/flights/service/CheckTicketDetail",
                                timeout=ticket_config.getint("spring", "timeout"), json=request_parm) for
                 request_parm in request_parms)
        rs = grequests.map(tasks)
        response = {"status": 0, "message": "success"}
        for r in rs:
            if r is not None and r.status_code == 200:
                for req_passenger in req_passengers:
                    try:
                        check_tickets = r.json()["CheckTickets"][0]
                        logging.info("9C Response:{0}".format(json.dumps(check_tickets)))
                        if self.check_passenger(check_tickets, req_passenger):
                            req_passenger["arrAirport"] = check_tickets["ACode"]
                            req_passenger["depAirport"] = check_tickets["DCode"]
                            req_passenger["ticketStatus"] = "open" if check_tickets[
                                                                          "StatusStr"] == "Sold" else "checked"
                    except Exception:
                        logger.error(
                            "check ticket error:passenger info error:ipcc:%s,pnr:%s,cardType:%s cardNum:%s And Error Is:%s" % (
                                self._req.ipcc,
                                pnr, req_passenger["cardType"], req_passenger["cardNum"], sys.exc_info()))
                        response["status"] = 2
                        response["message"] = "passenger info error"
                        return response
            else:
                response["status"] = 4
                response["message"] = "request the failure of the official network"
                return response
        response["passengers"] = req_passengers
        return response

    def format_string(self, string):
        return string.replace(" ", "").lower().encode("utf-8")

    def check_passenger(self, check_tickets, req_passenger):
        if self.format_string(req_passenger["lastName"]) != self.format_string(check_tickets["FamilyName"]):
            return False
        if self.format_string(req_passenger["firstName"]) != self.format_string(check_tickets["PersonalName"]):
            return False
        return True
