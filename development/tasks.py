"""
Made By: Shubham Heda
Developed Projects :: Django, Celery, Python, Rails and Angular
Under:  AppWallaz Company
"""

from __future__ import absolute_import, unicode_literals

import os
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from development.utils import scrapers
from development.Scripts import commonwealthauction as cwa
from development.Scripts import baystateauction as bsa
from development.Scripts import landmarkauction as lma
from development.Scripts import harkinsrealestate as hre
#from development.Scripts import patriotauctioneers as pa
from development.Scripts import pesco as pe
from development.Scripts import tacheauctionsandsales as tas
#from development.Scripts import sullivanauctioneers as sa
from development.Scripts import towneauction as ta
from celery.utils.log import get_task_logger
from datetime import datetime

# python manage.py celerybeat --verbosity=2 --loglevel=DEBUG
# python manage.py celeryd --verbosity=2 --loglevel=DEBUG


logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example():
    logger.info("Start task CommonWealthAuction")
    cwa.start_app()
    # result = scrapers.scraper_example(now.day, now.minute)
    logger.info("Processing!!! Done")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example_2():
    logger.info('Start Task BayStateAuction')
    bsa.start_app()
    logger.info("Processing!!! Done")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example_3():
    logger.info('Start Task Harkins Real State')
    hre.start_app()
    logger.info("Processing!!! Done")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example_4():
    logger.info('Start Task Land Mark Auction')
    lma.start_app()
    logger.info("Processing!!! Done")


# @periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
# def scraper_example_5():
#     logger.info('Start Task PatriotAuctioneer')
#     pa.start_app()
#     logger.info("Processing!!! Done")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example_6():
    logger.info('Start Task Pesco')
    pe.start_app()
    logger.info("Processing!!! Done")


# @periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
# def scraper_example_7():
#     logger.info('Start Task Sullivan Auctioneer')
#     sa.start_app()
#     logger.info("Processing!!! Done")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example_8():
    logger.info('Start Task TacheAuctionsSales')
    tas.start_app()
    logger.info("Processing!!! Done")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example_9():
    logger.info('Start Task TowneAuction')
    ta.start_app()
    logger.info("Processing!!! Done")
