# coding: utf-8
import json
import logging
import requests


class JiraTools(object):

    _jira_rest_url = 'https://jira.xxxxx.io/rest/api'
    # token: echo -n 'username:password' | base64
    _auth_token = 'base64 token'

    def __init__(self):
        self.sess = requests.session()
        default_headers = {'Authorization': 'Basic ' +
                           self._auth_token, 'Content-Type': 'application/json'}
        self.sess.headers.update(default_headers)

    def search(self, query: str, limit=3, fields=['id', 'key']):
        url = self._jira_rest_url + '/2/search'
        query_dict = {
            'jql': query,
            'maxResults': limit,
            'fields': fields,
        }
        resp = self.sess.post(url, json=query_dict)
        assert(resp.status_code == 200)
        print('ret_code=%d, ret_text=%s' % (resp.status_code, resp.text))

    def get_issue(self, jira_id, expand_fields: list):
        expend = ','.join(expand_fields)
        url = f'{self._jira_rest_url}/latest/issue/{jira_id}?expand={expend}'
        resp = self.sess.get(url)
        assert(resp.status_code == 200)

        json_text = resp.text
        json_object = json.loads(json_text)
        label = json_object['fields']['labels']
        desc = json_object['renderedFields']['description']
        resolution = json_object['names']['resolution']
        print(
            f'issue [{jira_id}] info: label={label}, description={desc}, resolution={resolution}')

    def close(self):
        if self.sess is not None:
            self.sess.close()


if __name__ == '__main__':

    jira = JiraTools()
    jira_id = 'jira-57878'
    expand_fields = ['names', 'renderedFields']
    jira.get_issue(jira_id, expand_fields)

    jql = 'assignee="jin.zheng@xxxxx.com" AND resolution=Unresolved'
    jira.search(jql)
    jira.close()

    print('jira demo done.')
