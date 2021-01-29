# coding: utf-8
import json
import logging
import requests
import time


class JiraTools(object):

    _jira_rest_api_url = 'https://jira.xxxxx.io/rest/api'
    # token: echo -n 'username:password' | base64
    _auth_token = 'base64 token'

    def __init__(self):
        self.sess = requests.session()
        default_headers = {'Authorization': 'Basic ' +
                           self._auth_token, 'Content-Type': 'application/json'}
        self.sess.headers.update(default_headers)

    def search(self, query: str, limit=3, fields=['id', 'key']):
        url = f'{self._jira_rest_api_url}/2/search'
        query_dict = {
            'jql': query,
            'maxResults': limit,
            'fields': fields,
        }
        resp = self.sess.post(url, json=query_dict)
        assert(resp.status_code >= 200)
        print('ret_code=%d, ret_text=%s' % (resp.status_code, resp.text))

    def get_issue(self, issue_id, expand_fields: list):
        expend = ','.join(expand_fields)
        url = f'{self._jira_rest_api_url}/latest/issue/{issue_id}?expand={expend}'
        resp = self.sess.get(url)
        assert(resp.status_code >= 200)

        json_text = resp.text
        json_object = json.loads(json_text)
        label = json_object['fields']['labels']
        desc = json_object['renderedFields']['description']
        resolution = json_object['names']['resolution']
        print(
            f'issue [{issue_id}] info: label={label}, description={desc}, resolution={resolution}')

    '''
    remote issue link api:
    https://developer.atlassian.com/server/jira/platform/jira-rest-api-for-remote-issue-links/
    '''

    def add_remote_issue_link(self, issue_id, link, title):
        url = f'{self._jira_rest_api_url}/latest/issue/{issue_id}/remotelink'
        favicon_url = 'https://git.xxxxx.com/assets/favicon-7901bd695fb93edb07975966062049829afb56cf11511236e61bcf425070e36e.png'
        link_data = {
            'object': {
                'url': link,
                'title': title,
                'icon': {
                    'url16x16': favicon_url,
                    'title': 'Gitlab'
                }
            }
        }
        resp = self.sess.post(url, json=link_data)
        assert(resp.status_code >= 200)
        print(resp.text)

    def get_remote_issue_links(self, issue_id):
        url = f'{self._jira_rest_api_url}/latest/issue/{issue_id}/remotelink'
        resp = self.sess.get(url)
        assert(resp.status_code >= 200)
        print(resp.text)

    def delete_remote_issue_link(self, issue_id, link_id):
        url = f'{self._jira_rest_api_url}/latest/issue/{issue_id}/remotelink/{link_id}'
        resp = self.sess.delete(url)
        assert(resp.status_code >= 200)
        print(resp.text)

    def close(self):
        if self.sess is not None:
            self.sess.close()


if __name__ == '__main__':

    jira = JiraTools()
    # get a issue
    issue_id = 'AIRPAY-54667'
    expand_fields = ['names', 'renderedFields']
    jira.get_issue(issue_id, expand_fields)

    # search issues by query
    jql = 'assignee="jin.zheng@xxxxx.com" AND resolution=Unresolved'
    jira.search(jql)

    # add issue link
    issue_id = 'AIRPAY-54665'
    link = 'https://git.xxxxx.com/jin.zheng/zhengjin_worksapce/-/merge_requests/1'
    title = f'[Merge Request] - {issue_id} / Update workspace readme.'
    jira.add_remote_issue_link(issue_id, link, title)

    # get issue links
    time.sleep(1)
    jira.get_remote_issue_links(issue_id)

    # delete issue link
    # link_id = '1194974'
    # jira.delete_remote_issue_link(issue_id, link_id)

    jira.close()
    print('jira demo done.')
