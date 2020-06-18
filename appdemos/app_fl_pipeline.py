import json
import requests

base_url = 'http://172.27.128.236:40121/'
base_headers = {'Content-Type': 'application/json;charset=utf-8'}
default_timeout = 3  # seconds
user_token = ''


def login():
    url = base_url + 'keystone/v1/sessions'
    data_dict = {'username': '4pdadmin', 'password': 'admin'}

    sess = requests.session()
    resp = sess.post(url, headers=base_headers,
                     data=json.dumps(data_dict), timeout=default_timeout)
    assert(resp.status_code == 200)
    user_token = resp.cookies.get('User-Token')
    print('login with user token:', user_token)
    return sess


def list_flowengine(sess, workspace_id, size=10):
    url = base_url + 'automl-manager/v1/appList'
    data_dict = {'workspaceId': workspace_id,
                 'status': 'RUNNING', 'size': size}

    resp = sess.get(url, params=data_dict, timeout=default_timeout)
    assert(resp.status_code == 200)
    fl_list = resp.json()['data']['appList']
    return [{'instanceId': fl['instanceId'], 'status': fl['status'], 'appName': fl['appName']} for fl in fl_list]


def create_pipeline(fl_id):
    '''
    url: http://172.27.128.236:40121/template-market/v1/pipeline/template/10032/create
    request json:
    {
    "id": null,
    "logicId": null,
    "engineTemplateId": "10032",
    "pipelineKey": "offline-test02-0617",
    "data": {
        "nodes": [
        {
            "id": null,
            "nodeId": "start_node",
            "name": "start",
            "status": "INITIALIZED",
            "type": "START",
            "title": "开始",
            "outputSlots": [
            {
                "elementType": "TABLE",
                "id": "79b4b2b8-9999-40d3-b504-5cf368cd3692"
            }
            ]
        }
        ],
        "edges": [],
        "id": "79971841-b07c-11ea-9f6f-dbcd1d5efc9a",
        "status": "init",
        "layout": "",
        "name": "offline-test02",
        "describe": "zhengjin offline pipeline test.",
        "executionConfig": {
        "runMode": "SINGLE",
        "cronExpression": null,
        "interval": 0,
        "intervalUnit": "MINUTE",
        "isManual": null,
        "trigger": "ModelTrainFinishEvent"
        },
        "openMsgTopicConfig": {},
        "pipelineParams": null
    }
    }
    '''
    pass


def list_pipeline(sess, instance_id, template_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/list'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    pipelines = resp.json()['data']['engineJobPipelineTemplateList']
    return [{'template_id': p['engineTemplateId'], 'id': p['id'], 'status': p['data']['status']} for p in pipelines]


def run_pipeline(sess, instance_id, template_id, pipeline_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/{pipeline_id}/start'

    resp = sess.post(url, headers=base_headers,
                     data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    status = resp.json()['data']['status']
    return True if status == 'running' else False


def list_pipeline_task(sess, instance_id, pipeline_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{pipeline_id}/historyList'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    tasks = resp.json()['data']
    return sorted([{'id': t['id'], 'status':t['status']} for t in tasks], key=lambda x: x['id'])


def stop_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/stopHistory?engineId={pipeline_id}'

    resp = sess.delete(url, headers=base_headers,
                       data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] else False


def resume_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/resumeHistory?engineId={pipeline_id}'

    resp = sess.post(url, headers=base_headers,
                     data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] else False


if __name__ == '__main__':

    workspace_id = '1'
    instance_id = '27'
    template_id = '1'
    pipeline_id = '1'
    pipeline_task_id = '19'

    sess = login()
    try:
        # print(list_flowengine(sess, workspace_id))

        # print(list_pipeline(sess, instance_id, template_id))
        # run_pipeline(sess, instance_id, template_id, pipeline_id)

        print(list_pipeline_task(sess, instance_id, pipeline_id))
        # resume_pipeline_task(sess, instance_id, pipeline_id, pipeline_task_id)
        # stop_pipeline_task(sess, instance_id, pipeline_id, pipeline_task_id)
    finally:
        sess.close()

    print('flowengine pipeline demo done.')
