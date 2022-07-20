# %% [markdown]
# # 데이터 조회
# 데이터 조회 시 유용한 문법에 대해 알아봅니다.
# * [SELECT](#select)
#     * [LIMIT](#limit)
#     * [연결 연산자 (||)](#연결-연산자)
#     * [AS](#as)
# * [DISTINCT](#distinct)
# * [ORDER BY](#order-by)
# * [WHERE](#where)
#     * [BETWEEN](#between)
#     * [IN](#in)
#     * [LIKE](#like)
# 
# 
# > <br/>사용한 데이터 정보  
# <br/>
# ![IMAGE](https://www.sqlitetutorial.net/wp-content/uploads/2015/11/sqlite-sample-database-color.jpg)  
# https://www.sqlitetutorial.net/sqlite-sample-database/  
# <br/>

# %% [markdown]
# ## 시작하기 전 실행하기!

# %%
import sqlite3
from prettytable import from_db_cursor

# SQLite 데이터베이스에 연결하기 위해 connect 생성
con = sqlite3.connect('./database/chinook.db')
con.row_factory = sqlite3.Row

# cursor 생성
cur = con.cursor()

# %% [markdown]
# ## SELECT
# 원하는 데이터를 조회할 때 사용합니다.
# 
# ※ SQL은 대소문자를 구분하지 않습니다. 명령문을 대문자, 그 외는 소문자로 입력하면 가독성이 좋아집니다.

# %%
# 한번에 모든 컬럼 조회
# SELECT * FROM table_name;
cur.execute("""
    SELECT *
    FROM customers
    """)

# 데이터 양이 많으니 상위 10개만 일단 보기
from_db_cursor(cur)[:10]

# %%
# 원하는 컬럼만 지정해서 조회 가능
# SELECT column1, column2 FROM table_name;
cur.execute("""
    SELECT customerid, firstname, city, state
    FROM customers
    """)

from_db_cursor(cur)[:10]

# %%
# 간단한 연산 결과를 얻을 수도 있다
cur.execute("SELECT 1+1")

from_db_cursor(cur)

# %%
# 여러개도 가능하다!
cur.execute("SELECT 1+1, 2*5")

from_db_cursor(cur)

# %%
# 컬럼끼리 연산하는것도 가능함
cur.execute("""
    SELECT customerid + supportrepid, firstname, city, state
    FROM customers
    """)

from_db_cursor(cur)[:10]

# %% [markdown]
# ### LIMIT
# 쿼리 결과를 원하는 행 수 만큼만 받도록 합니다.

# %%
cur.execute("""
    SELECT *
    FROM customers
    LIMIT 5
    """)

from_db_cursor(cur)

# %% [markdown]
# OFFSET 키워드로 행을 얼마만큼 건너뛸것인지 지정할 수 있습니다.

# %%
# offset을 n으로 지정하면 n행 건너뛰고 n+1행부터 리턴
cur.execute("""
    SELECT *
    FROM customers
    LIMIT 5 OFFSET 10
    """)

from_db_cursor(cur)

# %% [markdown]
# OFFSET 키워드를 사용하지 않고 지정할 수도 있습니다.

# %%
# 앞에 오는 숫자가 offset, 뒤에 오는 숫자가 limit
cur.execute("""
    SELECT *
    FROM customers
    LIMIT 10, 5
    """)

from_db_cursor(cur)

# %% [markdown]
# ### 연결 연산자 (||)
# 여러 컬럼의 값 또는 문자열을 합쳐 하나의 컬럼으로 출력합니다.  
# 문자열은 작은 따옴표(')로 감싸서 입력해야 합니다.

# %%
cur.execute("""
    SELECT firstname||' '||lastname
    FROM customers
    LIMIT 10
    """)

from_db_cursor(cur)

# %%
cur.execute("""
    SELECT customerid, 'My name is '||firstname||' '||lastname
    FROM customers
    LIMIT 10
    """)

from_db_cursor(cur)

# %% [markdown]
# ### AS
# 컬럼 및 테이블에 임시로 별명을 지어줄 수 있습니다.  

# %%
# SELECT column1 AS nickname FROM tablename
cur.execute("""
    SELECT customerid, firstname||' '||lastname AS Name
    FROM customers
    LIMIT 10
    """)

from_db_cursor(cur)

# %%
# 별명에 공백, 특수문자 등을 포함하고 싶은 경우 작은따옴표로 감싸서 문자열 형태로 만들어야 함
cur.execute("""
    SELECT customerid, firstname||' '||lastname AS 'My Name☆'
    FROM customers
    LIMIT 10
    """)

from_db_cursor(cur)

# %% [markdown]
# ## DISTINCT
# 중복된 데이터를 제외하고 유니크한 값만 보여줍니다

# %%
# 원하는 컬럼 앞에 DISTINCT 입력
# SELECT DISTINCT column1, column2 FROM table_name;
cur.execute("""
    SELECT DISTINCT country
    FROM customers
    LIMIT 10
    """)

from_db_cursor(cur)

# %% [markdown]
# ## ORDER BY
# 특정 컬럼을 기준으로 데이터를 정렬할 수 있습니다.

# %%
# SELECT * FROM table_name ORDER BY column1
# LIMIT은 ORDER BY 다음에 작성
cur.execute("""
    SELECT *
    FROM customers
    ORDER BY country
    LIMIT 10
    """)

from_db_cursor(cur)

# %%
# 2개 이상의 컬럼을 정렬 기준으로 넣을 수도 있음
cur.execute("""
    SELECT DISTINCT country, city
    FROM customers
    ORDER BY country, city
    LIMIT 15
    """)

from_db_cursor(cur)

# %% [markdown]
# 컬럼별로 정렬 순서를 지정할 수 있습니다.
# * ASC: 오름차순 (따로 입력하지 않으면 default로 오름차순)
# * DESC: 내림차순

# %%
# 컬럼 뒤에 정렬 순서 입력하기 (ASC는 생략 가능)
cur.execute("""
    SELECT DISTINCT country, city
    FROM customers
    ORDER BY country ASC, city DESC
    LIMIT 15
    """)

from_db_cursor(cur)

# %% [markdown]
# ## WHERE
# 조건에 맞는 데이터만 가져올 수 있습니다.  
# 연산자를 이용하여 조건문을 작성할 수 있습니다.

# %% [markdown]
# ### 비교 연산자
# |연산자|의미|
# |---|---|
# |=|일치하는 경우|
# |<><br/>!=|일치하지 않는 경우|
# |<|해당 값 미만인 경우|
# |<=|해당 값 이하인 경우|
# |>|해당 값 초과인 경우|
# |>=|해당 값 이상인 경우|

# %%
cur.execute("""
    SELECT *
    FROM customers
    WHERE customerid <= 5
    """)

from_db_cursor(cur)

# %%
cur.execute("""
    SELECT *
    FROM customers
    WHERE state='SP'
    """)

from_db_cursor(cur)

# %% [markdown]
# ### BETWEEN
# 지정한 범위 내의 값이면 참입니다.

# %%
# BETWEEN a AND b -> a~b 범위 안이면 참
cur.execute("""
    SELECT *
    FROM customers
    WHERE customerid BETWEEN 15 AND 20
    """)

from_db_cursor(cur)

# %% [markdown]
# ### IN
# 지정한 목록에 있는 값 중 하나와 일치하면 참입니다.

# %%
cur.execute("""
    SELECT *
    FROM customers
    WHERE customerid IN (1, 5, 10)
    """)

from_db_cursor(cur)

# %% [markdown]
# ### LIKE
# 패턴과 일치하는 경우 참입니다.  
# %와 _를 이용하여 패턴을 지정할 수 있습니다.  
# %와 _는 모든 문자와 매칭되며, %는 문자열, _는 문자 하나를 의미합니다.

# %%
# 전화번호가 +55로 시작하는 경우
cur.execute("""
    SELECT *
    FROM customers
    WHERE phone LIKE '+55%'
    """)

from_db_cursor(cur)

# %%
# 전화번호에 55를 포함하는 경우
cur.execute("""
    SELECT *
    FROM customers
    WHERE phone LIKE '%55%'
    """)

from_db_cursor(cur)

# %%
# state가 B로 끝나는 2글자인 경우
cur.execute("""
    SELECT *
    FROM customers
    WHERE state LIKE '_B'
    """)

from_db_cursor(cur)

# %%
# 성이 on으로 끝나는 문자열
cur.execute("""
    SELECT *
    FROM customers
    WHERE lastname LIKE '%on'
    """)

from_db_cursor(cur)

# %%
# email 도메인이 2글자인 경우 (. 뒤에 2글자인 경우)
cur.execute("""
    SELECT *
    FROM customers
    WHERE email LIKE '%.__'
    LIMIT 10
    """)

from_db_cursor(cur)


