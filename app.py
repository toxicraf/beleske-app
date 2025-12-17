from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "notes.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.template_filter("format_datetime")
def format_datetime(value):
    if not value:
        return ""
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(str(value))
        except ValueError:
            return value
    # Primer: 15.12.2025 14:35
    return dt.strftime("%d.%m.%Y %H:%M")


@app.template_filter("preview_split")
def preview_split(value, limit=100):
    """
    Podeli tekst u više redova, svaki do `limit` karaktera,
    tako da se reči ne lome nasred (seče na poslednjem razmaku).
    Vraća listu redova.
    """
    if not value:
        return []
    text = str(value).strip()
    lines = []

    while len(text) > limit:
        cut = text.rfind(" ", 0, limit)
        if cut == -1:
            cut = limit
        lines.append(text[:cut].rstrip())
        text = text[cut:].lstrip()

    if text:
        lines.append(text)

    return lines


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL CHECK(length(note) <= 255),
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


# Initialize the database (create table if it doesn't exist)
init_db()


@app.route("/")
def index():
    sort = request.args.get("sort", "desc")
    query = (request.args.get("q") or "").strip()
    
    # Paginacija
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    per_page = 20  # Broj beleški po stranici

    order_clause = "DESC"
    if sort == "asc":
        order_clause = "ASC"

    # SQL za brojanje ukupnog broja beleški
    count_sql = "SELECT COUNT(*) as total FROM notes"
    count_params = []

    # SQL za dohvatanje beleški
    sql = "SELECT id, note, date_created FROM notes"
    params = []

    if query:
        # Ako korisnik nije uneo *, automatski dodaj * na početak i kraj
        raw_pattern = query
        if "*" not in raw_pattern:
            raw_pattern = f"*{raw_pattern}*"
        # Zameni * sa % kao u SQL LIKE
        pattern = raw_pattern.replace("*", "%")
        where_clause = " WHERE note LIKE ?"
        sql += where_clause
        count_sql += where_clause
        params.append(pattern)
        count_params.append(pattern)

    sql += f" ORDER BY date_created {order_clause}"
    
    # Dodaj LIMIT i OFFSET za paginaciju
    offset = (page - 1) * per_page
    sql += f" LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    conn = get_connection()
    cursor = conn.cursor()
    
    # Izračunaj ukupan broj beleški
    cursor.execute(count_sql, count_params)
    total_count = cursor.fetchone()["total"]
    
    # Dohvati beleške za trenutnu stranicu
    cursor.execute(sql, params)
    notes = cursor.fetchall()
    conn.close()
    
    # Izračunaj paginacione podatke
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
    
    # Ako je page veći od ukupnog broja stranica, redirect na poslednju stranicu
    if page > total_pages and total_pages > 0:
        return redirect(url_for("index", page=total_pages, sort=sort, q=query))
    
    return render_template(
        "notes_list.html",
        notes=notes,
        sort=sort,
        q=query,
        page=page,
        per_page=per_page,
        total_count=total_count,
        total_pages=total_pages,
    )


@app.route("/notes/new", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        note_text = (request.form.get("note") or "").strip()
        if not note_text:
            flash("Tekst beleške je obavezan.", "error")
            return redirect(url_for("create_note"))
        if len(note_text) > 255:
            flash("Tekst beleške mora imati najviše 255 karaktera.", "error")
            return redirect(url_for("create_note"))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (note, date_created) VALUES (?, ?)",
            (note_text, datetime.utcnow()),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("note_form.html", action="Nova beleška", note=None)


@app.route("/notes/<int:note_id>")
def note_detail(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, note, date_created FROM notes WHERE id = ?", (note_id,)
    )
    note = cursor.fetchone()
    conn.close()
    if note is None:
        flash("Beleška nije pronađena.", "error")
        return redirect(url_for("index"))
    return render_template("note_detail.html", note=note)


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, note, date_created FROM notes WHERE id = ?", (note_id,)
    )
    note = cursor.fetchone()

    if note is None:
        conn.close()
        flash("Beleška nije pronađena.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        note_text = (request.form.get("note") or "").strip()
        if not note_text:
            flash("Tekst beleške je obavezan.", "error")
            return redirect(url_for("edit_note", note_id=note_id))
        if len(note_text) > 255:
            flash("Tekst beleške mora imati najviše 255 karaktera.", "error")
            return redirect(url_for("edit_note", note_id=note_id))

        cursor.execute(
            "UPDATE notes SET note = ? WHERE id = ?",
            (note_text, note_id),
        )
        conn.commit()
        conn.close()
        flash("Beleška je uspešno izmenjena.", "success")
        return redirect(url_for("note_detail", note_id=note_id))

    conn.close()
    return render_template("note_form.html", action="Izmeni belešku", note=note)


@app.route("/notes/<int:note_id>/delete", methods=["GET", "POST"])
def delete_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, note, date_created FROM notes WHERE id = ?", (note_id,)
    )
    note = cursor.fetchone()

    if note is None:
        conn.close()
        flash("Beleška nije pronađena.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        flash("Beleška je uspešno obrisana.", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("confirm_delete.html", note=note)


if __name__ == "__main__":
    app.run(debug=True)



