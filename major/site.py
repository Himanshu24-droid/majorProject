from flask import (
    Blueprint, g, redirect, url_for, render_template, request, flash, session
)
from major.db import get_db
from major.auth import login_required
from major.extensions import sp, q, dic
from mysql.connector import IntegrityError
bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    # Get a list of seed artists and tracks
    # seed_artists = ['4fEkbug6kZzzJ8eYX6Kbbp']
    # seed_tracks = ['7fW9J3EpVWVN1ouv0slAs0']

    # # Get recommendations based on the seed artists and tracks
    # recommendations = sp.recommendations(seed_artists=seed_artists, seed_tracks=seed_tracks)
    # x = recommendations(["3USxtqRwSYz57Ewm6wWRMp"], ["4yvcSjfu4PC0CYQyLy4wSq"])
    return render_template('site/index.html')

@bp.route('/queue', methods=('GET', 'POST'))
@login_required
def queue():
    return render_template('site/queue.html',q=q)

def recommendations(song_id,artist_id):
    rec = sp.recommendations(seed_artists=artist_id,seed_tracks=song_id,limit=1)
    return rec

@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    db=get_db()
    cur=db.cursor()
    error=None
    if request.method=='POST':
        if 'search' in request.form:
            query=request.form['search']
            song=sp.search(query,type='track')
            temp = song['tracks']['items']
            dic['song_id']=temp[0]['id']
            q.clear()
            rec = recommendations([temp[0]['id']], [temp[0]['artists'][0]['id']])
            q.append([rec['tracks'][0]['album']['images'][0]['url'],rec['tracks'][0]['name'],rec['tracks'][0]['artists'][0]['name'],rec['tracks'][0]['id']])
            return render_template('site/search.html', temp=temp)
        elif 'rate' in request.form:
            rating=request.form['rate']
            if not rating:
                error="Rating is required."
            
            if error is None:
                try:
                    cur.execute(
                        "INSERT INTO ratings(rating,user_id,song_id) VALUES(%s,%s,%s)",
                        (rating,g.user[0],dic['song_id'],)
                    )
                    db.commit()
                except IntegrityError:
                    cur.execute(
                        "UPDATE ratings SET rating=%s WHERE user_id=%s and song_id=%s",
                        (rating,g.user[0],dic['song_id'],)
                    )
                    db.commit()
                else:
                    return redirect(url_for('site.search'))

            flash(error)
    return render_template('site/search.html')

@bp.route('/play/<id>', methods=('GET', 'POST'))
@login_required
def play(id):
    track = sp.track(id)
    return render_template('site/play.html',track=track)

@bp.route('/playlist', methods=('GET','POST'))
@login_required
def playlist():
    db=get_db()
    cur=db.cursor()
    cur.execute(
        "SELECT COUNT(DISTINCT name) FROM playlist WHERE user_id=%s",
        (g.user[0],)
    )
    cnt=cur.fetchone()[0]
    cur.execute(
        "SELECT DISTINCT name FROM playlist WHERE user_id=%s",
        (g.user[0],)
    )

    playlists=cur.fetchall()
    
    if request.method=='POST':
        name=request.form['name']
        cur.execute(
            "INSERT INTO playlist(name,user_id) VALUES(%s,%s)",
            (name,g.user[0])
        )
        db.commit()
        return redirect(url_for('site.playlist', cnt=cnt))
    return render_template('site/playlist.html',cnt=cnt,playlists=playlists)

@bp.route('/playlist/<name>', methods=('GET','POST'))
@login_required
def pl(name):
    return render_template('site/pl.html')

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_to_playlist():
    return render_template('site/add.html')