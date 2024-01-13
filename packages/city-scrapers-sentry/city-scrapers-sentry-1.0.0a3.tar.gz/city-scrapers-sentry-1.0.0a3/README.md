city-scrapers-sentry
=============

A Scrapy extension that logs spider errors to Sentry.

This project began as a fork of [scrapy-sentry](https://github.com/llonchj/scrapy-sentry), which was developed by Jordi Llonch. We are grateful for his work and those of other contributors.

Note: while this extension captures errors from Scrapy spiders, it does not capture errors elsewhere in Scrapy's operation (e.g. the Scrapy pipeline).

Requirements: 
-----------

* A [Sentry](http://www.getsentry.com/) account.
* The [DSN](https://docs.sentry.io/product/sentry-basics/concepts/dsn-explainer/) for your Sentry project.

Installation
------------

```
pip install city-scrapers-sentry
```

Setup
-----

Add `SENTRY_DSN` and `city_scrapers_sentry.extensions.Errors` extension to your Scrapy project's `settings.py` file:

Example:

```
# sentry dsn
SENTRY_DSN = 'http://public:secret@example.com/1'
EXTENSIONS = {
    "city_scrapers_sentry.extensions.Errors": 10,
}
```

Development
-----

1. Install [pipenv](https://pipenv.pypa.io/en/latest/) if you don't have it already.

2. At the project root, create a .env file and include the following. Replace `<your-sentry-dsn>` with your Sentry DSN:
```
SENTRY_DSN=<your-sentry-dsn>
```
3. Run the following command from the project root to activate pipenv's virtual environment and install project dependencies:
```
pipenv sync --dev
```
When activated, pipenv should load your SENTRY_DSN env var from the .env file.

4. Enter the example_project directory:
```
cd example_project
```

5. Simulate a failed spider run. The spider will log an error to your Sentry account:
```
scrapy crawl example
```
