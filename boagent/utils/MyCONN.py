#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-3-20


@module: MyCONN
@used: mysql connect action
"""


import MySQLdb
import time

from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyCONN.py')
logger = mylog.outputLog()


__all__ = ['MySQL']
__author__ = 'zhihao'


class MySQL(object):
    """
    used : Encapsulate MySQLdb commonly used functions
    :param error_code : mysql error code
    :param _instance : self class intance
    :param _conn : db conn
    :param _cur : cursor
    :param _TIMEOUT : default timeout 30s
    :param _timecount : total timeout
    """

    error_code = '' #mysql error code

    _instance = None #self class intance
    _conn = None #db conn
    _cur = None  #cursor

    _TIMEOUT = 30 #default timeout 30s
    _timecount = 0 #total timeout

    def __init__(self, dbconfig):
        """
        used : init config and get value
        :param dbconfig : dictionary of connect config
        """
        try:
            self.dbconfig = dbconfig

            self._conn = MySQLdb.connect(host=self.dbconfig['host'],
                                         port=self.dbconfig['port'],
                                         user=self.dbconfig['user'],
                                         passwd=self.dbconfig['passwd'],
                                         db=self.dbconfig['db'],
                                         charset=self.dbconfig['charset'])
            conn_info ="[action]:connect" \
                       "[status]:OK" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}" \
                       "[user]:{user}".format(host=self.dbconfig['host'],
                                            db=self.dbconfig['db'],
                                            port=self.dbconfig['port'],
                                            user=self.dbconfig['user'])
            logger.info(conn_info)

        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = "[action]:connect" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}" \
                        "[user]:{user}".format(host=self.dbconfig['host'], db=self.dbconfig['db'],
                                               port=self.dbconfig['port'], user=self.dbconfig['user'],
                                               args0=e.args[0], args1=e.args[1])

            print error_msg

            logger.error(error_msg)

            # if not over _TIMEOUT , try again
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(dbconfig)
            else:
                logger.error("CONNTECTING TIMEOUT!")
                raise Exception("CONNTECTING TIMEOUT!")

        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self, sql):
        """
        used : execute SELECT
        :param sql : SELECT sql
        """

        try:

            self._cur.execute("set names utf8;")
            result = self._cur.execute(sql)

            sql_info = "[action]:query" \
                       "[status]:OK" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}" \
                       "[sql]:{sql}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                            sql=sql)
            logger.info(sql_info)

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:query" \
                        "[status]:FAIL[port]:{port}" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                               args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)
            result = False

        return result

    def update(self, sql):
        """
        used : execute UPDATE and DELETE
        :param sql : UPDATE sql
        """

        try:

            self._cur.execute("set names utf8;")
            result = self._cur.execute(sql)
            self._conn.commit()

            sql_info = "[action]:update" \
                       "[status]:OK" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}" \
                       "[sql]:{sql}".format(host=self.dbconfig['host'], port=self.dbconfig['port'],db=self.dbconfig['db'],
                                 sql=sql)
            logger.info(sql_info)

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:update" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                           args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)
            result = False

        return result

    def insert(self, sql):
        """
        used : execute INSERT , return increament id
        :param sql : INSERT sql
        """

        try:

            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            result = self._conn.insert_id()
            self._conn.commit()
            
            sql_info = "[action]:update" \
                       "[status]:OK" \
                       "[sql]:{sql}" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                          sql=sql)
            logger.info(sql_info)

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:update" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                           args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)
            result = False

        return result

    def fetchAllRows(self):
        """
        used : return List of results
        """

        try:
            sql_info = "[action]:fetchAllRows" \
                       "[status]:OK" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}" \
                       "[conn]:{conn}" \
                       "[cur]:{cur}".format(host=self.dbconfig['host'], port=self.dbconfig['port'], db=self.dbconfig['db'],
                                            conn=self._conn, cur=self._cur)
            logger.info(sql_info)

            return self._cur.fetchall()

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:fetchAllRows" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}" \
                        "[conn]:{conn}" \
                        "[cur]:{cur}".format(host=self.dbconfig['host'], port=self.dbconfig['port'], db=self.dbconfig['db'],
                                             conn=self._conn, cur=self._cur,
                                             args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)

            return False

    def fetchOneRow(self):
        """
        used : return one line of results
        """

        try:
            sql_info = "[action]:fetchOneRow" \
                       "[status]:OK" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}" \
                       "[conn]:{conn}" \
                       "[cur]:{cur}".format(host=self.dbconfig['host'], port=self.dbconfig['port'], db=self.dbconfig['db'],
                                            conn=self._conn, cur=self._cur)
            logger.info(sql_info)

            return self._cur.fetchone()
        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:fetchOneRow" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}" \
                        "[conn]:{conn}" \
                        "[cur]:{cur}".format(host=self.dbconfig['host'], port=self.dbconfig['port'], db=self.dbconfig['db'],
                                             conn=self._conn, cur=self._cur,
                                             args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)

            return False

    def getRowCount(self):
        """
        used : get count num of line
        """

        try:
            sql_info = "[action]:getRowCount" \
                       "[status]:OK" \
                       "[host]:{host}" \
                       "[port]:{port}" \
                       "[db]={db}" \
                       "[conn]:{conn}" \
                       "[cur]:{cur}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                            conn=self._conn,cur=self._cur)
            logger.info(sql_info)

            return self._cur.rowcount
        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:getRowCount" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[host]:{host}" \
                        "[port]:{port}" \
                        "[db]={db}" \
                        "[conn]:{conn}" \
                        "[cur]:{cur}".format(host=self.dbconfig['host'],port=self.dbconfig['port'],db=self.dbconfig['db'],
                                             conn=self._conn,cur=self._cur,
                                             args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)

            return False

    def commit(self):
        """
        used : execute commit
        """

        try:
            sql_info = "[action]:commit" \
                       "[status]:OK" \
                       "[conn]:{conn}".format(conn=self._conn)
            logger.info(sql_info)

            self._conn.commit()

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:commit" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[conn]:{conn}".format(conn=self._conn,
                                               args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)

    def rollback(self):
        """
        used : execute rollback
        """
        try:
            sql_info = "[action]:rollback" \
                       "[status]:OK" \
                       "[conn]:{conn}".format(conn=self._conn)
            logger.info(sql_info)

            self._conn.rollback()

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:rollback" \
                        "[status]:FAIL[MySQL" \
                        "Errorcode]:{args0},{args1}" \
                        "[conn]:{conn}".format(conn=self._conn,
                                               args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)

    def __del__(self):
        """
        used : release resource
        """

        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def close(self):
        """
        used : colse db conn
        """

        try:
            sql_info = "[action]:close" \
                       "[status]:OK" \
                       "[conn]:{conn}".format(conn=self._conn)
            logger.info(sql_info)

            self.__del__()

        except MySQLdb.Error, e:

            self.error_code = e.args[0]
            error_msg = "[action]:close" \
                        "[status]:FAIL" \
                        "[MySQL Errorcode]:{args0},{args1}" \
                        "[conn]:{conn}".format(conn=self._conn,
                                               args0=e.args[0], args1=e.args[1])
            print error_msg
            logger.error(error_msg)


if __name__ == '__main__':
    '''
    dbconfig = {'host': '192.168.41.40',
                'port': 3306,
                'user': 'zhihao',
                'passwd': 'tfkjzhihao',
                'db': 'zhihao_test',
                'charset': 'utf8'}

    db = MySQL(dbconfig)

    sql = "SELECT * FROM tbl_i_dept;"
    db.query(sql)
    result = db.fetchAllRows()
    print result
    #num = db.getRowCount()
    #print result
    #print num
    db.close()

    #sql="update tbl_i_dept1 set is_ok=1 where id = 11111111;"
    #sql = "delete from tbl_i_dept where id = 11111111;"
    #db.update(sql)
    #db.commit()
    #db.close()

    #sql = "INSERT INTO zhihao_test.tbl_i_dept (id, is_ok, org_id, full_name, short_name, prop, type, level, is_direct, type_name, contact, number, affiliation, address, start_time, end_time, gap, ordernum, base_group, background, header_name, if_lower, region_id, city_id, county_id, longitude, latitude, pid, dept_id, dept_level, system_id, secretary_id, is_auth, deleteflag, createby, createdt, updateby, updatedt, allpid, uuid, uupid) VALUES ('11111111', '0', '0', '世纪新苑社区第七党支部', '世纪新苑社区第七党支部', '0', '4', '0', '0', '', '', '0', '本市', '', '0', '0', '4', '7', '0', '0', '', '0', '0', '0', '0', '0.000000000', '0.000000000', '7604', '0', '5', '0', '0', '0', '0', '', '0', '', '0', '8276,7368,7530,7604,7078', '000000000000', '0000000000000000000');"
    #db.insert(sql)
    #db.commit()
    #db.close()

    '''

    import MyCONN
    help(MyCONN)


