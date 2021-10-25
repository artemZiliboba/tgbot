import psycopg2
from psycopg2 import Error


def get_db_data(db, db_user, db_pass, db_host, db_port, tag):
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
                 "cars_desc cd on cn.label = cd.label join car_detail cd2 on cn.label = rtrim(substring(cd2.label, 4)," \
                 "'_a')  where cn.images_yn = 'Y' and cn.publish_yn = 'N' order by random() limit 1"
        # order by random() limit 1 #and cn.publish_yn = 'N'
        cursor.execute(select)
        rec = cursor.fetchall()

        for row in rec:
            head = "*" + row[0] + "*\n" + hash_tag(row[0], tag) + "\n"
            length = str_to_int(row[1]) + " → длина"
            width = str_to_int(row[2]) + " → ширина"
            height = str_to_int(row[3]) + " → высота"
            mass = str_to_int(row[4]) + " → масса"
            all_details = "`" + length + width + height + mass + "`"
            return head + all_details + "\n\n" + row[5]
    except (Exception, Error) as error:
        print("Error with work Postgre : ", error)
    finally:
        if con:
            cursor.close()
            con.close()
            print("Connection was closed")


def str_to_int(row):
    row = str(row)
    return "\n" + row


def get_tags(db, db_user, db_pass, db_host, db_port):
    try:
        con = psycopg2.connect(
            database=db,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
        )
        cursor = con.cursor()
        select = "select ct.tag_insta from car_tags ct where ct.tag_id = 1"
        cursor.execute(select)
        tags = cursor.fetchone()[0]

        return tags
    except (Exception, Error) as error:
        print("Error with work Postgre : ", error)
    finally:
        if con:
            cursor.close()
            con.close()
            print("Connection was closed")


def hash_tag(row, tag):
    if tag == 0:
        label = row.split('\n', 1)[0]
        label = label.split(' ', 1)[0]
        return '#' + label.lower()
    return ''


def update_publish_yn(db, db_user, db_pass, db_host, db_port, grade):
    try:
        con = psycopg2.connect(
            database=db,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
        )
        cursor = con.cursor()
        grade = grade.replace("'", "''")
        sql = "update car_name set publish_yn = 'Y' where grade = '" + grade + "'"
        print(sql)
        cursor.execute(sql)
        con.commit()
        return 'UPDATED GRADE' + grade
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if con is not None:
            con.close()


def insert_log(db, db_user, db_pass, db_host, db_port, chat_id, message):
    try:
        con = psycopg2.connect(
            database=db,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
        )
        cursor = con.cursor()
        sql = "insert into logs_req (CHAT_ID, \"MESSAGE_TXT\") values (" + chat_id + ",'" + message + "')"
        print(sql)
        cursor.execute(sql)
        con.commit()
        return 'XXX'
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if con is not None:
            con.close()
