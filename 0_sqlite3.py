#!/usr/bin/env python
# coding: utf-8

# # sqlite3
# Python에서는 sqlite3 라이브러리를 기본적으로 제공합니다.

# In[3]:


import sqlite3


# ## 연결 생성
# sqlite3 모듈을 사용하기 위해서는 먼저 Connection 객체를 생성하여 데이터베이스에 연결해야합니다.
# 

# In[4]:


# 원하는 파일명 지정 (존재하지 않는 파일인경우 생성됨)
con = sqlite3.connect('./database/example.db')

# 실제 파일 경로 대신 :memory: 를 넘기면 RAM에 임시로 데이터베이스가 생성됨
# con = sqlite3.connect(':memory:')


# ## SQL 실행
# Connection 객체를 생성한 다음 Cursor 오브젝트를 생성하여 SQL문을 실행할 수 있도록 합니다.

# In[5]:


# Cursor 생성
cur = con.cursor()

# 테이블이 이미 있다면 삭제
cur.execute("DROP TABLE IF EXISTS student")

# 테이블 생성
cur.execute("""
    CREATE TABLE student(
        first_name text,
        last_name text,
        age integer
    )
    """)

# 데이터 삽입
# execute 함수는 한번에 하나의 SQL문만 실행 가능
cur.execute("INSERT INTO student VALUES ('Tomas', 'Train', 10)")
cur.execute("INSERT INTO student VALUES ('Bean', 'Green', 1)")


# In[6]:


# 한번에 여러개를 실행하려고 하면 에러 발생
cur.execute("""
            INSERT INTO student VALUES ('Tomas', 'Train', 10);
            INSERT INTO student VALUES ('Bean', 'Green', 1);
            """)


# In[7]:


# 한번에 여러 SQL문을 실행하고 싶은 경우 executescript 사용하기
cur.executescript("""
    DROP TABLE IF EXISTS teacher;
    DROP TABLE IF EXISTS book;

    CREATE TABLE teacher(
        firstname,
        lastname,
        age
    );

    CREATE TABLE book(
        title,
        author,
        published
    );

    INSERT INTO book(title, author, published)
    VALUES (
        'Dirk Gently''s Holistic Detective Agency',
        'Douglas Adams',
        1987
    );
    """)


# In[8]:


# 같은 형식의 SQL문에 데이터만 바꿔서 여러번 실행하고 싶은 경우,
# executemany와 제너레이터를 조합하면 좋다
# 메모리에 모두 올라가는 적은 양의 데이터라면 그냥 리스트로 넘겨도 될듯
def data_generator():
    datas = [
                ['Bee', 'Honey', 3],
                ['Bee', 'Zig', 5], 
                ['Bob', 'Sponge', 7]
            ]
    for data in datas:
        yield data

cur.executemany("INSERT INTO student VALUES (?, ?, ?)", data_generator())
cur.execute("SELECT * FROM student")
cur.fetchall()


# ### 결과 조회
# SQL 결과를 조회하기 위해서는 Cursor 객체를 iterator로 활용하는 방법,  
# fetchone, fetchmany, fetchall 함수를 이용하는 방법이 있습니다.
# 

# In[9]:


# Cursor는 iterator객체이므로 순차적으로 값을 불러올 수 있다
cur.execute("SELECT * FROM student").rowcount

print(next(cur))
print(next(cur))


# In[10]:


# SQL 실행하면 동일한 cursor 객체를 리턴해준다
cur.execute("SELECT * FROM student") is cur


# In[11]:


# 그래서 이렇게 바로 for문에 넣는것도 가능!
for row in cur.execute("SELECT * FROM student"):
    print(row)


# fetchone, fetchmany, fetchall 함수를 이용하여 결과를 가져올 경우,  
# 이미 조회한 데이터는 다시 함수를 호출해도 조회할 수 없습니다. (다음 데이터부터 가져옴)  
# 다시 조회하고 싶다면 SQL문을 다시 실행해야합니다.

# In[12]:


# fetchone은 실행결과 중 하나의 행만 가져온다
cur.execute("SELECT * FROM student")
cur.fetchone()


# In[13]:


# 한번 더 호출해보면 그 다음 행을 가져온다
cur.fetchone()


# In[14]:


# fetchmany는 실행 결과 중 원하는 개수의 행을 가져올 수 있다
# 원하는 개수보다 적은 행이 남아있으면 남은 행만큼만 가져온다
cur.fetchmany(5)


# In[15]:


# fetchall은 실행 결과 중 남아있는 모든 행을 가져온다
# 남아있는 행이 없으면 빈 리스트 리턴
cur.fetchall()


# In[16]:


# 다시 조회하고 싶으면 SQL문을 다시 실행해야한다
cur.execute("SELECT * FROM student")
cur.fetchall()


# ### 변경사항 저장
# Connection객체의 commit함수로 변경사항을 저장할 수 있습니다.

# In[17]:


# commit으로 변경사항 저장
con.commit()

# 다시 연결한 다음 확인해보기
con.close()

con = sqlite3.connect('./database/example.db')
cur = con.cursor()

# 변경사항이 저장됐다
for row in cur.execute("SELECT * FROM student"):
    print(row)


# ## 테이블 보기 좋게 출력하기

# ### prettytable
# 이번 프로젝트에서는 prettytable 모듈을 활용했습니다.  
# pandas를 활용해도 좋겠지만 단순히 SQL 실행 결과만 확인할 것이기 때문에 prettytable로도 충분합니다.

# In[18]:


# prettytable 모듈 버전 확인
get_ipython().system('pip show prettytable | findstr Version')

# 리눅스 환경에서는 findstr 말고 grep 사용하기
# !pip show prettytable | grep Version

# 모듈 없는 경우 주석 해제하고 설치하기
# !pip install prettytable


# Python DB-API를 통해 지원되는 DB모듈의 경우 Cursor 객체를 바로 테이블로 만들 수 있습니다

# In[19]:


from prettytable import from_db_cursor

cur.execute("SELECT * FROM student")
from_db_cursor(cur)


# ### 컬럼명 (필드명)
# prettytable 모듈을 거치지 않고 특정 테이블의 컬럼명을 알고 싶은 경우 2가지 방법이 있습니다.  
# * PARAGMA 키워드로 스키마 확인하기
# * Conncetion 객체에 Row 객체 연결하기

# 스키마에서 컬럼명을 확인하는 경우, 특정 인덱스의 열만 가져오는 작업이 필요합니다.

# In[20]:


# PRAGMA 키워드로 스키마 확인
cur.execute("PRAGMA table_info('student')")
schema = cur.fetchall()
schema


# In[21]:


# 컬럼명만 가져오기
col_names = list(map(lambda x: x[1], schema))
col_names


# Row 객체를 연결하면 더 쉽게 접근이 가능합니다.  
# SQL 실행 결과가 Row 객체로 오게 되는데, keys() 함수로 편리하게 컬럼명을 얻을 수 있습니다.

# In[22]:


# Row 객체 연결
con.row_factory = sqlite3.Row

# ※연결 후 Cursor 객체를 다시 생성해줘야 함
cur = con.cursor()
cur.execute("SELECT * FROM student")
row = cur.fetchone()

# 컬럼명 확인하기
print('col_name: ', row.keys())


# In[23]:


# SQL 실행 결과는 Row 객체가 리턴됨
print(row)


# In[24]:


# 컬럼명으로 특정 값에 접근 가능
cur.execute("""SELECT * FROM student""")
row = cur.fetchone()
print(row['last_name'])

# 행 데이터를 확인하기 위해 형변환
# dict나 list 타입도 가능하지만 값 변경 못하게 tuple로 변환해보기
print(tuple(row))


# ## sqlite_master
# DB 파일의 테이블에 관한 정보는 마스터 테이블인 sqlite_master에 저장됩니다.

# In[25]:


# sqlite_master 스키마 확인해보기
cur.execute("PRAGMA table_info('sqlite_master')")
from_db_cursor(cur)


# In[26]:


# 생성된 데이터베이스에 대한 정보가 저장되어있다
cur.execute("SELECT * FROM sqlite_master")
from_db_cursor(cur)

