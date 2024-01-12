from kfsd.apps.core.management.commands.baserun import Command as BaseCommand
from kfsd.apps.core.common.logger import Logger, LogLevel


logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Command(BaseCommand):
    help = "Utils Pkg Setup"
    service_id = "utils_api"

    def getAppSerializers(self):
        return {}

    def getConfig(self):
        return {
            "kubefacets": {
                "env": {
                    "service_id": "{}".format(self.service_id),
                    "env": "dev",
                    "settings_id": "SETTING=Kubefacets",
                    "outbound_policy_id": "POLICY_TYPE=Events,POLICY_NAME=Outbound",
                    "inbound_policy_id": "POLICY_TYPE=Events,POLICY_NAME=Inbound",
                },
                "cleanup": [self.update_utils_pkg, self.clean_db],
                "migrate": [
                    "python manage.py makemigrations",
                    "python manage.py migrate",
                ],
                "setup_fixtures": [
                    "v1/kubefacets/config/settings.json",
                    "v1/kubefacets/msmq/base.json",
                    "v1/kubefacets/policies/base.json",
                    "v1/kubefacets/msmq/inbound/auth/routes.json",
                    "v1/kubefacets/msmq/inbound/common/rules/clear_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/clear_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/user_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/user_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/org_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/org_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/team_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/team_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/role_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/role_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/apikey_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/apikey_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/access_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/access_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/service_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/service_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/rules/plan_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/signals/plan_tbl.json",
                    "v1/kubefacets/msmq/inbound/common/routes.json",
                    "v1/kubefacets/msmq/inbound/queues.json",
                    "v1/kubefacets/msmq/outbound/common/rules/clear_tbl.json",
                    "v1/kubefacets/msmq/outbound/common/signals/clear_tbl.json",
                ],
                "data_fixtures": [],
                "msmq": "python manage.py basemsmq -s={}".format(self.service_id),
                "server": "python manage.py runserver 8000",
            }
        }
