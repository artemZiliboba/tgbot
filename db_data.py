import os

import psycopg2
from psycopg2 import Error


def get_db_data(db, db_user, db_pass, db_host, db_port):
    try:
        con = psycopg2.connect(
            database=db,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
        )
        cursor = con.cursor()
        select = "select cn.grade, cd2.length, cd2.width, cd2.height, cd2.mass, cd.c_desc from car_name cn join " \
                 "cars_desc cd on cn.label = cd.label join car_detail cd2 on cn.label = rtrim(ltrim(cd2.label, 'ch_'), " \
                 "'_a') order by random() limit 1"
        cursor.execute(select)
        rec = cursor.fetchall()

        for row in rec:
            head = "*" + row[0] + "*" + "\n\n"
            length = "Длина:\t" + str_to_int(row[1])
            width = "Ширина:\t" + str_to_int(row[2])
            height = "Высота:\t" + str_to_int(row[3])
            mass = "Масса:\t" + str_to_int(row[4])
            all_details = length + width + height + mass
            return head + all_details + "\n\n" + row[5]
    # cur = con.cursor().execute("select cd.label, cd.length from car_detail cd where cd.label like '%tesla%'")
    except (Exception, Error) as error:
        print("Error with work Postgre", error)
    finally:
        if con:
            cursor.close()
            con.close()
            print("Connection was closed")


def str_to_int(row):
    row = str(row)
    return row + "\n"
