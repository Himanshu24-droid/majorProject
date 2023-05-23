from flask import (
    Blueprint, g, redirect, url_for, render_template, request, flash, session
)
from major.db import get_db
from major.auth import login_required
from major.extensions import sp, q, dic
from major.recommendations import recommend_songs_by_similarity, recommend_songs_by_artist
from mysql.connector import IntegrityError
bp = Blueprint('site', __name__)

@bp.route('/')
def index():
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
    cur.execute(
        "SELECT DISTINCT name FROM playlist WHERE user_id=%s",
        (g.user[0],)
    )
    playlists=cur.fetchall()
    if request.method=='POST':
        if 'search' in request.form:
            query=request.form['search']
            song=sp.search(query,type='track')
            temp = song['tracks']['items']
            dic['song_id']=temp[0]['id']
            q.clear()
            rec = recommendations([temp[0]['id']], [temp[0]['artists'][0]['id']])
            q.append([rec['tracks'][0]['album']['images'][0]['url'],rec['tracks'][0]['name'],rec['tracks'][0]['artists'][0]['name'],rec['tracks'][0]['id']])
            return render_template('site/search.html', temp=temp,playlists=playlists)
        elif 'rate' in request.form:
            rating=request.form['rate']
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
        elif 'pl' in request.form:
            pl = request.form.get('pl')
            
            cur.execute(
                "SELECT id FROM playlist WHERE name=%s and user_id=%s",
                (pl,g.user[0],)
            )
            
            pl_id = cur.fetchone()[0]
            try:
                cur.execute(
                    "INSERT INTO song(id,playlist_id) VALUES(%s,%s)",
                    (dic['song_id'],pl_id,)
                )
                db.commit()
            except IntegrityError:
                flash("Song is already added in playlist.")
            else:
                return redirect(url_for('site.search'))
                
    return render_template('site/search.html',playlists=playlists)

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
    # cur.execute(
    #     "SELECT DISTINCT name FROM playlist WHERE user_id=%s",
    #     (g.user[0],)
    # )
    cur.execute(
        "SELECT * FROM playlist WHERE user_id=%s",
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

@bp.route('/playlist/<id>', methods=('GET','POST'))
@login_required
def pl(id):
    db=get_db()
    cur=db.cursor()
    cur.execute(
        "SELECT id FROM song WHERE playlist_id=%s",
        (id,)
    )
    playlist_songs=cur.fetchall()
    return render_template('site/pl.html',songs=playlist_songs)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    db=get_db()
    cur=db.cursor()
    cur.execute(
        "SELECT DISTINCT name FROM playlist WHERE user_id=%s",
        (g.user[0],)
    )
    playlists=cur.fetchall()

    return render_template('site/add.html',playlists=playlists)