from pymongo import MongoClient

def delete_specific_databases(pattern):
    """특정 이름 패턴에 따라 데이터베이스 삭제"""
    client = MongoClient("mongodb://localhost:27017/")
    databases = client.list_database_names()

    for db_name in databases:
        # 패턴에 맞는 데이터베이스만 삭제
        if pattern in db_name:
            client.drop_database(db_name)
            print(f"Deleted database: {db_name}")

# 메가박스 관련 데이터베이스 삭제
delete_specific_databases("메가박스")
