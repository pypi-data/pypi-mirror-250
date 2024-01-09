from kfsd.apps.frontend.permissions.base import BasePermission
from kfsd.apps.core.exceptions.fe import KubefacetsFEException
from http import HTTPStatus


class IsStaff(BasePermission):
    def __init__(self, request):
        BasePermission.__init__(self, request)

    def __str__(self):
        return "Is staff check"

    def is_valid(self):
        if self.getUser().isStaff():
            return True
        return False

    def raise_exception(self):
        raise KubefacetsFEException(self.__str__(), HTTPStatus.FORBIDDEN, None)

    def redirect_url(self):
        return ""

    def redirect_url_neg(self):
        return ""

    def raise_exception_neg(self):
        raise KubefacetsFEException(self.__str__(), HTTPStatus.FORBIDDEN, None)
