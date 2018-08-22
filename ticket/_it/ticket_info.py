# -*- coding: utf-8 -*-
import logging
import requests

from conf import ticket_config

logger = logging.getLogger("lcc_ticket_info")


class ITiger(object):

    def __init__(self, req):
        self._req = req

    def get_ticket_result(self):
        pnrinfo = {}
        pnr = self._req.pnr.encode("utf-8")
        last_name = self._req.passengers[0]["name"].split("/")[0].encode("utf-8")
        first_name = self._req.passengers[0]["name"].split("/")[1].encode("utf-8")
        req_passengers = self._req.passengers
        pnrinfo["pnr"] = pnr
        pnrinfo["contactLastName"] = last_name
        pnrinfo["contactFirstName"] = first_name
        result = requests.post("https://tiger-wkgk.matchbyte.net/wkapi/v1.0/booking",
                               timeout=ticket_config.getint("it", "timeout"), json=pnrinfo)
        response = {"status": 0, "message": "success"}
        req_conut = ticket_config.getint("it", "req_count")-1
        while result.status_code != 200:
            proxy_inf = ticket_config.get("proxy", "dynamicProxy")
            proxies = {"http": "http://" + proxy_inf,
                       "https": "http://" + proxy_inf}
            try:
                result = requests.post("https://tiger-wkgk.matchbyte.net/wkapi/v1.0/booking",
                                       timeout=ticket_config.getint("it", "timeout"), proxies=proxies,
                                       json=pnrinfo)
            except Exception:
                pass
            req_conut -= 1
            if req_conut == 0 and result.status_code != 200:
                logger.error("check ticket error:passenger info error:ipcc:%s,pnr:%s,lastName:%s,firstName:%s" % (
                    self._req.ipcc,
                    pnr, last_name,
                    first_name))
                response["status"] = 4
                response["message"] = "request the failure of the official network"
                return response
        result_json = result.json()
        try:
            passengers = result_json["passengers"]
            for passenger in passengers:
                res_first_name = passenger["firstName"].replace(" ", "")
                res_last_name = passenger["lastName"].replace(" ", "")
                for req_passenger in req_passengers:
                    if req_passenger["firstName"].replace(" ", "").lower() == res_first_name.lower() and req_passenger[
                        "lastName"].replace(" ", "").lower() == res_last_name.lower():
                        paxDatas = passenger["paxData"]
                        req_passenger["ticketStatus"] = "checked"
                        for paxData in paxDatas:
                            seatDesignator = paxData["paxSegmentData"][0]["seatInfo"]["seatDesignator"]
                            if seatDesignator == "-":
                                req_passenger["ticketStatus"] = "open"
                                break
            response["passengers"] = req_passengers
            return response
        except KeyError:
            logger.error(
                "check ticket error:passenger info error:ipcc:%s,pnr:%s,lastName:%s,firstName:%s" % (self._req.ipcc,
                                                                                                     pnr, last_name,
                                                                                                     first_name))
            response["status"] = 2
            response["message"] = "passenger info error"
            return response
