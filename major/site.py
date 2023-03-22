from flask import(
    Blueprint,g,redirect,url_for,render_template
)
from major.db import get_db
bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    db=get_db()
    cur=db.cursor()
    cur.execute(
        "SELECT * FROM user"
    )
    users=cur.fetchall()
    db.close()
    return render_template('site/index.html',users=users)
