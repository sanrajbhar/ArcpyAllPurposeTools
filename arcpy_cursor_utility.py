#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sri00571
#
# Created:     07/03/2018
# Copyright:   (c) sri00571 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def search_cursor(cursor):
    """
    Enables named fields in an arcpy.da.SearchCursor.

    Use:
    ```
    field_acres = {}
    with arcpy.da.SearchCursor(
        dataset,
        ("FIELD1", "FIELD2", "SHAPE@"),
        "FIELD2 > 2"
    ) as rows:
        for row in utils.search_cursor(rows):
            if row[0] not in field_acres:
                field_acres[row.FIELD1] = set()
            field_acres[row.FIELD1].add((row.FIELD2, row["SHAPE@"]))
    ```
    """
    return _name_cursor(cursor)


def update_cursor(cursor):
    """
    Enables named fields in an arcpy.da.UpdateCursor.

    Use:
    ```
    with arcpy.da.UpdateCursor(
        dataset,
        ("FIELD1", "FIELD2"),
        "FIELD1 > 2"
    ) as rows:
        for row in utils.update_cursor(rows):
            row.FIELD1 = 34.7
            row.FIELD2 = 1
            rows.updateRow(row.values())
    ```
    """
    return _name_cursor(cursor)


def insert_cursor(cursor):
    """
    Enables named fields in an arcpy.da.InsertCursor.

    Use:
    ```
    with arcpy.da.InsertCursor(
        dataset,
        ("FIELD1", "FIELD2")
    ) as rows:
        for index in xrange(0, 10):
            row = utils.insert_cursor(rows)
            row.FIELD1 = 34.7
            row.FIELD2 = 1
            rows.insertRow(row.values())
    ```
    """
    if isinstance(cursor, arcpy.da.InsertCursor):
        return MutableNamedTuple(
            zip(cursor.fields, [None for field in cursor.fields])
        )


def _name_cursor(cursor):
    """
    Private generator to enable named fields in an arcpy.da cursor
    (SearchCursor or UpdateCursor).

    Please use search_cursor(), update_cursor(), and insert_cursor().
    """
    if (
        isinstance(cursor, arcpy.da.SearchCursor) or
        isinstance(cursor, arcpy.da.UpdateCursor)
    ):
        for row in cursor:
            yield MutableNamedTuple(zip(cursor.fields, row))


class MutableNamedTuple(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        super(MutableNamedTuple, self).__init__(*args, **kwargs)
        self._initialized = True

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized'):
            if hasattr(self, name):
                super(MutableNamedTuple, self).__setitem__(name, value)
            else:
                raise AttributeError(name)
        else:
            super(MutableNamedTuple, self).__setattr__(name, value)