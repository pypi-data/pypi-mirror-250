city-scrapers-sentry
=============

A Scrapy extension that logs spider errors to Sentry.

This project began as a fork of [scrapy-sentry](https://github.com/llonchj/scrapy-sentry), which was developed by Jordi Llonch. We are grateful for their work and contributions.

Note: while this extension captures errors from Scrapy spiders, it does not capture errors elsewhere in Scrapy's operation (e.g. the Scrapy pipeline).

Requisites: 
-----------

* [Sentry server](http://www.getsentry.com/)

Installation
------------

```
pip install city-scrapers-sentry
```

Setup
-----

Add `SENTRY_DSN` and `city_scrapers_sentry.extensions.Errors` extension to your Scrapy Project `settings.py`.

Example:

```
# sentry dsn
SENTRY_DSN = 'http://public:secret@example.com/1'
EXTENSIONS = {
    "city_scrapers_sentry.extensions.Errors": 10,
}
```
