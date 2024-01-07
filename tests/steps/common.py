from typing import Tuple, Any


def table_exists_check(db_conn, db: str, tbl_name: str) -> Tuple[Any, bool]:
    try:
        table_exists_query = f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables 
                    WHERE table_schema = %s AND table_name = %s
                );
                """
        with db_conn.get_cursor() as cursor:
            cursor.execute(table_exists_query, (db, tbl_name,))
            val = cursor.fetchone()[0]
        return cursor, bool(val)
    except Exception as e:
        raise AssertionError(F"Database error occurred: {e}")
