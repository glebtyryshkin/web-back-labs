import random
from flask import Blueprint, render_template, request, jsonify, session, url_for
from flask_login import current_user

lab9 = Blueprint('lab9', __name__)

GIFT_FILES = [
    "lab9/gifts/gift1.png",
    "lab9/gifts/gift2.png",
    "lab9/gifts/gift3.png",
    "lab9/gifts/gift4.png",
    "lab9/gifts/gift5.jpg",
    "lab9/gifts/gift6.jpg",
    "lab9/gifts/gift7.png",
    "lab9/gifts/gift8.jpg",
    "lab9/gifts/gift9.jpg",
    "lab9/gifts/gift10.jpg",
]

BOX_COUNT = len(GIFT_FILES) 
OPENED = [False] * BOX_COUNT

# какие коробки "только для авторизованных"
AUTH_ONLY = {0, 3, 7} 

# глобально храним, какие коробки уже пустые (для всех пользователей)
OPENED = [False] * BOX_COUNT

MESSAGES = [
    ("С Новым годом!", "Пусть сбудется то, что важно именно тебе!"),
    ("Ура!", "Желаю сил, удачи и хороших людей рядом."),
    ("Счастья!", "Пусть год будет спокойным и продуктивным."),
    ("Успехов!", "Пусть учёба/работа идут легко и в кайф."),
    ("Тепла!", "Пусть дома всегда будет уютно."),
    ("Вдохновения!", "Пусть будут идеи и желание их реализовать."),
    ("Здоровья!", "Пусть энергии хватает на всё."),
    ("Денег!", "Пусть доходы растут, а траты радуют."),
    ("Побед!", "Пусть год принесёт новые достижения."),
    ("Радости!", "Пусть будет больше поводов улыбаться."),
]


def _ensure_layout():
    """
    Случайные позиции коробок, но фиксированные для пользователя:
    сохраняем layout в session и не меняем при обновлении страницы.
    """
    if "lab9_layout" not in session:
        layout = []
        for i in range(BOX_COUNT):
            x = random.randint(5, 88)   # %
            y = random.randint(18, 82)  # %
            r = random.randint(-12, 12) # deg
            layout.append({"x": x, "y": y, "r": r})
        session["lab9_layout"] = layout


def _box_img(i: int) -> str:
    return url_for("static", filename=f"lab9/boxes/box{i+1}.png")


def _gift_img(i: int) -> str:
    return url_for("static", filename=GIFT_FILES[i])


@lab9.route("/lab9/")
def main():
    _ensure_layout()
    opened_count = session.get("lab9_opened_count", 0)
    remaining = OPENED.count(False)

    return render_template(
        "lab9/index.html",
        box_count=BOX_COUNT,
        layout=session["lab9_layout"],
        opened=OPENED,
        auth_only=AUTH_ONLY,
        is_auth=current_user.is_authenticated,
        opened_count=opened_count,
        remaining=remaining,
        boxes=[_box_img(i) for i in range(BOX_COUNT)],
    )


@lab9.route("/lab9/api/open", methods=["POST"])
def api_open():
    data = request.get_json(silent=True) or {}
    box_id = data.get("box_id")

    if box_id is None or not isinstance(box_id, int):
        return jsonify({"ok": False, "error": "Некорректный box_id"}), 400
    if box_id < 0 or box_id >= BOX_COUNT:
        return jsonify({"ok": False, "error": "Некорректный box_id"}), 400

    # доп. задание
    if box_id in AUTH_ONLY and not current_user.is_authenticated:
        return jsonify({
            "ok": False,
            "error": "Этот подарок доступен только авторизованным пользователям.",
            "remaining": OPENED.count(False),
            "opened_count": session.get("lab9_opened_count", 0)
        }), 401

    opened_count = session.get("lab9_opened_count", 0)
    if opened_count >= 3:
        return jsonify({
            "ok": False,
            "error": "Можно открыть не более 3 подарков.",
            "remaining": OPENED.count(False),
            "opened_count": opened_count
        }), 403

    if OPENED[box_id]:
        return jsonify({
            "ok": False,
            "error": "Эта коробка уже пустая.",
            "remaining": OPENED.count(False),
            "opened_count": opened_count
        }), 409

    OPENED[box_id] = True
    session["lab9_opened_count"] = opened_count + 1

    title, text = MESSAGES[box_id]
    gift = {
        "title": title,
        "text": text,
        "img": _gift_img(box_id),
    }

    return jsonify({
        "ok": True,
        "gift": gift,
        "remaining": OPENED.count(False),
        "opened_count": session["lab9_opened_count"]
    })


@lab9.route("/lab9/api/santa", methods=["POST"])
def api_santa():
    # доп. задание: кнопка только для авторизованных
    if not current_user.is_authenticated:
        return jsonify({"ok": False, "error": "Только для авторизованных"}), 401

    for i in range(BOX_COUNT):
        OPENED[i] = False

    # сбросить счётчик открытий у текущего пользователя
    session["lab9_opened_count"] = 0

    return jsonify({
        "ok": True,
        "remaining": OPENED.count(False),
        "opened_count": session.get("lab9_opened_count", 0)
    })
