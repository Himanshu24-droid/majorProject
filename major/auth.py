import functools
from flask import(
    Blueprint,request,redirect,url_for,flash,render_template,session,g
)
from werkzeug.security import check_password_hash, generate_password_hash
from major.db import get_db
from mysql.connector import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        error=None

        if not email:
            error="Email is required."
        elif not password:
            error="Password is required."

        if error is None:
            try:
                cur.execute(
                    "INSERT INTO user(email,password) VALUES(%s,%s)",
                    (email,generate_password_hash(password))
                )
                db.commit()

            except IntegrityError:
                error=f"Email {email} already exists."
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        db=get_db()
        cur = db.cursor()
        error=None

        if not email:
            error="Email is required."
        elif not password:
            error="Password is required."
        
        cur.execute(
            "SELECT * FROM user WHERE email = %s",
            (email,)
        )
        user=cur.fetchone()

        if user is None:
            error="Incorrect Email."
        elif not check_password_hash(user[2], password):
            error="Incorrect Password."

        if error is None:
            session.clear()
            session['user_id']=user[0]
            return redirect(url_for('site.index'))
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')

    if user_id is None:
        g.user=None
    else:
        db=get_db()
        cur=db.cursor()
        cur.execute(
            "SELECT * FROM user WHERE id = %s",
            (user_id,)
        )
        g.user=cur.fetchone()
        

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('site.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view