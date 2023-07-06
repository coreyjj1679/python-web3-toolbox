from datetime import datetime
import time


def timestamp_to_datestr(_timestamp: int, _format: str = None) -> str:
    """
    :param _timestamp: UNIX timestamp
    :param _format: datestr format, default as YYYY-MM-DD HH:MM:SS
    :return: datestr in specific format
    """
    if _format:
        return datetime.fromtimestamp(_timestamp).strftime(_format)
    else:
        return datetime.fromtimestamp(_timestamp).strftime('%Y-%m-%d %H:%M:%S')


def datestr_to_timestamp(_datestr: str) -> int:
    """
    :param _datestr: datestr in YYYY-MM-DD format
    :return: UNIX timestamp
    """
    return int(format((time.mktime(datetime.strptime(_datestr,
                                                     '%Y-%m-%d %H:%M:%S').timetuple())), '.10g'))

def get_current_timestamp() -> int:
    """
    :return: UNIX timestamp
    """
    return int(format((time.mktime(datetime.now().timetuple())), '.10g'))