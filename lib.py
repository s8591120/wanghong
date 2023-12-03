import json
import sqlite3


def read_credentials(file_path):
    """
    讀取帳密檔案，返回帳號密碼的字典列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        credentials = json.load(file)
    return credentials


def read_member_data(file_path):
    """
    讀取成員資料檔案，返回成員資料的列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        member_data = [line.strip().split(',') for line in lines]
    return member_data


def authenticate_user(credentials, username, password):
    """
    驗證使用者帳密是否正確
    """
    for user in credentials:
        if user['帳號'] == username and user['密碼'] == password:
            return True
    return False


def create_database_and_table(db_path):
    """
    建立資料庫與資料表
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                iid INTEGER PRIMARY KEY AUTOINCREMENT,
                mname TEXT NOT NULL,
                msex TEXT NOT NULL,
                mphone TEXT NOT NULL
            )
        """)


def import_member_data(db_path, member_data):
    """
    將成員資料匯入資料庫
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)",
            member_data
            )


def display_all_records(db_path):
    """
    顯示所有成員紀錄
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members")
        records = cursor.fetchall()

    if not records:
        print("=>查無資料")
    else:
        print("姓名\t性別\t手機")
        print("-" * 25)
        for record in records:
            print(f"{record[1]}\t{record[2]}\t{record[3]}")


def add_record(db_path, name, gender, phone):
    """
    新增成員紀錄
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)",
            (name, gender, phone)
            )
    print("=>異動 1 筆記錄")


def modify_record(db_path, name, new_gender, new_phone):
    """
    修改成員紀錄
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE mname=?", (name,))
        record = cursor.fetchone()

        if record:
            print(f"原資料：\n姓名：{record[1]}，性別：{record[2]}，手機：{record[3]}")
            cursor.execute(
                "UPDATE members SET msex=?, mphone=? WHERE mname=?",
                (new_gender, new_phone, name)
                )
            conn.commit()

            cursor.execute("SELECT * FROM members WHERE mname=?", (name,))
            updated_record = cursor.fetchone()
            print("=>異動 1 筆記錄")
            print(f"修改後資料：\n"
                  f"姓名：{updated_record[1]}，"
                  f"性別：{updated_record[2]}，"
                  f"手機：{updated_record[3]}")
        else:
            print("=>必須指定姓名才可修改記錄")


def search_by_phone(db_path, phone):
    """
    依據手機查詢成員紀錄
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE mphone=?", (phone,))
        records = cursor.fetchall()

    if not records:
        print("=>查無資料")
    else:
        print("姓名\t性別\t手機")
        print("-" * 25)
        for record in records:
            print(f"{record[1]}\t{record[2]}\t{record[3]}")


def delete_all_records(db_path):
    """
    刪除所有成員紀錄
    """
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM members")
    print("=>異動所有記錄")
