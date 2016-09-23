# Scrapy settings for hscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os

BOT_NAME = 'hscrapy'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['hscrapy.spiders']
NEWSPIDER_MODULE = 'hscrapy.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

PROJECT_PATH = os.path.dirname(__file__)

PS_CONFIG = PROJECT_PATH + os.sep + "pc.json"
DEST_DIR = PROJECT_PATH + os.sep + "dist"
