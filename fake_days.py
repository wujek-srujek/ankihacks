#!/usr/bin/env python3

# review percentage calculation reverse engineering
# result: Anki takes the first ever day of review as a number of how many days
# ago it was and total number of days with reviews and uses that
# this means days without any scheduled review will influence the stats, not
# sure if this is good
# to fake a review for a day just move from other day a review in the revlog
# table - set the id to the timestamp in millis of the faked day

from anki.storage import Collection
import types

deck_name = 'Español'
collection_path = '/Users/rafal/Playground/collection.anki2'

collection = Collection(collection_path)
try:
    deck = collection.decks.byName(deck_name)
    if not deck:
        raise ValueError('deck \'{}\' not found'.format(deck_name))
    collection.decks.select(deck['id'])

    stats = collection.stats()
    stats.type = 2  # lifetime

    def daysStudiedSql(self):
        # copied from _daysStudied to just show the SQL, not execute it
        lims = []
        num = self._periodDays()
        if num:
            lims.append(
                "id > %d" % ((self.col.sched.dayCutoff-(num*86400))*1000))
        rlim = self._revlogLimit()
        if rlim:
            lims.append(rlim)
        if lims:
            lim = "where " + " and ".join(lims)
        else:
            lim = ""
        return """
select count(), abs(min(day)) from (select
(cast((id/1000 - {cut}) / 86400.0 as int)+1) as day
from revlog {lim}
group by day order by day)
""".format(lim=lim, cut=self.col.sched.dayCutoff)

    print(types.MethodType(daysStudiedSql, stats)())
    period = stats._deckAge('review')
    daysStudied, fstDay = stats._daysStudied()
    print('days studied', daysStudied, 'first day', fstDay, 'period', period)
    print("{}% ({} of {})".format(daysStudied/period*100, daysStudied, period))
finally:
    collection.close()

# col.crt is creation timestamp
# sched.today is day number after creation
# sched.dayCutoff is end of current day

# select id from cards where did in (1435088749676)
# - returns all cards for deck Español

# select * from revlog where cid in (select id from cards where did in (1435088749676))
# - returns all reviews on all days for all cards for deck Español

# revlog.id is time.time() of review * 1000 (millis)

# select (cast((id/1000 - 1534543200 # cutoff #) / 86400.0 as int)+1) as day from revlog where cid in
#     (select id from cards where did in (1435088749676))
# - returns all days with reviews for all cards for deck Español
# - days 1 for today, 0 for yesterday, negative for more past days

# select (cast((id/1000 - 1534543200 # cutoff #) / 86400.0 as int)+1) as day from revlog where cid in
#     (select id from cards where did in (1435088749676))
# group by day order by day
# - returns distinct days with reviews for all cards for deck Español
# - days 1 for today, 0 for yesterday, negative for more past days

# select count(), abs(min(day)) from
#     (select (cast((id/1000 - 1534543200 # cut #) / 86400.0 as int)+1) as day from revlog where cid in
#         (select id from cards where did in (1435088749676))
#     group by day order by day)
# - returns count of all days with any reviews and how many days ago the first review was done (when reviewing started)
