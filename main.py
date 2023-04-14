import telebot
import sqlite3
import re

conn = sqlite3.connect('db_questions.sqlite3', check_same_thread=False)
cur = conn.cursor()


bot = telebot.TeleBot('6270406324:AAFNjaHAWGUWpDRy9HtVOq-PXkWEonOqyTs')

questionId = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, f"добро пожаловать {message.from_user.first_name} {message.from_user.last_name}!\n с какого номера хотите начать?(напишите число)")

@bot.message_handler(commands=['command1'])
def next(message):
    global questionId
    questionId += 1
    cur.execute(f"SELECT question FROM questions WHERE _id = ?;", (questionId,))
    question_row = cur.fetchone()
    if not question_row:
        bot.send_message(message.chat.id, "Вопрос с таким идентификатором не найден.")
        return

    question = re.sub(r'[^\w\s]', '', question_row[0])

    cur.execute(f"SELECT answer FROM questions WHERE _id = ?;", (questionId,))
    answer_row = cur.fetchone()
    if not answer_row:
        bot.send_message(message.chat.id, "Ответ на вопрос не найден.")
        return

    answer = re.sub(r'[^\w\s]', '', answer_row[0])

    result = f"{question}\n||{answer}||"
    print(result)
    bot.send_message(message.chat.id, result, parse_mode='MarkdownV2')

@bot.message_handler()
def message(message):
    global questionId

    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Пожалуйста, введите числовой идентификатор вопроса.")
        return

    questionId = int(message.text)

    cur.execute(f"SELECT question FROM questions WHERE _id = ?;", (questionId,))
    question_row = cur.fetchone()
    if not question_row:
        bot.send_message(message.chat.id, "Вопрос с таким идентификатором не найден.")
        return

    question = re.sub(r'[^\w\s]', '', question_row[0])

    cur.execute(f"SELECT answer FROM questions WHERE _id = ?;", (questionId,))
    answer_row = cur.fetchone()
    if not answer_row:
        bot.send_message(message.chat.id, "Ответ на вопрос не найден.")
        return

    answer = re.sub(r'[^\w\s]', '', answer_row[0])

    result = f"{question}\n||{answer}||"
    print(result)
    bot.send_message(message.chat.id, result, parse_mode='MarkdownV2')
    


bot.polling(none_stop=True)
