import json
import urllib
import utils
import os
import os.path
import re
from lxml import html, etree
import logging

import nomination_info


def run(options):
    nomination_id = options.get('nomination_id', None)

    if nomination_id:
        nomination_type, number, congress = utils.split_nomination_id(nomination_id)
        to_fetch = [nomination_id]
    else:
        congress = options.get('congress', utils.current_congress())
        to_fetch = get_nominations_to_process(congress, options)

        if not to_fetch:
            # TODO Find out what the "fast" option is
            if options.get("fast", False):
                logging.warn("No nominations changed.")
            else:
                logging.error("Error figuring out which nominations to download, aborting.")
            return None

        limit = options.get('limit', None)
        if limit:
            to_fetch = to_fetch[:int(limit)]

    logging.warn("Going to fetch %i nominations from congress #%s" % (len(to_fetch), congress))
    utils.process_set(to_fetch, nomination_info.fetch_nomination, options)

def get_nominations_to_process(congress, options={}):
    # Return a generator over nomination_ids that need to be processed.
    # TODO Figure out whether there is a way to do a last modified check like
    # bills.py does
    nomination_ids = []
    pages = get_pages(congress, options={})
    for page in pages:
        nomination_ids = nomination_ids + parse_nomination_ids(page)

    return [{"id": x, "congress": congress} for x in nomination_ids]

def parse_nomination_ids(page_html):
    # Given a page's html, return a list of nomination ids
    doc = html.document_fromstring(page_html)
    nominations = doc.xpath("//*[@id='main']/ol[contains(@class, 'basic-search-results-lists')]/li")
    ids = []
    for nomination in nominations:
        # The link text of the heading contains the nomination id
        links = nomination.cssselect('.result-heading a')
        if links and len(links) > 0:
            link = links[0]
            ids.append(link.text)

    return ids

def get_pages(congress, options={}):
    pages = []

    current_page = 1
    while current_page == 1 or next_page_exists(pages[-1]):
        # TODO cache false?
        url = get_page_url(congress, current_page)
        page_html = utils.download(
            url,
            "%s/nominations/pages/page_%s.html" % (congress, current_page),
            options)
        pages.append(page_html)

        current_page += 1

    return pages

def next_page_exists(page_html):
    # Given a page's html, return whether there is a subsequent page. Relies on
    # the pagination navigation element at bottom of results. If the "next"
    # element is a link, then there is a next page.
    doc = html.document_fromstring(page_html)
    next_link = doc.xpath("//*[@id='main']/*[@role='navigation']//a[contains(@class, 'next')]")

    return bool(next_link)

def get_page_url(congress, page=1):
    # Given a congress and optional page number, return the Congress.gov url
    # listing nominations
    #
    # Example:
    # https://www.congress.gov/search?q={"source":"nominations","congress":"115"}&pageSort=actionDesc&pageSize=250
    query = {
        "q": json.dumps({
            "source": "nominations",
            "congress": str(congress)
        }, separators=(',', ':')),
        "pageSort": "actionDesc",
        "pageSize": 250,
        "page": page
    }
    params = urllib.urlencode(query)
    return "https://www.congress.gov/search?%s" % params
