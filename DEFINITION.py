# define columns
COLUMNS = ['primary_key']
for x in range(52):
    COLUMNS.append(('%02d' % x) + 'id')
    COLUMNS.append(('%02d' % x) + 'index')
COLUMNS.append('cost')
# defined dtypes
DTYPES = dict()
DTYPES[NAMES[0]] = 'str'
for x in range(1, 106):
    DTYPES[NAMES[x]] = 'uint8'
