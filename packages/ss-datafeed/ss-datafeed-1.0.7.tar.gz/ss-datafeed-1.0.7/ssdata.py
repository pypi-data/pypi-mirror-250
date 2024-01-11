from ssdata_util import query,sqlone
from ssdata_datasource import SS_DATASOURCE

class ssdata:
    def __init__(self, appId, appSec):
        self.appId = appId
        self.appSec = appSec
    def dataset(self,sql,*params,datasource=SS_DATASOURCE.DS_EFORM):
        result = query(self.appId,self.appSec,sql,*params,
                                   datasource=datasource)
        return result
    def sqlone(self, sql, *params, datasource=SS_DATASOURCE.DS_EFORM):
        result = sqlone(self.appId, self.appSec, sql, *params,
                       datasource=datasource)
        return result

