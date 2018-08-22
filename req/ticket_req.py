# -*- coding: utf-8 -*-
import json
import logging


class TicketReq(object):
    logger = logging.getLogger()

    _key_pnr = "pnr"
    _key_from_city = "fromCity"
    _key_to_city = "toCity"
    _key_flight_option = "flightOption"
    _key_ds = "ds"
    _key_ipcc = "ipcc"
    _key_start_time = "startTime"
    _end_time = "endTime"
    _adult_number = "adultNumber"
    _child_number = "childNumber"

    _from_segments = "fromSegments"
    _passengers = "passengers"
    _ret_segments = "retSegments"
    _credit_card_info = "creditCardInfo"
    _key_adultPrice = "adultPrice"
    _key_adultTax = "adultTax"
    _key_childPrice = "childPrice"
    _key_childTax = "childTax"

    cid = ''
    fromCity = ''
    toCity = ''
    startTime = ''
    endTime = ''
    username = ''
    password = ''
    passengers = []
    fromSegments = []
    retSegments = []
    creditCardInfo = {}
    flightOption = 1
    adultNumber = 1
    childNumber = 0
    adultPrice = 0
    adultTax = 0
    childPrice = 0
    childTax = 0
    infantNumber = 0
    ds = ''
    ipcc = ''
    total_price = ""
    order_number = ""
    exchange = 0
    price = 0
    json = ''

    def constructor(self, req):
        self.json = req
        if (not req or
                not self._key_start_time in req or
                not self._key_pnr in req or
                not self._key_from_city in req or
                not self._key_to_city in req or
                not self._from_segments in req or
                not self._key_flight_option in req or
                not self._key_ds in req or
                not self._key_ipcc in req):

            self.logger.error('invalid req: {0}'.format(json.dumps(req)))
            return False
        else:
            self.passengers = req[self._passengers]
            self.pnr = req[self._key_pnr]
            self.fromCity = req[self._key_from_city]
            self.toCity = req[self._key_to_city]
            self.startTime = req[self._key_start_time]
            self.fromSegments = req[self._from_segments]
            self.adultNumber = req[self._adult_number]
            self.childNumber = req[self._child_number]
            if self._ret_segments in req:
                self.retSegments = req[self._ret_segments]
            if self._credit_card_info in req:
                self.creditCardInfo = req[self._credit_card_info]

            flightOption = req[self._key_flight_option]
            if flightOption == 'roundTrip':
                self.flightOption = 2
                self.endTime = req[self._end_time]
            else:
                self.flightOption = 1

            self.ds = req[self._key_ds]
            self.ipcc = req[self._key_ipcc]
            self.adultPrice = req.get("adultPrice")
            self.adultTax = req.get("adultTax")
            self.childPrice = req.get("childPrice")
            self.childTax = req.get("childTax")
            return True
