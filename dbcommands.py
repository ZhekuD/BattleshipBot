import sqlite3


def context_manager(func):
    def wrap(*args, **kwargs):
        conn = sqlite3.connect('./database.sqlite3')
        curs = conn.cursor()
        result = func(curs, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrap


@context_manager
def db_data_input(cursor, update, game_data, enemy_game_data, memory='null'):
    user_id = update.message.from_user.id
    username = update.message.from_user.first_name

    result = cursor.execute(
        "SELECT id FROM users WHERE id=?",
        (user_id, )
    )
    result = result.fetchone()
    if not result:
        cursor.execute(
            """
            INSERT INTO users (id, username, data, enemy_data)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, username, game_data, enemy_game_data)
        )
    else:
        cursor.execute(
            """
            UPDATE users
            SET data=?, enemy_data=?, ai_memory=?
            WHERE id=?
            """,
            (game_data, enemy_game_data, memory, result[0])
        )


@context_manager
def db_data_output(cursor, update):
    user_id = update.message.from_user.id
    result = cursor.execute(
        "SELECT data, enemy_data, ai_memory FROM users WHERE id=?",
        (user_id, )
    ).fetchone()
    return result


@context_manager
def db_data_erase(cursor, update, victory):
    user_id = update.message.from_user.id
    cursor.execute(
        "SELECT allgames, wingames FROM users WHERE id=?",
        (user_id, )
    )

    allgames, wingames = cursor.fetchone()
    allgames += 1
    if victory:
        wingames += 1

    cursor.execute(
        """
        UPDATE users
        SET data=NULL, enemy_data=NULL, ai_memory=NULL, allgames=?, wingames=?
        WHERE id=?
        """,
        (allgames, wingames, user_id)
    )


@context_manager
def db_statistic(cursor, update):
    user_id = update.message.from_user.id
    cursor.execute(
        "SELECT allgames, wingames FROM users WHERE id=?",
        (user_id, )
    )
    result = cursor.fetchone()
    return result


@context_manager
def create_table(cursor, *args):
    cursor.execute("""CREATE TABLE users (
        id INT PRIMARY KEY, 
        username, 
        data, 
        enemy_data, 
        ai_memory DEFAULT 'null', 
        allgames INT DEFAULT 0, 
        wingames INT DEFAULT 0
    )""")
