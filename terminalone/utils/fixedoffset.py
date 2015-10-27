from datetime import tzinfo, timedelta


class FixedOffset(tzinfo):
    """Fixed offset in minutes: `time = utc_time + utc_offset`."""

    def __init__(self, offset):
        self.__offset = timedelta(minutes=offset)
        hours, minutes = divmod(offset, 60)
        # NOTE: the last part is to remind about deprecated POSIX GMT+h timezones
        #  that have the opposite sign in the name;
        #  the corresponding numeric value is not used e.g., no minutes
        self.__name = '<%+03d%02d>%+d' % (hours, minutes, -hours)

    def utcoffset(self, dt=None):
        return self.__offset

    def tzname(self, dt=None):
        return self.__name

    def dst(self, dt=None):
        return timedelta(0)

    def __repr__(self):
        return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)
