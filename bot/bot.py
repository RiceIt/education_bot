import os, requests, json, pprint

from flask import Flask, request

from parser.config import Configuration
from parser.models import add_user, select_discipline_names_buttons, create_or_delete_discipline, \
    select_country_names_buttons, create_or_delete_country, select_degree_names_buttons, create_or_delete_degree

app = Flask(__name__)
app.config.from_object(Configuration)

DISCIPLINES = ("Arts", "Biological & Medical Sciences", "Business & Finance", "Chemical Sciences", "Earth Sciences", "Education", "Engineering", "Humanities", "Law", "Maths & Computing", "Physical Sciences", "Social Science", )


@app.route("/", methods=["GET", "POST"])
def receive_update():
    request_handler(request.json)
    return {"ok": True}


def request_handler(request_json):
    if request_json.get("message"):
        if request_json["message"]["text"] == "/start":
            add_user(chat_id=request_json["message"]["chat"]["id"])
            send_start_message(chat_id=request_json["message"]["chat"]["id"])
    elif request_json.get("callback_query"):
        if request_json["callback_query"]["data"] == "disciplines":
            send_discipline_list(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
                                 message_id=request_json["callback_query"]["message"]["message_id"],
                                 )
        elif request_json["callback_query"]["data"] == "countries":
            send_country_list(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
                              message_id=request_json["callback_query"]["message"]["message_id"],
                              )
        elif request_json["callback_query"]["data"] == "degrees":
            send_degree_list(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
                             message_id=request_json["callback_query"]["message"]["message_id"],
                             )
        # elif request_json["callback_query"]["data"] == "institutes":
        #     send_institutes_chapters(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
        #                              message_id=request_json["callback_query"]["message"]["message_id"],
        #                              )
        # elif request_json["callback_query"]["data"].startswith("chapter"):
        #     send_institutes_list(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
        #                          message_id=request_json["callback_query"]["message"]["message_id"],
        #                          text=request_json["callback_query"]["data"]
        #                          )
        elif request_json["callback_query"]["data"].startswith("Disciplines"):
            update_discipline(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
                              message_id=request_json["callback_query"]["message"]["message_id"],
                              text=request_json["callback_query"]["data"]
                              )
        elif request_json["callback_query"]["data"].startswith("Countries"):
            update_country(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
                           message_id=request_json["callback_query"]["message"]["message_id"],
                           text=request_json["callback_query"]["data"],
                           )
        elif request_json["callback_query"]["data"].startswith("Degrees"):
            update_degree(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
                          message_id=request_json["callback_query"]["message"]["message_id"],
                          text=request_json["callback_query"]["data"],
                          )
        # elif request_json["callback_query"]["data"].startswith("Institutes"):
        #     update_institute(chat_id=request_json["callback_query"]["message"]["chat"]["id"],
        #                      message_id=request_json["callback_query"]["message"]["message_id"],
        #                      text=request_json["callback_query"]["data"],
        #                      )

        answer_callback_query(request_json["callback_query"]["id"])


def send_message(method, chat_id, **kwargs):
    token = os.getenv("TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, **kwargs}
    response = requests.post(url, data=data)


def send_start_message(chat_id):
    inline_keyboard_button1 = {"text": "Disciplines", "callback_data": "disciplines"}
    inline_keyboard_button2 = {"text": "Location", "callback_data": "countries"}
    inline_keyboard_button3 = {"text": "Degree", "callback_data": "degrees"}
    # inline_keyboard_button3 = {"text": "Institutes", "callback_data": "institutes"}
    # inline_keyboard_button4 = {"text": "PhD Type", "callback_data": "type"}
    # inline_keyboard_button5 = {"text": "Funding", "callback_data": "funded"}

    inline_keyboard = {"inline_keyboard": [
        [inline_keyboard_button1, ],
        [inline_keyboard_button2, ],
        [inline_keyboard_button3, ],
        # [inline_keyboard_button3, ],
        # [inline_keyboard_button4, ],
        # [inline_keyboard_button5, ],
    ]
    }
    reply_markup = json.dumps(inline_keyboard)

    data = {"text": "Filters: ", "reply_markup": reply_markup}
    send_message("sendMessage", chat_id, **data)

# FIXME
# def send_institutes_chapters(chat_id, message_id):
#     inline_keyboard_button1 = {"text": "A-K", "callback_data": "chapter:0 97"}
#     inline_keyboard_button2 = {"text": "K-T", "callback_data": "chapter:97 86"}
#     inline_keyboard_button3 = {"text": "U", "callback_data": "chapter:183 100"}
#     inline_keyboard_button4 = {"text": "V-Z", "callback_data": "chapter:283 99"}
#     inline_keyboard = {"inline_keyboard": [
#         [inline_keyboard_button1, inline_keyboard_button2, ],
#         [inline_keyboard_button3, inline_keyboard_button4, ],
#     ]
#     }
#     reply_markup = json.dumps(inline_keyboard)
#
#     data = {"message_id": message_id, "reply_markup": reply_markup}
#     send_message("editMessageReplyMarkup", chat_id, **data)


def send_discipline_list(chat_id, message_id):
    inline_keyboard = select_discipline_names_buttons(chat_id)
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})
    data = {"message_id": message_id, "reply_markup": reply_markup}
    send_message("editMessageReplyMarkup", chat_id, **data)


def send_country_list(chat_id, message_id):
    inline_keyboard = select_country_names_buttons(chat_id)
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})
    data = {"message_id": message_id, "reply_markup": reply_markup}
    send_message("editMessageReplyMarkup", chat_id, **data)


def send_degree_list(chat_id, message_id):
    inline_keyboard = select_degree_names_buttons(chat_id)
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})
    data = {"message_id": message_id, "reply_markup": reply_markup}
    send_message("editMessageReplyMarkup", chat_id, **data)

# def send_institutes_list(chat_id, message_id, text):
#     offset, limit = text.split(':')[-1].split(' ')
#     inline_keyboard = select_institute_names_buttons(chat_id, limit, offset)
#     reply_markup = json.dumps({"inline_keyboard": inline_keyboard})
#     data = {"message_id": message_id, "reply_markup": reply_markup}
#     send_message("editMessageReplyMarkup", chat_id, **data)


def update_discipline(chat_id, message_id, text):
    discipline_name, platform = text.split(":")[1:]
    create_or_delete_discipline(chat_id, discipline_name, platform)
    inline_keyboard = select_discipline_names_buttons(chat_id)
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})

    data = {"message_id": message_id, "reply_markup": reply_markup}
    send_message("editMessageReplyMarkup", chat_id, **data)


def update_country(chat_id, message_id, text):
    country_name = text.split(":")[-1]
    print(country_name)
    create_or_delete_country(chat_id, country_name)
    inline_keyboard = select_country_names_buttons(chat_id)
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})

    data = {"message_id": message_id, "reply_markup": reply_markup}
    send_message("editMessageReplyMarkup", chat_id, **data)


def update_degree(chat_id, message_id, text):
    degree_name = text.split(":")[-1]
    print(degree_name)
    create_or_delete_degree(chat_id, degree_name)
    inline_keyboard = select_degree_names_buttons(chat_id)
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})

    data = {"message_id": message_id, "reply_markup": reply_markup}
    send_message("editMessageReplyMarkup", chat_id, **data)


# def update_institute(chat_id, message_id, text):
#     institute_name = text.split(":")[-1]
#     text = create_or_delete_institute(chat_id, institute_name)
#     inline_keyboard = select_country_names_buttons(chat_id)
#     reply_markup = json.dumps({"inline_keyboard": inline_keyboard})
#
#     data = {"message_id": message_id, "reply_markup": reply_markup}
#     send_message("editMessageReplyMarkup", chat_id, **data)


def back():
    pass


def answer_callback_query(callback_query_id):
    method = "answerCallbackQuery"
    token = os.getenv("TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"

    data = {"callback_query_id": callback_query_id}
    requests.post(url, data=data)
