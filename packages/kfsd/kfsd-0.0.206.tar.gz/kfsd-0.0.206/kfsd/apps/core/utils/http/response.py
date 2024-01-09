from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.utils.http.headers.cookie import Cookie
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Response(Cookie):
    def __init__(self):
        self.__response = None

    def getResponse(self):
        return self.__response

    def getUrl(self):
        return self.__response.url

    def getJsonResponse(self):
        return self.__response.json()

    def setResponse(self, response):
        self.__response = response
        self.setCookiesHttpObj(response)

    def getStatusCode(self):
        return self.__response.status_code

    def isRespJSON(self):
        if (
            "application/json"
            in self.__response.headers.get("content-type", "").lower()
        ) and self.__response.content:
            return True
        return False

    def raiseAPIException(self, detail="Unknown error detail", code="unexpected_error"):
        resp = self.getJsonResponse() if self.isRespJSON() else {}
        errorStr = DictUtils.get(resp, "detail", detail)
        errorCode = DictUtils.get(resp, "code", code)
        raise KubefacetsAPIException(errorStr, errorCode, self.getStatusCode())

    def summary(self, expCode):
        return {
            "url": self.__response.url,
            "obs_status": self.__response.status_code,
            "exp_status": expCode,
            "req_body": self.__response.request.body,
            "req_headers": self.__response.request.headers,
            "req_method": self.__response.request.method,
            "resp_body": self.getJsonResponse()
            if self.isRespJSON()
            else "<NON JSON CONTENT>"
            if self.__response.request.method != "DELETE"
            else "<NON JSON CONTENT>",
            "resp_headers": self.__response.headers,
        }

    def isRespValid(self, expStatusCode):
        logger.debug(self.summary(expStatusCode))
        if isinstance(expStatusCode, int) and not expStatusCode == self.getStatusCode():
            logger.error(self.summary(expStatusCode))
            self.raiseAPIException(
                "Resp code mismatch, expected: {}, obs: {}".format(
                    expStatusCode, self.getStatusCode()
                )
            )

        if (
            isinstance(expStatusCode, list)
            and self.getStatusCode() not in expStatusCode
        ):
            self.raiseAPIException(
                "Resp code mismatch, expected: {}, obs: {}".format(
                    expStatusCode, self.getStatusCode()
                )
            )

        return True
