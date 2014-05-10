


class Pin(object):
    def __init__(self):
        self._pinid = None
        self._pinname = None
        self._pinurl = None
        self._pincomments = None


    @property
    def pinid(self):
        return self._pinid

    @property
    def pinname(self):
        return self._pinname

    @property
    def pinurl(self):
        return self._pinurl

    @property
    def pincomments(self):
        return self._pincomments

    @pinid.setter
    def x(self, value):
        self._pinid = value

    @pinname.setter
    def x(self, value):
        self._pinname = value


    @pinurl.setter
    def x(self, value):
        self._pinurl = value

    @pincomments.setter
    def x(self, value):
        self._pincomments = value

    @pinid.deleter
    def x(self):
        del self._pinid

    @pinname.deleter
    def x(self):
        del self._pinname

    @pinurl.deleter
    def x(self):
        del self._pinurl

    @pincomments.deleter
    def x(self):
        del self._pincomments


