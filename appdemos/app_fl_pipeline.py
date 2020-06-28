import logging
import json
import requests

base_url = 'http://172.27.128.236:40121/'
base_headers = {'Content-Type': 'application/json;charset=utf-8'}
default_timeout = 3  # seconds
user_token = ''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def login():
    url = base_url + 'keystone/v1/sessions'
    data_dict = {'username': '4pdadmin', 'password': 'admin'}

    sess = requests.session()
    sess.headers.update(base_headers)
    resp = sess.post(url, data=json.dumps(data_dict), timeout=default_timeout)
    log_request_info(resp.request)
    assert(resp.status_code == 200)

    cookies_dict = requests.utils.dict_from_cookiejar(resp.cookies)
    logger.info('login with user token: %s' % cookies_dict['User-Token'])
    return sess


def log_request_info(req):
    logger.debug('request url: %s' % req.url)
    logger.debug('request headers: %s' % req.headers)
    logger.debug('request method: %s' % req.method)
    logger.debug('request body: %s' % req.body)

# -----------------------------------------------
# Get info and operator for running flowengine
# -----------------------------------------------


def list_flowengine(sess, workspace_id, size=10):
    '''
    list all running flowengines.
    '''
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
    '''
    list all pipelines of running flowengine.
    '''
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/list'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    pipelines = resp.json()['data']['engineJobPipelineTemplateList']
    return [{'template_id': p['engineTemplateId'], 'id': p['id'], 'status': p['data']['status']} for p in pipelines]


def run_pipeline(sess, instance_id, template_id, pipeline_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/{pipeline_id}/start'

    resp = sess.post(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    status = resp.json()['data']['status']
    return True if status == 'running' else False


def list_pipeline_task(sess, instance_id, pipeline_id):
    '''
    list all history task of a pipeline.
    '''
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{pipeline_id}/historyList'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    tasks = resp.json()['data']
    return sorted([{'id': t['id'], 'status':t['status']} for t in tasks], key=lambda x: x['id'])


def stop_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/stopHistory?engineId={pipeline_id}'

    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False


def resume_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/resumeHistory?engineId={pipeline_id}'

    resp = sess.post(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False

# -----------------------------------------------
# Get info and operator for flowengine template
# -----------------------------------------------


def list_pipeline_template(sess, template_id, size=10):
    '''
    list all pipelines of template.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/list/byPage?size={size}'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    assert(resp.json()['status'] == 0)

    return [{'id': template['id'], 'describe': template['data']['describe']}
            for template in resp.json()['data']['engineJobPipelineTemplateList']]


def list_job_template(sess, template_id, size=10):
    '''
    list all jobs of template.
    '''
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/list/byPage?page=1&size={size}'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    assert(resp.json()['status'] == 0)

    return [{'id': job['id'], 'name': job['name']}
            for job in resp.json()['data']['engineJobTemplateList']]


def list_pipeline_job(sess, template_id, pipeline_id, size=10):
    '''
    list all jobs of a pipeline.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/list/byPage?size={size}'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    assert(resp.json()['status'] == 0)

    pipelines = [p for p in resp.json()['data']['engineJobPipelineTemplateList']
                 if str(p['id']) == pipeline_id]
    if len(pipelines) == 0:
        return []

    pipeline = pipelines[0]
    return [{'name': node['name']} for node in pipeline['data']['nodes']]


def create_pipeline_job(sess, template_id, pipeline_template_name):
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/create'
    data = build_pipeline_job_data(template_id, pipeline_template_name)

    resp = sess.post(url, data=json.dumps(data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False


def build_pipeline_job_data(template_id, template_name):
    data = {'name': template_name, 'engineTemplateId': template_id,
            'indexType': 'DAG', 'type': 'TASK', 'system': False}

    outputCfg = data['outputConfig'] = {}
    outputCfg['outputType'] = 'Table'

    execCfg = data['executionConfig'] = {}
    execCfg['runMode'] = 'SINGLE'
    execCfg['interval'] = 0
    execCfg['intervalUnit'] = 'MINUTE'
    execCfg['trigger'] = 'ModelTrainFinishEvent'

    return data


def delete_pipeline_job(sess):
    pass


def copy_pipeline(sess, template_data):
    pass


if __name__ == '__main__':

    workspace_id = '1'
    instance_id = '38'
    running_template_id = '1'
    running_pipeline_id = '1'
    pipeline_task_id = '19'

    template_id = '10032'
    pipeline_id = '65'

    sess = login()
    try:
        # logger.info(list_flowengine(sess, workspace_id))

        # logger.info(list_pipeline(sess, instance_id, template_id))
        # run_pipeline(sess, instance_id, template_id, pipeline_id)

        # logger.info(list_pipeline_task(sess, instance_id, pipeline_id))
        # resume_pipeline_task(sess, instance_id, pipeline_id, pipeline_task_id)
        # stop_pipeline_task(sess, instance_id, pipeline_id, pipeline_task_id)

        # logger.info(list_pipeline_template(sess, template_id))
        # logger.info(list_job_template(sess, template_id))
        logger.info(list_pipeline_job(sess, template_id, pipeline_id))

        # ret = create_pipeline_job(sess, template_id, 'offline-job04')
        # assert(ret)
    finally:
        sess.close()

    logger.info('flowengine pipeline demo done.')
