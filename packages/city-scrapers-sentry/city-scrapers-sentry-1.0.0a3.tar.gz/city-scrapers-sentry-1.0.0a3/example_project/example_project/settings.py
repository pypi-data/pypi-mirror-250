import os
# Scrapy settings for example_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "example_project"

if not os.environ.get("SENTRY_DSN"):
    import sys
    sys.stderr.write("Please define SENTRY_DSN in your environment "
                     "to run this example_project")
    exit(1)


SENTRY_DSN = os.environ["SENTRY_DSN"]
EXTENSIONS = {
    'city_scrapers_sentry.extensions.Errors': 10,
}

SPIDER_MODULES = ["example_project.spiders"]
NEWSPIDER_MODULE = "example_project.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
