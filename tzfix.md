- `revlog.id` is timestamp in millis since epoch.
- All date range filtering is therefore done based on `revlog.id`.

1. Sync everywhere.
1. Find missing day using Anki statistics view ('Calendar' section).
1. Turn off Anki.
1. Backup the database:
    ```shell
    cp ~/Library/Application\ Support/Anki2/<profile>/collection.anki2 collection.anki2.bak
    ```
1. Copy the database:
    ```shell
    cp ~/Library/Application\ Support/Anki2/<profile>/collection.anki2 .
    ```
1. Select review datetime and `id` around the missing day.
    ```sql
    select
      datetime(round(id / 1000), 'unixepoch', 'localtime') as datetime,
      id
    from revlog
    where
      cid in (select id from cards where did = 1435088749676)
    and
      <id/datetime range, e.g.>
      id >= 1647471600000 and id <= 1647730800000
    order by id
    ```
1. Pick ids to move to the previous / next day based on review datetime (add or
   subtract hours from `revlog.id` to move).
1. Simulate how it would work.
    ```sql
    select
      datetime(round(id / 1000), 'unixepoch', 'localtime') as datetime_orig,
      <changed datetime, e.g. subtract 8 hours>
      datetime(round(id  / 1000) - 3600 * 8, 'unixepoch', 'localtime') as datetime_new,
      id
    from revlog
    where
      cid in (select id from cards where did = 1435088749676)
    and
      <id/datetime range, e.g.>
      id >= 1647655200000 and id <= 1647723600000
    order by id
    ```
1. Update `revlog.id`s to change review datetimes.
    ```sql
    update revlog
      <update chosen timestamps, e.g. subtract 8 hours>
      set id = id - 3600 * 1000 * 8
    where
      cid in (select id from cards where did = 1435088749676)
    and
      <id/datetime range, e.g.>
      id >= 1647655200000 and id <= 1647723600000
    ```
1. Copy the updated database back:
    ```shell
    cp collection.anki2 ~/Library/Application\ Support/Anki2/<profile>
    ```
1. Check in 'Calendar' section in statistics whether missing days are fixed.
1. Force upload local database in Anki.
1. Sync everywhere.
