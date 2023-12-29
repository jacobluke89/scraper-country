import os
import uuid
from typing import Union

from behave.runner import Context
from utils.globals import user, pw, host
import psycopg2
from psycopg2.errors import DuplicateDatabase
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import re

def extract_tag_info(tag: str) -> Union[str, None]:

    pattern = r"setup_([a-zA-Z0-9_]+)_database"

    match = re.match(pattern, tag)
    if match:
        part = match.group(1)
        return part

    return None

def setup_database(context: Context, tag: str):

    os.makedirs('tmp/temporary_database', exist_ok=True)
    if not hasattr(context, 'temp_databases'):
        context.temp_databases = {}
    db_name = extract_tag_info(tag)
    unique_db_name = f"temp_{db_name}_{uuid.uuid4().hex}"
    global conn
    try:
        conn = psycopg2.connect(user=user, password=pw, host=host)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cursor:
            try:
                cursor.execute(f"CREATE DATABASE {unique_db_name};")
                print(f'Created database: {unique_db_name}')
                attr_name = f"{unique_db_name}_temp_db"
                if not hasattr(context, attr_name):
                    setattr(context, f"{unique_db_name}_temp_db", [])
                temp_db_list = getattr(context, attr_name)
                temp_db_list.append(unique_db_name)
            except DuplicateDatabase as e:
                if "already exists" in str(e):
                    print(f'Skipping {unique_db_name} database creation because it already exists..')
                else:
                    raise
    finally:
        conn.close()

    # Now connect to the new test database
    context.db_conn = psycopg2.connect(dbname=unique_db_name, user=user, password=pw, host=host)

def teardown_database(context: Context):
    query = "SELECT current_database();"

    with context.db_conn.cursor() as cursor:
        cursor.execute(query)
        db_name = cursor.fetchone()[0]
        if db_name:
            print(f'RESULT IS... {db_name}')

    conn = psycopg2.connect(dbname="postgres", user=user, password=pw, host=host)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                  AND pid <> pg_backend_pid();
            """)
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
            print(f"Database {db_name} dropped.")
    except Exception as e:
        print(f"Error dropping database {db_name}: {e}")
    finally:
        conn.close()



def before_tag(context: Context, tag):
    if  re.match(r'^setup_.*_database$', tag):
        print("Setting up database...")
        setup_database(context, tag)

def after_tag(context: Context, tag: str):
    if  re.match(r'^teardown_.*_database$', tag):
        print("Tearing down database...")
        teardown_database(context)