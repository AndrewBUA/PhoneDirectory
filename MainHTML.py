# MainHTML.py
from flask import Flask, render_template, request, g, redirect, url_for, jsonify
import re
import DirectoryDB as db

app = Flask(__name__)


# --- Database Connection Management ---
def get_db():
    if 'db' not in g:
        g.db = db.get_db_connection()
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db_conn = g.pop('db', None)
    if db_conn is not None:
        db_conn.close()


# --- Web Routes ---

@app.route('/', methods=['GET'])
def homepage():
    """Renders the homepage with all property records."""
    conn = get_db()
    all_records = db.all_records(conn)
    return render_template("Directory.html", DirectoryTable=all_records)


@app.route('/live_search')
def live_search():
    """
    Parses a user's search query, gets results from the database,
    and returns them as JSON.
    """
    search_string = request.args.get('query', '').strip()
    search_criteria = {}

    pattern = re.compile(r'(\w+):((?:"[^"]+")|(?:\S+))')
    matches = pattern.findall(search_string)

    if matches:
        for key, value in matches:
            clean_key = key.strip().upper()
            clean_value = value.strip().replace('"', '')
            search_criteria[clean_key] = clean_value
    elif search_string:
        search_criteria['PROPERTYNAME'] = search_string

    conn = get_db()

    if not search_criteria:
        results = db.all_records(conn)
    else:
        results = db.select_records(conn, search_criteria)


    dict_results = [dict(row) for row in results]

    # pass the clean list of dictionaries to jsonify.
    return jsonify(dict_results)


# --- Error Handler (no changes here) ---
@app.errorhandler(404)
def page_not_found(e):
    """Custom handler for 404 errors, redirects to homepage."""
    return redirect(url_for('homepage'))


if __name__ == "__main__":
    # Ensure you have run setup_database.py at least once before starting!
    app.run(debug=True)