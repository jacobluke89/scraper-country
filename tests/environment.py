import os
import uuid
from typing import Union

from behave.runner import Context

from database_manager.connection import DBManager
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

def get_database_name(context: Context) -> str | None:
    query = "SELECT current_database();"
    try:
        with context.db_manager.get_cursor() as cursor:
            cursor.execute(query)
            db_name = cursor.fetchone()[0]
            if not db_name:
                print("db not found!")
                raise
            return db_name
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return
    except Exception as e:
        print(f"General Exception: {e}")
        return


def create_tables(db, db_manager: DBManager):

    with db_manager.get_cursor() as cursor:
        try:
            create_schema = f"CREATE SCHEMA IF NOT EXISTS {db};"
            cursor.execute(create_schema)
            logger_table = f"""
                CREATE TABLE IF NOT EXISTS {db}.logger (
                    id SERIAL PRIMARY KEY,
                    function_name VARCHAR(255),
                    date_time TIMESTAMP NOT NULL,
                    error_level INTEGER NOT NULL,
                    level_name VARCHAR(50) NOT NULL,
                    info TEXT NOT NULL
                );
                """
            cursor.execute(logger_table)
            print("Created tables.")
        except Exception as e:
            print(f"FAILED : {e}")

def setup_database(context: Context, tag: str):

    os.makedirs('tmp/temporary_database', exist_ok=True)
    if not hasattr(context, "temp_databases"):
        context.temp_databases = {}
    db_name = extract_tag_info(tag)
    unique_db_name = f"temp_{db_name}_{uuid.uuid4().hex}"
    try:
        conn = psycopg2.connect(user=user, password=pw, host=host)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cursor:
            try:
                cursor.execute(f"CREATE DATABASE {unique_db_name};")
                print(f"Created database: {unique_db_name}")
                attr_name = f"{unique_db_name}_temp_db"
                if not hasattr(context, attr_name):
                    setattr(context, f"{unique_db_name}_temp_db", [])
                temp_db_list = getattr(context, attr_name)
                temp_db_list.append(unique_db_name)
            except DuplicateDatabase as e:
                if "already exists" in str(e):
                    print(f"Skipping {unique_db_name} database creation because it already exists..")
                else:
                    raise
    except Exception as e:
        print(f"Exception raised:  {e}")
    db_manager = DBManager(unique_db_name, user, pw, host)
    create_tables(unique_db_name, db_manager)
    # Now connect to the new test database
    context.db_manager = db_manager

def teardown_database(context: Context):
    db_name = get_database_name(context)
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
    if re.match(r'^setup_.*_database$', tag):
        print("Setting up database...")
        setup_database(context, tag)

def after_tag(context: Context, tag: str):
    if re.match(r'^teardown_.*_database$', tag):
        print("Tearing down database...")
        teardown_database(context)
