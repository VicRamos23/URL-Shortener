from flask import Flask, request, redirect, url_for, render_template
import hashlib
import validators
from database import create_connection, setup_database

app = Flask(__name__)

def generate_short_url(original_url):
    return hashlib.md5(original_url.encode()).hexdigest()[:6]

def store_url(original_url, short_url):
    conn = create_connection()
    with conn:
        conn.execute("INSERT INTO urls (original, short) VALUES (?, ?)", (original_url, short_url))

def get_original_url(short_url):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT original FROM urls WHERE short=?", (short_url,))
    row = cur.fetchone()
    return row[0] if row else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not validators.url(original_url):
            return render_template('index.html', error="URL no válida. Asegúrate de incluir el esquema (http:// o https://).")
        short_url = generate_short_url(original_url)
        store_url(original_url, short_url)
        return render_template('result.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return "URL no encontrada", 404

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)

