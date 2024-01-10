from menglingtool_sqltools.pgsql import Pgsql

_connect = {
    'dbname': ''
}


def _savePgsql(dts):
    with Pgsql(**_connect) as pgt:
        pass


# 结果处理
def resultDispose(result: list or dict):
    pass
