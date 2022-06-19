import requests
import json


class RedashHelper:
    def __init__(self, config_helper, data_source):
        self.config_helper = config_helper
        self.group = 'INTERNAL_REDASH'
        self.cookie = self.config_helper.get_config(self.group, 'COOKIE')
        self.data_source_id = self.config_helper.get_config('DATA_SOURCE', data_source)
        print(f'Source Id: {self.data_source_id}')
        self.headers = headers = {
            'Cookie': self.cookie
        }

    def get_records_from_table(self, query):
        print(f'[Executing Query]: {query}')
        job_id = self.get_job_id(query)
        query_result_id = self.get_query_result_id(job_id)
        query_results = self.get_query_results(query_result_id)
        if len(query_results) == 0:
            print(f'0 records found for the query [ {query} ]')
            return []
        return query_results

    def get_job_id(self, query):
        data = json.dumps({
            "data_source_id": self.data_source_id,
            "max_age": 0,
            "parameters": {},
            "query": query
        })
        url = self.config_helper.get_config(self.group, 'ENDPOINT') + '/api/query_results'
        response = requests.request("POST", url, headers=self.headers, data=data)
        return json.loads(response.content.decode('utf-8'))['job']['id']

    def get_query_result_id(self, job_id):
        url = self.config_helper.get_config(self.group, 'ENDPOINT') + f'/api/jobs/{job_id}'
        response = requests.get(url, headers=self.headers)
        return json.loads(response.content.decode('utf-8'))['job']['query_result_id']

    def get_query_results(self, query_result_id):
        url = self.config_helper.get_config(self.group, 'ENDPOINT') + f'/api/query_results/{query_result_id}'
        response = requests.get(url, headers=self.headers)
        return json.loads(response.content.decode('utf-8'))['query_result']['data']['rows']
