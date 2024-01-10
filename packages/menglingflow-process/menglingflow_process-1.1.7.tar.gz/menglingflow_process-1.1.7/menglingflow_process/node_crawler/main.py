import click
from .execute import run
import os


def _write(task_name, file, pyfile):
    path = os.path.dirname(os.path.abspath(__file__)) + '/ceils'
    with open(f'./{task_name}/{file}.py', mode='w+', encoding='utf8') as f, \
            open(f'{path}/{pyfile}.py', mode='r', encoding='utf8') as pf:
        f.write(pf.read())


def _download(task_name, nodenum):
    if not os.path.exists(task_name):
        os.mkdir(task_name)
    _write(task_name, '_0_start', 'start')
    [_write(task_name, f'_{i + 1}_node', 'node') for i in range(nodenum)]
    _write(task_name, f'_{nodenum + 1}_end', 'end')


##任务校验启动功能未完成
@click.command()
@click.argument('act')
@click.argument('task-name')
@click.option('--nodenum', default=1)
@click.option('-end', 'is_end', is_flag=True, help='是否执行所有数据的执行方法')
@click.option('-all', 'is_all', is_flag=True, help='是否将全部节点参数作为最后执行方法的入参')
@click.option('-del', 'is_del', is_flag=True, help='是否在完成最后方法后执行redis的数据删除')
def transfer(act, task_name, nodenum, is_end=True, is_all=False, is_del=False):
    if act in ('download', 'dl'):
        # 配置节点代码
        _download(task_name, int(nodenum))
        print(f'已配置参考节点任务-{task_name}')
    elif act in ('start', 'st'):
        # 任务启动
        run(task_name, is_end=is_end, is_all=is_all, is_del=is_del)
    else:
        print('命令错误,仅 download start')
