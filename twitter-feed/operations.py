""" Copyright start
  Copyright (C) 2008 - 2022 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import requests, json
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('twitter-feed')


def check_health(config):
    try:
        url = '/v1/tweets/daily/full'
        resp = make_rest_call(config, url)
        if resp:
            return True
    except Exception as Err:
        logger.exception(Err)
        raise ConnectorError(Err)


def make_rest_call(config, url):
    try:
        server_url = config.get('server_url').strip('/')
        if not server_url.startswith('https://') and not server_url.startswith('http://'):
            server_url = 'http://{0}'.format(server_url)
        logger.info('executing url ={}'.format(server_url+url))
        response = requests.get(server_url+url, verify=config.get('verify_ssl'))
        if response.ok:
            if 'json' in str(response.headers):
                return response.json()
            else:
                logger.debug('Response not in json format')
                return json.loads(response.text)
        else:
            raise ConnectorError(
                'Unable to access the feed URL. Check connectivity and retry. Error status: {0}, response = {1}'.format(response.status_code, response.text))
    except requests.exceptions.SSLError:
        logger.error('An SSL error occurred.')
        raise ConnectorError('An SSL error occurred.')
    except requests.exceptions.ConnectionError:
        logger.error('A connection error occurred.')
        raise ConnectorError('A connection error occurred.')
    except Exception as Err:
        logger.exception(Err)
        raise ConnectorError(Err)


def get_indicators(config, params):
    try:
        feed_type = params.get('feed_type', None)
        if feed_type == 'Username':
            url = '/v1/tweets/daily/full/user/{0}'.format(params.get('filter_value'))
        elif feed_type == 'Hashtag':
            url = '/v1/tweets/daily/full/hashtags/{0}'.format(params.get('filter_value'))
        else:
            url = '/v1/tweets/daily/full'
        resp = make_rest_call(config, url)
        return resp
    except Exception as Err:
        logger.exception(Err)
        raise ConnectorError(Err)


operations = {
    'get_indicators': get_indicators
}


#http://www.tweettioc.com/v1/tweets/daily/full
