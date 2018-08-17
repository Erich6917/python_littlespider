# -*- coding: utf-8 -*-
# @Time    : 2017/9/18
# @Author  : LIYUAN134
# @Site    :
# @File    : PostgreSQLManage.py
# @Comment: PostgreSQL数据操作管理
#           1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
#           2、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
#           3、在输入的值中不需要使用转意函数，系统会自动处理

import sys

import MySQLdb
import psycopg2


# from DBUtils.PooledDB import PooledDB


class Mysql(object):
    """  
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()  
            释放连接对象;conn.close()或del conn  
    """

    # 连接池对象
    __pool = None

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        # if Mysql.__pool is None:
        #     # mysql 连接
        #     __pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20,
        #                       host="112.25.233.123",  # Config.DBHOST ,
        #                       port=6980,  # Config.DBPORT ,
        #                       user="root",  # Config.DBUSER ,
        #                       passwd="aaaaa888",  # Config.DBPWD ,
        #                       db="pavoice",  # Config.DBNAME,
        #                       charset="utf8",  # Config.DBCHAR,
        #                       )
        #     return __pool.connection()
        # conn = psycopg2.connect(
        #     database='jadebloom',
        #     user='bloomopr',
        #     password='pg123',
        #     host='localhost',
        #     port='5432'
        # )
        conn = psycopg2.connect(
            database='d0bloom',
            user='bloomopr',
            password='paic1234',
            host='localhost',
            port='5432'
        )

        return conn
        # return __pool.connection()
        #                             use_unicode=False,
        #                             cursorclass=DictCursor

    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        try:
            self._conn = Mysql.__getConn()
            self._cursor = self._conn.cursor()
        except Exception, e:
            error = 'Connect failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error
            sys.exit()

    # 针对读操作返回结果集
    def _exeCute(self, sql=''):
        try:
            self._cursor.execute(sql)
            records = self._cursor.fetchall()
            return records
        except MySQLdb.Error, e:
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error

            # 针对更新,删除,事务等操作失败时回滚

    def _exeCuteCommit(self, sql='', arg=None):
        try:
            if arg is None:
                self._cursor.execute(sql)
            else:
                self._cursor.execute(sql, arg)
            self._conn.commit()
        except MySQLdb.Error, e:
            self._conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error
            # sys.exit()

    def _createTable(self, table, attr_dict, constraint):
        sql = ''
        # sql_mid = '`row_id` bigint(11) NOT NULL AUTO_INCREMENT,'  
        sql_mid = ''
        for attr, value in attr_dict.items():
            sql_mid = sql_mid + '`' + attr + '`' + ' ' + value + ','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s (' % table
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print '_createTable:' + sql
        self._exeCuteCommit(sql)

    def insertOne(self, sql, value=None):
        """  
        @summary: 向数据表插入一条记录  
        @param sql:要插入的ＳＱＬ格式  
        @param value:要插入的记录数据tuple/list  
        @return: insertId 受影响的行数  
        """
        self._exeCuteCommit(sql, value)

    #         return self.__getInsertId()


    def _insert(self, table, attrs, value):
        """
        @summary: 向数据表插入一条记录 
        @param attrs = [] :要插入的属性
        @param value = [] :要插入的数据值 
        """
        # values_sql = ['%s' for v in attrs]
        attrs_sql = '(' + ','.join(attrs) + ')'
        value_str = self._transferContent(value)
        values_sql = ' values(' + value_str + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print '_insert:' + sql
        self._exeCuteCommit(sql)

    def _insertDic(self, table, attrs):
        """
        @summary: 向数据表插入一条记录 
        @param attrs = {"colNmae:value"} :要插入的属性：数据值
        """
        attrs_sql = '(' + ','.join(attrs.keys()) + ')'
        value_str = self._transferContent(attrs.values())  # ','.join(attrs.values())
        values_sql = ' values(' + value_str + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print '_insert:' + sql
        self._exeCuteCommit(sql)

        # 将list转为字符串

    def _transferContent(self, content):
        if content is None:
            return None
        else:
            Strtmp = ""
            for col in content:
                if Strtmp == "":
                    Strtmp = "\"" + col + "\""
                else:
                    Strtmp += "," + "\"" + col + "\""
            return Strtmp

    def _insertMany(self, table, attrs, values):
        """
        @summary: 向数据表插入多条数据  
        @param attrs = [id,name,...]  :要插入的属性
        @param values = [[1,'jack'],[2,'rose']] :要插入的数据值
        """
        values_sql = ['%s' for v in attrs]
        attrs_sql = '(' + ','.join(attrs) + ')'
        values_sql = ' values(' + ','.join(values_sql) + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        print '_insertMany:' + sql
        try:
            for i in range(0, len(values), 20000):
                self._cursor.executemany(sql, values[i:i + 20000])
                self._conn.commit()
        except MySQLdb.Error, e:
            self._conn.rollback()
            error = '_insertMany executemany failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error
            range(error)
            # sys.exit()

    def insertMany(self, sql, values=None):
        """  
        @summary: 向数据表插入多条记录  
        @param sql:要插入的ＳＱＬ格式  
        @param values:要插入的记录数据tuple(tuple)/list[list]  
        @return: count 受影响的行数  
        """
        try:
            if values is None:
                count = self._cursor.executemany(sql)
            else:
                count = self._cursor.executemany(sql, values)
            self._conn.commit()
        except MySQLdb.Error, e:
            self._conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error
            # sys.exit()
        return count

    def _select(self, table, cond_dict='', order=''):
        """
        @summary: 执行条件查询，并取出所有结果集
        @cond_dict:{'name':'xiaoming'...}  
        @order:'order by id desc'
        @return:  result ({"col":"val","":""},{})
        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                consql = consql + k + '=' + v + ' and'
        consql = consql + ' 1=1 '
        sql = 'select * from %s where ' % table
        sql = sql + consql + order
        print '_select:' + sql
        return self._exeCute(sql)

    def __getInsertId(self):
        """  
        获取当前连接最后一次插入操作生成的id,如果没有则为０  
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def getAll(self, sql, param=None):
        """  
        @summary: 执行查询，并取出所有结果集  
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来  
        @param param: 可选参数，条件列表值（元组/列表）  
        @return: result list(字典对象)/boolean 查询到的结果集 
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        """  
        @summary: 执行查询，并取出第一条  
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来  
        @param param: 可选参数，条件列表值（元组/列表）  
        @return: result list/boolean 查询到的结果集  
        """
        # pg 写法
        self._cursor.execute(sql, param)
        result = self._cursor.fetchone()

        # # mysql写法
        # if param is None:
        #     count = self._cursor.execute(sql)
        # else:
        #     count = self._cursor.execute(sql, param)
        # if count > 0:
        #     result = self._cursor.fetchone()
        # else:
        #     result = False
        return result

    def getMany(self, sql, num, param=None):
        """  
        @summary: 执行查询，并取出num条结果  
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来  
        @param num:取得的结果条数  
        @param param: 可选参数，条件列表值（元组/列表）  
        @return: result list/boolean 查询到的结果集  
        """

        count = self.__query(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def update(self, sql, param=None):
        """  
        @summary: 更新数据表记录  
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)  
        @param param: 要更新的  值 tuple/list  
        @return: count 受影响的行数  
        """
        return self._exeCuteCommit(sql, param)

    def delete(self, sql, param=None):
        """  
        @summary: 删除数据表记录  
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)  
        @param param: 要删除的条件 值 tuple/list  
        @return: count 受影响的行数  
        """
        return self._exeCuteCommit(sql, param)

    def begin(self):
        """  
        @summary: 开启事务  
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """  
        @summary: 结束事务  
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """  
        @summary: 释放连接池资源  
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
