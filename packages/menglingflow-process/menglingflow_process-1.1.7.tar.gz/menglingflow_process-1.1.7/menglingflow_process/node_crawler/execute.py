import base64
import json
from importlib import import_module
from menglingtool_redis.redis_tool import RedisExecutor
from menglingtool.goodlib import ThreadDictGoods
from menglingtool.thread import thread_auto_run
import os, sys, re

RCONF = None


def _toBaseJson(data):
    decoded_data = base64.b64decode(data).decode('utf-8')
    return json.loads(decoded_data)


def _toJsonBase(data):
    js = json.dumps(data, ensure_ascii=False)
    return base64.b64encode(js.encode('utf-8')).decode('utf-8')


def _task_run(arg):
    key, name, next_name, func_ceil, func_analysis, layer = arg
    with RedisExecutor(**RCONF) as r:
        if r.hget(name, key): return
        # 首层不进行base编码
        if layer == 0:
            inn = key
        else:
            inn = _toBaseJson(key)
        result = []
        for out in func_ceil(inn):
            result.extend(func_analysis(out))
        r.hset(name, key, json.dumps(result, ensure_ascii=False))
        # 尾层存为set格式
        if layer == -1:
            r.sadd(next_name, *[json.dumps(out, ensure_ascii=False) for out in result])
        else:
            for out in result:
                next_key = _toJsonBase(out)
                if not r.hexists(next_name, next_key):
                    r.hset(next_name, next_key, '')


def _run(datas, run_nodes):
    first_name = run_nodes[0][1]
    with RedisExecutor(**RCONF) as r:
        for key in datas:
            if not r.hexists(first_name, key):
                r.hset(first_name, key, '')

        for layer, args in enumerate(run_nodes):
            thread_num, name, next_name = args[0], args[1], args[2]
            print(f'\n{name}节点任务开始', f'线程数:{thread_num}')
            print('节点输入数量:', r.hlen(name))
            thread_auto_run(_task_run,
                            [(key, *args[1:], layer if layer + 1 < len(run_nodes) else -1) for key in r.hkeys(name)],
                            threadnum=thread_num)
        print(f'\n节点任务结束')
        print('结尾输出数量:', r.scard(next_name))


def _get_allMap(rnodes):
    with RedisExecutor(**RCONF) as r:
        def saveKey(index, key):
            rnode = rnodes[index]
            base_key = _toJsonBase(key) if index > 0 else key
            vs = json.loads(r.hget(rnode, base_key))
            if index == len(rnodes) - 1:
                return vs
            else:
                nodedt = {}
                for v in vs:
                    js_v = json.dumps(v, ensure_ascii=False)
                    nodedt[js_v] = saveKey(index + 1, v)
                return nodedt

        mapdt = {}
        for k0 in r.hkeys(rnodes[0]):
            mapdt[k0] = saveKey(0, k0)
        return mapdt


def run(task_name, is_end, is_all, is_del):
    work_path = f'{os.getcwd()}/{task_name}'
    sys.path.append(work_path)
    # 获取节点
    nodes = []
    for f in os.listdir(work_path):
        nodef = re.findall('^_(\d+)_(\w+)\.py$', f)
        if nodef:
            rank, node_name = nodef[0]
            nodes.append((int(rank), f'{task_name}_{rank}_{node_name}', f[:-3]))
    nodes.sort(key=lambda x: x[0])
    assert len(nodes) >= 3, f'节点数量出错，{nodes}'

    # 初始层参数
    global RCONF
    start_model = import_module(nodes[0][-1])
    RCONF = getattr(start_model, 'RCONF')
    datas = getattr(start_model, 'original')()

    # 执行层参数
    run_nodes = []
    for _, rname, pyname in nodes[1:-1]:
        node_name = rname
        node_model = import_module(pyname)
        ceil = getattr(node_model, 'ceil')
        analysis = getattr(node_model, 'analysis')
        thread_num = getattr(node_model, 'thread_num')
        # 为上个节点填充名称
        if run_nodes: run_nodes[-1][2] = node_name
        # 记录当前节点配置
        run_nodes.append([thread_num, node_name, None, ceil, analysis])

    # 结束层配置，配置最后一层名称
    end_name = nodes[-1][1]
    run_nodes[-1][2] = end_name

    print(f'任务-{task_name} 载入完成！')
    print('执行节点数量:', len(run_nodes))
    print('起始输入数量:', len(datas))
    _run(datas, run_nodes)
    # 执行数据的最后方法
    if is_end:
        print('执行数据的最后方法...')
        _, rname, pyname = nodes[-1]
        last_model = import_module(pyname)
        last_fn = getattr(last_model, 'resultDispose')
        if is_all:
            print('数据格式为全节点字典')
            last_fn(_get_allMap([node[1] for node in nodes[1:-1]]))
        else:
            print('数据格式为全结果列表')
            with RedisExecutor(**RCONF) as r:
                last_fn([json.loads(v) for v in r.smembers(rname)])
    if is_del:
        print('删除缓存数据')
        with RedisExecutor(**RCONF) as r:
            r.delete(*[node[1] for node in nodes[1:]])


if __name__ == '__main__':
    RCONF = {
        'dbindex': 0,
        'host': '192.168.3.67',
        'pwd': 'Ljh1357999',
        'port': 5007,
    }
    a = _get_allMap(['24fa8_nodes_1_node', '24fa8_nodes_2_node'])
    print()
