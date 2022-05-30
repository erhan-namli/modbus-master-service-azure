from asyncio.windows_events import NULL
from pickle import NONE
import pandas as pd
import sqlite3

conn = sqlite3.connect('test_database')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS deviceRegisters (ParameterNo, Description, RegisterValue, RegisterFunction, RegisterId, DeviceIp)')
conn.commit()

xl_file = pd.read_excel("webarayuz.xlsx", sheet_name="Sheet1")

df = pd.DataFrame(xl_file)

df['RegisterFunction'].replace({'Sadece okunabilir' : 'Readable', 'Yazılabilir':'Writable'}, inplace=True)

df['RegisterId'] = df['RegisterId'].str.extract('(\d+)', expand=False)

for i in df['RegisterValue']:
    df['RegisterValue'].replace({i:None}, inplace=True)

print(df['RegisterValue'])

df.to_sql('deviceRegisters', conn, if_exists='replace', index = False)


