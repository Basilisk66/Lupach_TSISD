import os
from datetime import datetime

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_conn():
    """Открывает соединение с БД. Параметры берём из переменных окружения."""
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def parse_time(value):
    """Проверяет, что строка имеет вид чч:мм. Возвращает строку или None."""
    try:
        return datetime.strptime(value, "%H:%M").strftime("%H:%M")
    except (ValueError, TypeError):
        return None


@app.get("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        return jsonify(status="ok")
    except Exception as e:
        return jsonify(status="error", detail=str(e)), 500


@app.get("/stops")
def list_stops():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name FROM stops ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.post("/stops")
def add_stop():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify(error="Нужно поле name"), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO stops (name) VALUES (%s) RETURNING id", (name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify(id=new_id, name=name), 201


@app.post("/trips")
def add_trip():
    """Добавить рейс: номер маршрута, остановка, время отправления."""
    data = request.get_json(silent=True) or {}
    route = (data.get("route_number") or "").strip()
    stop_id = data.get("stop_id")
    dep = parse_time(data.get("departure_time"))

    if not route or not isinstance(stop_id, int) or dep is None:
        return jsonify(
            error="Нужны route_number (строка), stop_id (число), "
            "departure_time (формат чч:мм)"
        ), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM stops WHERE id = %s", (stop_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify(error="Остановка не найдена"), 404

    cur.execute(
        "INSERT INTO trips (route_number, stop_id, departure_time) "
        "VALUES (%s, %s, %s) RETURNING id",
        (route, stop_id, dep),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify(
        id=new_id, route_number=route, stop_id=stop_id, departure_time=dep
    ), 201


@app.get("/stops/<int:stop_id>/next")
def next_trips(stop_id):
    """Ближайшие рейсы по остановке.
    ?after=чч:мм - от какого времени считать (по умолчанию - сейчас)
    ?limit=N     - сколько рейсов вернуть (по умолчанию стоит 5)
    """
    after = request.args.get("after")
    if after is None:
        after = datetime.now().strftime("%H:%M")
    elif parse_time(after) is None:
        return jsonify(error="after должен быть в формате ЧЧ:ММ"), 400

    try:
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return jsonify(error="limit должен быть числом"), 400

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT name FROM stops WHERE id = %s", (stop_id,))
    stop = cur.fetchone()
    if stop is None:
        conn.close()
        return jsonify(error="Остановка не найдена"), 404

    cur.execute(
        "SELECT id, route_number, to_char(departure_time, 'HH24:MI') AS departure_time "
        "FROM trips WHERE stop_id = %s AND departure_time >= %s "
        "ORDER BY departure_time LIMIT %s",
        (stop_id, after, limit),
    )
    trips = cur.fetchall()
    conn.close()
    return jsonify(stop=stop["name"], after=after, trips=trips)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
