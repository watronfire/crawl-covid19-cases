import scrapy
import logging
from covid19.items import TestingStats
import requests
import json
from datetime import datetime as dt
from dateutil.parser import parse

class AustraliaSpider( scrapy.Spider ) :

    name = "australia"
    allowed_domains = ["https://health.act.gov.au"]
    obj = ["AustraliaCapital"]
    case_categories = ["positive", "pending", "negative"]
    names = ["Australia Capital" ]
    custom_settings = { "LOG_LEVEL" : logging.ERROR }


    def start_requests( self ):
        yield scrapy.Request( "https://health.act.gov.au/public-health-alert/updated-information-about-covid-19", callback=self.parse )

    def parse( self, response ):
        item = TestingStats()
        positive = response.xpath( '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/article/div/div[1]/div/div[2]/div[1]/text()' ).get()
        positive = positive.split( ": " )[-1]

        negative = response.xpath( '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/article/div/div[1]/div/div[2]/div[2]/text()' ).get()
        negative = negative.split( ": " )[-1]

        date = response.xpath( '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/article/div/div[1]/div/div[1]/span/text()' ).get()
        date = parse( date, fuzzy=True )


        item["date"] = date.strftime( "%Y-%m-%d %H:%M %p" )
        item["name"] = self.names[0]
        item["positive"] = positive
        item["negative"] = negative
        print( item.toAsciiTable() )
        return item

#['aupyth',
# 'australiansw',
# 'canadaalberta',
# 'canadabritishcolumbia',
# 'canadanational',
# 'canadaontario',
# 'unitedkingdomnational',
# 'florida',
# 'illinois',
# 'newmexico',
# 'newyork',
# 'oregon',
# 'sandiego',
# 'snohomish',
# 'washington']
