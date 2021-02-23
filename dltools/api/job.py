from dltools.api.api import CommAPI, run_api
from dltools.api.info import CombinedIssueInfo, DataMetaInfo, JobInfo, LabeledDataInfo, ReviewInfo,StatusInfo, TaskInfo

class JobAPI(CommAPI):
    def __init__(self) -> None:
        super().__init__(JobInfo)
        self.target = 'jobs'
        self.target_url = self.get_api_url(self.target)

    def get_annotations(self, job_id:int):
        url = self.target_url + f'/{job_id}/annotations'
        r = self.session.get(url)
        self.r = r
        r.raise_for_status()
        return LabeledDataInfo(r.json())

    def put_annotations(self, job_id:int, **kwd):
        url = self.target_url + f'/{job_id}/annotaions'
        r = self.session.put(url, data=kwd)
        self.r = r
        r.raise_for_status()
        return LabeledDataInfo(r.json())

    def patch_annotations(self, job_id:int, **kwd):
        url = self.target_url + f'/{job_id}/annotaions'
        r = self.session.patch(url, data=kwd)
        self.r = r
        r.raise_for_status()
        return LabeledDataInfo(r.json())

    def del_annotations(self, job_id:int):
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