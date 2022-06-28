from enum import Enum


class ACL(str, Enum):
    MANAGE = "manage"
    WRITE = "write"
    READ = "read"
    AUTH = "auth"
    NONE = "none"


class ACLTestCase:
    """
    テストケースを保持するクラス
    """

    def __init__(
        self,
        requester: str,
        target: str,
        acl: ACL = ACL.READ,
        attributes: list[str] = None,
    ):
        self.requester = requester
        self.target = target
        self.acl = acl
        if attributes is None:
            attributes = []
        self.attributes: list[str] = attributes
