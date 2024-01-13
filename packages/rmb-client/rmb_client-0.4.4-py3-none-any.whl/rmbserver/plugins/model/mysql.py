from rmbcommon.models import StrucQuery, QueryResult
import sqlparse

class MySQLQuery(StrucQuery):

    @property
    def sql(self):
        return self.content

    def __str__(self):
        return sqlparse.format(self.content, reindent=True, keyword_case='upper')


# class MySQLQueryResult(QueryResult):
#     __source_type__ = "MySQL"
#
#     @property
#     def rows(self):
#         return self.content.fetchall()
#
#     @property
#     def columns(self):
#         return self.content.keys()
#
#     def __str__(self):
#         output = ""
#         output += f"Columns: {','.join([column for column in self.columns])}\n"
#         output += f"Rows: {self.rows}\n"
#         return output[0:2000]  # 截取前2000个字符

class MySQLQueryResult(QueryResult):
    pass
