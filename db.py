import psycopg2
from datetime import datetime
import pandas as pd

def json_to_postgres(_name, _where, _listings_detail):
    listing = _listings_detail
    date = datetime.now()
    try:
        con = psycopg2.connect(
            host="database-1.ciqncuyyyscf.sa-east-1.rds.amazonaws.com",
            database="investrealty_ai_db1",
            user="postgres",
            password="valor40740"
        )
        cur = con.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('{}'.format(_name),))

        if bool(cur.rowcount):
            print('Table Already Exists')
        else:
            try:
                cur.execute("CREATE TABLE {} (id serial PRIMARY KEY, local text, type text,"
                            "preco int, iptu integer, condominio integer, titulo text, description text, amen text,"
                            "address text, area_tot int, area_util int, banheiros int, vagas int, quartos int, "
                            "suites int,""imob text, url text, latitude text, longitude text, "
                            "date timestamptz);".format(_name))
                con.commit()
                print('Table Successfully created on PostgreSQL')
            except:
                print("Couldn't create datatable")
        for i in range(0, len(listing)):
            temp = listing[i]
            try:
                insert_query = """ INSERT INTO {} (local, type, preco, iptu, condominio, titulo, description, 
                                    amen, address, area_tot, area_util, banheiros, vagas, quartos, suites, imob, 
                                    url, latitude, longitude, date) VALUES ('{}', '{}', {}, {}, {}, '{}', '{}', 
                                    '{}', '{}', '{}', {}, {}, {}, {}, {}, '{}','{}', '{}', {}, 
                                    '{}')""".format(_name, _where, temp['type'],
                                                    temp['preco'], temp['iptu'], temp['condominio'],
                                                    temp['titulo'].replace("'", ""),
                                                    temp['desc'].replace("'", ""),
                                                    temp['amen'].replace("'", ""), temp['end'].replace("'", ""),
                                                    temp['area_tot'], temp['area_util'],
                                                    temp['banheiros'], temp['vagas'],
                                                    temp['quartos'], temp['suites'],
                                                    temp['imob'].replace("'", ""), temp['url'],
                                                    temp['latitude'], temp['longitude'], date)
                cur.execute(insert_query)
                con.commit()
                print('-- Captured -- Imóvel {}'.format(i))
            except:
                print('-- ERROR -- Imóvel {}'.format(i))
                continue

    except(Exception, psycopg2.Error) as error:
        print("Couldn't establish connection to datatable", error)

    finally:
        if con:
            cur.close()
            con.close()
            print('Connection Closed')





# import psycopg2
# con = psycopg2.connect(
#     host="database-1.ciqncuyyyscf.sa-east-1.rds.amazonaws.com",
#     database="investrealty_ai_db1",
#     user="postgres",
#     password="valor40740"
# )
# cur = con.cursor()
# cur.execute('DROP TABLE wimoveis CASCADE')
# con.commit()