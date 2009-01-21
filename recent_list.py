"""An iterable, list-type class that auto-expires members.

The intended use for this is to support an error retry loop that must abort if
there are too many errors in a short time period.

As of 1/21/09 it is not written to be efficient, just to be simple and get the job done.

>>> x = RecentList(max_minutes=5)
>>> x.append(1)
>>> x.append(2, backdate_minutes=6)
>>> x.append(3, backdate_minutes=4)
>>> list(x)
[1, 3]
>>> x = RecentList(max_minutes=5)
>>> x.append(1)
>>> x.append(2, backdate_minutes=6)
>>> len(x)
1
"""
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta
class RecentList(object):
    def __init__(self, max_minutes):
        self.max_minutes = max_minutes
        self._list = list()
    def __getitem__(self, i):
        self._sweep()
        x = self._list.__getitem__(i)
        return x[1]
    def __delitem__(self, i):
        return self._list.__delitem__(i)
    def __len__(self):
        self._sweep()
        return self._list.__len__()
    def _sweep(self):
        cutoff_time = _datetime.now() - _timedelta(minutes=self.max_minutes)
        self._list = [x for x in self._list if x[0] >= cutoff_time]
    def insert(self, i, value, backdate_minutes=0):
        d = _datetime.now() - _timedelta(minutes=backdate_minutes)
        return self._list.insert(i, (d, value))
    def append(self, value, backdate_minutes=0):
        self.insert(len(self), value, backdate_minutes=backdate_minutes)
if __name__ == '__main__':
    import doctest
    print "Running doctest . . ."
    doctest.testmod()
