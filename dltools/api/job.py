from dltools.api.api import CommAPI, run_api
from dltools.api.info import CombinedIssueInfo, DataMetaInfo, JobInfo, LabeledDataInfo, ReviewInfo,StatusInfo, TaskInfo

class JobAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(JobInfo)
        self.target_url = self.get_api_url('jobs')

    def get_anno(self, job_id:int):
        url = self.target_url + f'/{job_id}/annotaions'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return LabeledDataInfo(r.json())

    def put_anno(self, job_id:int, **kwd):
        url = self.target_url + f'/{job_id}/annotaions'
        r = self.session.put(url, data=kwd)
        self.r = r
        r.raise_for_status()
        return LabeledDataInfo(r.json())

    def patch_anno(self, job_id:int, **kwd):
        url = self.target_url + f'/{job_id}/annotaions'
        r = self.session.patch(url, data=kwd)
        self.r = r
        r.raise_for_status()
        return LabeledDataInfo(r.json())

    def del_anno(self, job_id:int):
        url = self.target_url + f'/{job_id}/annotaions'
        r = self.session.delete(url)
        self.r = r
        r.raise_for_status()
        return r.ok

    def get_issues(self, job_id:int):
        url = self.target_url + f'/{job_id}/issues'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return [CombinedIssueInfo(i) for i in r.json()]

    def get_reviews(self, job_id:int):
        url = self.target_url + f'/{job_id}/reviews'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return [ReviewInfo(i) for i in r.json()]