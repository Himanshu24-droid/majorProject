import mysql.connector
from flask import g,current_app
import click
import os

def get_connection():
    if 'db' not in g:
        g.db=mysql.connector.connect(
            host=os.environ.get('host'),
            user=os.environ.get('user'),
            password=os.environ.get('password')
        )
        # print('Connection established.....')
    return g.db

def get_db():
    db=mysql.connector.connect(
        host=os.environ.get('host'),
        user=os.environ.get('user'),
        password=os.environ.get('password'),
        database='major'
    )
    # print('Connection established.....')
    return db

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS major")
    cursor.execute("CREATE DATABASE major")
    conn.commit()
    conn.close()

    db=get_db()
    cursor=db.cursor()
    with current_app.open_resource('schema.sql','r') as f:
        schema = f.read()

    for stmnt in schema.split(';'):
        if stmnt!="":
            cursor.execute(stmnt)
            
    db.commit()
    db.close()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initialized the database")

def init_app(app):
    app.cli.add_command(init_db_command)