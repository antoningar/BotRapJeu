import sqlite3
import settings

def create_db():
    con = sqlite3.connect(settings.DB_NAME)

    with open('assets/create.sql', 'r', encoding='utf-8') as rq:
        cur = con.cursor()
        cur.execute(rq.read())

    con.commit()
    con.close()

def insert_user(username, score):
    rq = f'insert into leaderboard values (\'{username}\', {score})'
    con = sqlite3.connect(settings.DB_NAME)
    cur = con.cursor()

    cur.execute(rq)

    con.commit()
    con.close()

def get_users():
    rq = 'select * from leaderboard order by score desc'
    con = sqlite3.connect(settings.DB_NAME)
    cur = con.cursor()

    cur.execute(rq)
    results = cur.fetchall()

    con.commit()
    con.close()
    return results


def get_top_5():
    rq = 'select * from leaderboard order by score desc limit 5'
    con = sqlite3.connect(settings.DB_NAME)
    cur = con.cursor()

    cur.execute(rq)
    results = cur.fetchall()

    con.commit()
    con.close()
    return results

def get_user(username):
    rq = f'select * from leaderboard where username like \'{username}\''
    con = sqlite3.connect(settings.DB_NAME)

    cur = con.cursor()
    cur.execute(rq)

    result = cur.fetchone()

    con.commit()
    con.close()
    return result

def update_user(username, score):
    rq = f'update leaderboard set score = {score} where username=\'{username}\''
    con = sqlite3.connect(settings.DB_NAME)
    cur = con.cursor()

    cur.execute(rq)
    cur.fetchall()

    con.commit()
    con.close()

def update_users(users, score):
    users_db = get_users()
    for user in users:
        user_db = [user_db for user_db in users_db if user_db[0] == user]
        if user_db:
            update_user(user,score + user_db[0][1])
            print(f'{user} update with score {score}')
        else:
            insert_user(user, score)
            print(f'{user} insert with score, {score}')

def delete_all():
    rq = f'delete from leaderboard'
    con = sqlite3.connect(settings.DB_NAME)
    cur = con.cursor()

    cur.execute(rq)
    cur.fetchall()

    con.commit()
    con.close()

create_db()
delete_all()
insert_user('sil2ob', 500)

insert_user('ok', 4)
insert_user('lets', 10)
insert_user('go', 25)
insert_user('cest', 30)
insert_user('parti', 40)