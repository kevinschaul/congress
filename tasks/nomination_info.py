import utils
import logging
import re
import json
from datetime import datetime
from lxml import etree
import time
from lxml.html import fromstring

# Can be run on its own, requires a congress and nomination_id (e.g. PN2094)
def run(options):
    congress = options.get('congress', utils.current_congress)
    nomination_id = options.get('nomination_id', None)

    if congress and nomination_id:
        nomination_id_full = {
            "id": nomination_id,
            "congress": congress
        }
        result = fetch_nomination(nomination_id_full, options)
        logging.warn("\n%s" % result)
    else:
        logging.error("To run this task directly, supply a congress and a nomination_id.")

def fetch_nomination(nomination_id_full, options={}):
    # Download and parse information about a specific nomination, given a dict
    # with the nomination's congress and id
    nomination_id = nomination_id_full.get('id')
    congress = nomination_id_full.get('congress')

    if nomination_id and congress:
        logging.info("\n[%s-%s] Fetching..." % (congress, nomination_id))

        # Fetch bill details html
        html = utils.download(
                nomination_url_for(congress, nomination_id),
                nomination_cache_for(congress, nomination_id, "details.html"), options)

        if not html:
            return {'saved': False, 'ok': False, 'reason': "failed to download"}

        if options.get("download_only", False):
            return {'saved': False, 'ok': True, 'reason': "requested download only"}

        # TODO:
        #   detect group nominations, particularly for military promotions
        #   detect when a group nomination is split into subnominations
        #
        # Also, the splitting process is nonsense:
        # http://thomas.loc.gov/home/PN/split.htm
        # http://web.archive.org/web/20141006022210/http://thomas.loc.gov/home/PN/split.htm
        # TODO handle splits
        #if "split into two or more parts" in html:
            #return {'saved': False, 'ok': True, 'reason': 'was split'}

        nomination = parse_nomination(congress, nomination_id, html, options)
        output_nomination(nomination, options)
        return {'ok': True, 'saved': True}
    else:
        return {'saved': False, 'ok': False, 'reason': 'Both nomination_id and congress are required'}

def parse_nomination(congress, nomination_id, html, options):
    info = {
        'congress': congress,
        'nomination_id': nomination_id,
        'actions': [],
        'committee_names': [],
        'committees': []
    }

    doc = html.document_fromstring(page_html)

    # TODO parse nomination details

    return info

def output_for_nomination(congress, nomination_id, format):
    # TODO what is format
    # TODO what is data_dir() and should we be using it everywhere?
    return "%s/%s/nominations/%s/%s" % (utils.data_dir(), congress, nomination_id, "data.%s" % format)

def nomination_url_for(congress, nomination_id):
    # nomination_id can be either of the form "63" or "64-01"
    # Some example URLs:
    # https://www.congress.gov/nomination/114th-congress/74

    # TODO what is this
    #number_pieces = number.split("-")
    #if len(number_pieces) == 1:
        #number_pieces.append("00")
    #url_number = "%05d%s" % (int(number_pieces[0]), number_pieces[1])

    suffix = utils.get_numerical_suffix(congress)
    return "https://www.congress.gov/nomination/%s%s-congress/%s" % (congress, suffix, nomination_id)

def nomination_cache_for(congress, nomination_id, filename):
    return "%s/nominations/%s/%s" % (congress, nomination_id, filename)

def output_nomination(nomination, options):
    logging.info("[%s] Writing to disk..." % nomination['nomination_id'])

    # TODO does this need to check for the format?
    # output JSON - so easy!
    utils.write(
            json.dumps(nomination, sort_keys=True, indent=2, default=utils.format_datetime),
            output_for_nomination(nomination['congress'], nomination['nomination_id'], "json")
            )
