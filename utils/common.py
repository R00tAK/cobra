# -*- coding: utf-8 -*-

"""
    utils.common
    ~~~~~~~~~~~~

    Implements common helpers

    :author:    Feei <wufeifei#wufeifei.com>
    :homepage:  https://github.com/wufeifei/cobra
    :license:   MIT, see LICENSE for more details.
    :copyright: Copyright (c) 2016 Feei. All rights reserved
"""
import sys
import datetime
import hashlib
import logging
from utils import config

logging = logging.getLogger(__name__)


def convert_timestamp(stamp):
    """returns a datetime.date object off a timestamp"""
    # Really, this should be implemented using time.strptime()
    date_shards = stamp.split()
    date_shards = date_shards[0].split('-')
    date_shards = [x.lstrip('0') for x in date_shards]
    processed_date = datetime.date(int(date_shards[0]), int(date_shards[1]), int(date_shards[2]))
    return processed_date


def convert_time(seconds):
    """
    Seconds to minute/second
    Ex: 61 -> 1′1″
    :param seconds:
    :return:
    :link: https://en.wikipedia.org/wiki/Prime_(symbol)
    """
    one_minute = 60
    minute = seconds / one_minute
    if minute == 0:
        return str(seconds % one_minute) + "″"
    else:
        return str(minute) + "′" + str(seconds % one_minute) + "″"


def convert_number(number):
    """
    Convert number to , split
    Ex: 123456 -> 123,456
    :param number:
    :return:
    """
    if number is None or number == 0:
        return 0
    number = int(number)
    return '{:20,}'.format(number)


def md5(content):
    """
    MD5 Hash
    :param content:
    :return:
    """
    return hashlib.md5(content).hexdigest()


def allowed_file(filename):
    """
    Allowd upload file
    Config Path: ./config [upload]
    :param filename:
    :return:
    """
    config_extension = config.Config('upload', 'extensions').value
    if config_extension == '':
        logging.critical('Please set config file upload->directory')
        sys.exit(0)
    allowed_extensions = config_extension.split('|')
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions


def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true", "t", "1"): return True
    if str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


def path_to_short(path, max_length=36):
    """
    /impl/src/main/java/com/mogujie/service/mgs/digitalcert/utils/CertUtil.java
    impl/.../CertUtil.java
    :param path:
    :return:
    """
    if len(path) < max_length:
        return path
    paths = path.split('/')
    tmp_path = ''
    for i in range(0, len(paths)):
        tmp_path = str(paths[i]) + str(paths[paths-i])
        if len(tmp_path) > max_length:
            return tmp_path

