from lib import read_credentials, read_member_data, authenticate_user
from lib import create_database_and_table, import_member_data
from lib import display_all_records, add_record, modify_record
from lib import search_by_phone, delete_all_records


def main():
    pass_file_path = 'pass.json'
    member_data_file_path = 'members.txt'
    db_path = 'wanghong.db'

    credentials = read_credentials(pass_file_path)
    username = input("請輸入帳號：")
    password = input("請輸入密碼：")

    if authenticate_user(credentials, username, password):
        print("\n---------- 選單 ----------")
        print("0 / Enter 離開")
        print("1 建立資料庫與資料表")
        print("2 匯入資料")
        print("3 顯示所有紀錄")
        print("4 新增記錄")
        print("5 修改記錄")
        print("6 查詢指定手機")
        print("7 刪除所有記錄")
        print("--------------------------")

        while True:
            choice = input("請輸入您的選擇 [0-7]: ")

            if choice == '0':
                print("程式結束")
                break
            elif choice == '1':
                create_database_and_table(db_path)
                print("=>資料庫已建立")
            elif choice == '2':
                member_data = read_member_data(member_data_file_path)
                import_member_data(db_path, member_data)
                print(f"=>異動 {len(member_data)} 筆記錄")
            elif choice == '3':
                display_all_records(db_path)
            elif choice == '4':
                name = input("請輸入姓名: ")
                gender = input("請輸入性別: ")
                phone = input("請輸入手機: ")
                add_record(db_path, name, gender, phone)
            elif choice == '5':
                name = input("請輸入想修改記錄的姓名: ")
                new_gender = input("請輸入要改變的性別: ")
                new_phone = input("請輸入要改變的手機: ")
                modify_record(db_path, name, new_gender, new_phone)
            elif choice == '6':
                search_phone = input("請輸入想查詢記錄的手機: ")
                search_by_phone(db_path, search_phone)
            elif choice == '7':
                delete_all_records(db_path)
            else:
                print("=>無效的選擇")

    else:
        print("=>帳密錯誤，程式結束")


if __name__ == "__main__":
    main()
