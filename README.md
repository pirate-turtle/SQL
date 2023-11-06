# SQL with Python sqlite3
> 이 Repository에서는 sqlite3 모듈로 SQL 문법을 학습한 내용을 정리합니다.  
sqlite3는 Python에서 2.5버전부터 기본적으로 지원하는 라이브러리로, SQLite를 사용할 수 있도록 인터페이스를 제공합니다.  
jupyter notebook을 이용하여 SQL문과 실행 결과를 한눈에 볼 수 있도록 했습니다.  
_(jupyter 모듈이 설치되어있어야 합니다._  
`pip install jupyter`
_또는 아나콘다를 통해 설치)_

### SQL(Structed Query Language)
* 관계형 데이터베이스 시스템(RDBMS)에서 DB를 관리하기 위한 언어
* 크게 3가지로 나뉩니다
    * DDL (Data Define Language): 외부 스키마와 관련된 명령어  
    _(CREATE, ALTER, DROP, RENAME, TRUNCATE, COMMENT)_  

    * DML (Data Manipulation Language): 데이터를 조작하는 명령어  
    _(SELECT, INSERT, UPDATE, DELETE)_  

    * DCL (Data Control Language): 데이터의 보안 및 무결성과 관련된 명령어  
    _(GRANT, REVOKE)_



### SQLite
* 파일 기반 데이터베이스입니다.
* DB를 위한 서버가 따로 필요하지 않습니다. (Serverless)
* SQLite는 전용 시스템을 설치하거나 설정 파일을 생성할 필요가 없습니다. 파일 내에 데이터베이스 설정도 함께 저장됩니다.
* 가볍기 때문에 임베디드 환경에 알맞지만, 다른 RDBMS에 비해 지원하는 기능이 적고 한번에 한 사용자만 DB에 접근할 수 있으며, 최적화가 어렵다는 단점이 있습니다.



## Reference

SQLite Tutorial에서 제공하는 샘플 데이터  
https://www.sqlitetutorial.net/sqlite-sample-database/
![IMAGE](https://www.sqlitetutorial.net/wp-content/uploads/2015/11/sqlite-sample-database-color.jpg)




참고한 사이트
* https://docs.python.org/3/library/sqlite3.html
* https://www.sqlitetutorial.net/
* https://pypi.org/project/prettytable/

참고한 도서
* [모두의 SQL](https://thebook.io/006977/)
