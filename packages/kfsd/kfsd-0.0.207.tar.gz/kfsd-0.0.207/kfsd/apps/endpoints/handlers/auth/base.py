from rest_framework.exceptions import ValidationError

from kfsd.apps.endpoints.handlers.relations.base import BaseHRelHandler
from kfsd.apps.core.utils.system import System
from kfsd.apps.models.constants import ENV_RESOURCE_POLICY_ID
from kfsd.apps.endpoints.handlers.validations.policy import (
    gen_policy_handler,
    PolicyHandler,
)
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class BasePermHandler(BaseHRelHandler):
    DEFAULT_RESOURCE_POLICY_ID = "POLICY_TYPE=Events,POLICY_NAME=Resource"

    def __init__(self, **kwargs):
        BaseHRelHandler.__init__(self, **kwargs)

    def getResourcePolicyFinderId(self):
        policyID = System.getEnv(ENV_RESOURCE_POLICY_ID)
        return policyID if policyID else self.DEFAULT_RESOURCE_POLICY_ID

    def setPolicy(self):
        policyId = self.getResourcePolicyFinderId()
        policyHandler = PolicyHandler(policyId, True)
        data = {"resource": self.getModelQSData()}
        policyHandler.exec(data)
        matchedPolicies = policyHandler.getEvaluatedValues()
        if len(matchedPolicies) != 1:
            logger.error(
                "Matched Policies: {} for Data: {}".format(matchedPolicies, data)
            )
            raise ValidationError(
                "Resource: {} matches more than 1 policy or no policy found".format(
                    self.getIdentifier()
                ),
                "policy_error",
            )
        logger.debug(
            "[{}] Assigned Policy: {}".format(
                self.getIdentifier(),
                matchedPolicies[0],
            )
        )
        self.getModelQS().policy = PolicyHandler(matchedPolicies[0], True).getModelQS()
        self.getModelQS().save()

    def getPolicyHandler(self):
        if not self.getModelQS().policy:
            return None
        return gen_policy_handler(self.getModelQS().policy)

    def authorize(self, user, ctx):
        userData = user.getModelQSData()
        resourceData = self.getModelQSData()
        data = {"user": userData, "resource": resourceData, "ctx": ctx}
        policyHandler = self.getPolicyHandler()
        policyHandler.exec(data)
        return policyHandler
