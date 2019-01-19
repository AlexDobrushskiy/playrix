import csv
from datetime import datetime, timedelta
from collections import defaultdict

START = datetime(year=2016, month=5, day=2)
END = datetime(year=2016, month=5, day=10)

PURCHASES_FILENAME = 'purchases.csv'
INSTALLS_FILENAME = 'installs.csv'
TS_FORMAT = '%Y-%m-%d %H:%M:%S'
APP_TYPE_2 = '2'

INSTALL_TS_IDX = 0
INSTALL_APP_IDX = 1
INSTALL_COUNTRY_IDX = 2

PURCHASE_TS_IDX = 0
PURCHASE_APP_IDX = 1
PURCHASE_COUNTRY_IDX = 2
PURCHASE_INSTALL_TS_IDX = 3
PURCHASE_REVENUE_IDX = 4

installs = defaultdict(int)

with open(INSTALLS_FILENAME) as installs_csv:
    i_reader = csv.reader(installs_csv, delimiter=',')

    next(i_reader)  # skip the header
    for row in i_reader:
        install_ts = datetime.strptime(row[INSTALL_TS_IDX], TS_FORMAT)
        if START <= install_ts < END and row[INSTALL_APP_IDX] == APP_TYPE_2:
            installs[row[INSTALL_COUNTRY_IDX]] += 1

# revenue = dict.fromkeys(range(1,11), defaultdict(int))
revenue = {i: defaultdict(int) for i in range(1, 11)}
with open(PURCHASES_FILENAME) as purchases_csv:
    p_reader = csv.reader(purchases_csv, delimiter=',')

    next(p_reader)  # skip the header
    for row in p_reader:
        install_ts = datetime.strptime(row[PURCHASE_INSTALL_TS_IDX], TS_FORMAT)
        if START <= install_ts < END and row[1] == APP_TYPE_2:
            revenue_ts = datetime.strptime(row[PURCHASE_TS_IDX], TS_FORMAT)
            for i in range(10, 0, -1):
                if timedelta(days=i-1) < revenue_ts-install_ts <= timedelta(days=i):
                    for j in range(10, i-1, -1):
                        revenue[j][row[PURCHASE_COUNTRY_IDX]] += float(row[PURCHASE_REVENUE_IDX])

with open('result.csv', 'w') as result:
    result_writer = csv.writer(result, delimiter=',')
    result_writer.writerow(['country', 'installs'] + ['RPI{}'.format(i) for i in range(1, 11)])
    for country in installs:
        installs_per_country = installs[country]
        rpi_1_10 = [revenue[i][country]/installs_per_country for i in range(1, 11)]
        result_writer.writerow([country, installs_per_country]+rpi_1_10)
