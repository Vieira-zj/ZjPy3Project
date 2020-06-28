import logging
import json
import requests
import uuid

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
    print_request_info(resp.request)
    assert(resp.status_code == 200)

    cookies_dict = requests.utils.dict_from_cookiejar(resp.cookies)
    logger.info('login with user token: %s' % cookies_dict['User-Token'])
    return sess


def print_request_info(req):
    logger.debug('request url: %s' % req.url)
    logger.debug('request headers: %s' % req.headers)
    logger.debug('request method: %s' % req.method)
    logger.debug('request body: %s' % req.body)

# -----------------------------------------------
# Get info and operator for running flowengine
# -----------------------------------------------


def list_running_flowengines(sess, workspace_id, size=10):
    '''
    list all running flowengine instances.
    '''
    url = base_url + 'automl-manager/v1/appList'
    data_dict = {'workspaceId': workspace_id,
                 'status': 'RUNNING', 'size': size}

    resp = sess.get(url, params=data_dict, timeout=default_timeout)
    assert(resp.status_code == 200)
    fl_list = resp.json()['data']['appList']
    return [{'instanceId': fl['instanceId'], 'status': fl['status'], 'appName': fl['appName']} for fl in fl_list]


def list_fl_pipelines(sess, instance_id, template_id):
    '''
    list all pipelines of a running flowengine.
    '''
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/list'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    pipelines = resp.json()['data']['engineJobPipelineTemplateList']
    return [{'template_id': p['engineTemplateId'], 'id': p['id'], 'status': p['data']['status']} for p in pipelines]


def run_fl_pipeline(sess, instance_id, template_id, pipeline_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/{pipeline_id}/start'

    resp = sess.post(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    status = resp.json()['data']['status']
    return True if status == 'running' else False


def list_fl_pipeline_tasks(sess, instance_id, pipeline_id):
    '''
    list all history tasks of a flowengine pipeline.
    '''
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{pipeline_id}/historyList'

    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    tasks = resp.json()['data']
    return sorted([{'id': t['id'], 'status':t['status']} for t in tasks], key=lambda x: x['id'])


def stop_fl_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/stopHistory?engineId={pipeline_id}'

    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False


def resume_fl_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/resumeHistory?engineId={pipeline_id}'

    resp = sess.post(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False

# -----------------------------------------------
# Get info and operator for flowengine template
# -----------------------------------------------


def list_template_pipelines(sess, template_id, size=10):
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


def list_template_jobs(sess, template_id, size=10):
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


def list_template_pipeline_jobs(sess, template_id, pipeline_id, size=10):
    data = get_template_pipeline_data(sess, template_id, pipeline_id, size)
    return [{'name': node['name']} for node in data['nodes']]


def get_template_pipeline_data(sess, template_id, pipeline_id, size=10):
    '''
    get data of a pipeline.
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

    return pipelines[0]['data']


def create_template_pipeline_job(sess, template_id, pipeline_template_name):
    '''
    create a pipeline job of template.
    '''
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


def delete_template_pipeline_job(sess, template_id, job_id):
    '''
    delete a pipeline job of template.
    '''
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/{job_id}/delete'

    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False


def delete_template_pipeline(sess, template_id, pipeline_id):
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/{pipeline_id}/delete'

    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False


def copy_template_pipeline(sess, template_id, src_pipeline_id, pipeline_name):
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/create'

    req_data = {'engineTemplateId': template_id,
                'pipelineKey': pipeline_name + '_' + str(uuid.uuid1())[:8]}
    data = get_template_pipeline_data(sess, template_id, src_pipeline_id)
    data['name'] = pipeline_name
    data['describe'] = f'pipeline copied from pipelineID={src_pipeline_id}.'
    req_data['data'] = data

    resp = sess.post(url, data=json.dumps(req_data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if resp.json()['status'] == 0 else False


def copy_template_job(sess, src_template_id, src_job_id):
    pass


if __name__ == '__main__':

    workspace_id = '1'
    instance_id = '38'
    running_template_id = '1'
    running_pipeline_id = '1'
    pipeline_task_id = '19'

    template_id = '10032'
    pipeline_id = '65'
    job_id = '117'

    sess = login()
    try:
        # flowengine
        # logger.info(list_running_flowengines(sess, workspace_id))

        # logger.info(list_fl_pipelines(sess, instance_id, template_id))
        # ret = run_fl_pipeline(sess, instance_id, template_id, pipeline_id)

        # logger.info(list_fl_pipeline_tasks(sess, instance_id, pipeline_id))
        # ret = resume_fl_pipeline_task(sess, instance_id, pipeline_id, pipeline_task_id)
        # ret = stop_fl_pipeline_task(sess, instance_id, pipeline_id, pipeline_task_id)
        # assert(ret)

        # template
        # logger.info(list_template_pipelines(sess, template_id))
        # logger.info(list_template_jobs(sess, template_id))
        # logger.info(list_template_pipeline_jobs(sess, template_id, pipeline_id))

        # ret = create_template_pipeline_job(sess, template_id, 'offline-job04')
        # ret = delete_template_pipeline_job(sess, template_id, job_id)
        # ret = delete_template_pipeline(sess, template_id, pipeline_id)

        pipeline_key = 'copied_pipeline_test03'
        ret = copy_template_pipeline(
            sess, template_id, pipeline_id, pipeline_key)
        assert(ret)
    finally:
        sess.close()

    logger.info('flowengine pipeline demo done.')
