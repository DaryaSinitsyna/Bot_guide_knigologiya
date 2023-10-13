import psycopg2
from dotenv import find_dotenv
from config_data.config import Config, load_config


config: Config = load_config(find_dotenv('.env'))

conn = psycopg2.connect(dbname=config.db.database,
                        user=config.db.db_user,
                        password=config.db.db_password,
                        host=config.db.db_host,
                        port=config.db.dp_port)
try:
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(open("database/db_tables.sql", "r", encoding='utf-8').read())
except:
    pass
finally:
    cursor.close()


def process_stop_test(user_telegram_id: int):
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"UPDATE bot_user SET status=False, current_question = 0, score = 0"
                   f"WHERE user_telegram_id={user_telegram_id}")


def add_user(user_telegram_id: int):
    try:
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(f"INSERT INTO bot_user (user_telegram_id)"
                       f"VALUES ({user_telegram_id})")

    except:
        process_stop_test(user_telegram_id)


def user_in_test(user_telegram_id: int):
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"SELECT status "
                   f"FROM bot_user "
                   f"WHERE user_telegram_id={user_telegram_id}")

    res = cursor.fetchone()[0]
    return res


def current_question(user_telegram_id: int):
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"UPDATE bot_user SET current_question = current_question + 1, status = True "
                   f"WHERE user_telegram_id={user_telegram_id};"
                   f"SELECT current_question "
                   f"FROM bot_user "
                   f"WHERE user_telegram_id={user_telegram_id}")


def get_current_question(user_telegram_id: int):
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"SELECT current_question "
                   f"FROM bot_user "
                   f"WHERE user_telegram_id={user_telegram_id}")

    return cursor.fetchone()[0]


def show_question(current_number: int):
    try:
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(f"SELECT text_question, image_path "
                       f"FROM question "
                       f"WHERE number_question={current_number}")

        question = cursor.fetchone()
        return question

    except:
        pass


def show_answers(current_number: int):
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"SELECT serial_number, text_answer "
                   f"FROM answer "
                   f"WHERE fk_question_id={current_number}")

    answers = cursor.fetchall()

    res = ''
    for number, answer in answers:
        res += f'{number}. {answer}.\n'

    return res


def get_current_question_content(user_id: int):
    get_current_quest = get_current_question(user_id)
    question = show_question(get_current_quest)
    answers = show_answers(get_current_quest)
    return question, answers


def score(user_telegram_id: int, answer_choice: str):
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(f"UPDATE bot_user SET score = score + {3 - int(answer_choice)} "
                   f"WHERE user_telegram_id={user_telegram_id}")


def result(user_telegram_id: int):
    cursor = conn.cursor()
    conn.autocommit = True

    cursor.execute(f'SELECT score '
                   f'FROM bot_user '
                   f'WHERE user_telegram_id={user_telegram_id}')
    user_score = cursor.fetchone()[0]

    cursor.execute(f'SELECT text_result, url '
                   f'FROM test_result '
                   f'WHERE score_range @> {user_score}')
    res = cursor.fetchall()
    process_stop_test(user_telegram_id)
    return res
