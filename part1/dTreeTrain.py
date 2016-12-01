def divideset(rows, column, value):
    set1 = [row for row in rows if row[column] >= value]
    set2 = [row for row in rows if not row[column] >= value]
    return (set1, set2)