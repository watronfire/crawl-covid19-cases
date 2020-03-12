import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt

class AustraliaNSWSpider( scrapy.Spider ) :

    name = "australiansw"
    allowed_domains = ["https://www.health.nsw.gov.au"]
    obj = ["AustraliaNSW"]
    case_categories = ["positive", "pending", "negative"]
    names = ["NSW, AUS"]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }

    #  https://www.health.nsw.gov.au/news/Pages/default.aspx is listing of pres releases

    def start_requests( self ):
        url_gen = "https://www.health.nsw.gov.au/news/Pages/{}_00.aspx".format( dt.now().strftime( "%Y%m%d" ) )
        yield scrapy.Request( url_gen, callback=self.parse )

    def parse( self, response ):
        item = TestingStats()

        confirmed = response.xpath( '/html/body/form/div[2]/div[2]/div/div[3]/div[2]/div[3]/table/tbody/tr[2]/td[2]//text()[1]' ).get()
        confirmed = confirmed.replace( "*", "" )
        pending = response.xpath( '/html/body/form/div[2]/div[2]/div/div[3]/div[2]/div[3]/table/tbody/tr[3]/td[2]/text()' ).get()
        pending = pending.replace( ",", "" )
        negative = response.xpath( '/html/body/form/div[2]/div[2]/div/div[3]/div[2]/div[3]/table/tbody/tr[4]/td[2]/text()' ).get()
        negative = negative.replace( ",", "" )



        date =  response.xpath( '/html/body/form/div[2]/div[2]/div/div[3]/div[2]/div[1]/div/text()' ).get()
        date = date.strip()
        date = dt.strptime( date, "%d %B %Y" )

        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["Local"] = { "name" : self.names[0],
                          "positive" : confirmed,
                          "negative" : negative,
                          "pending" : pending }
        print( item.toAsciiTable() )
        return item