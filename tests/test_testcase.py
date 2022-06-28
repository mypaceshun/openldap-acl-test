from openldap_acl_test.testcase import ACL, ACLTestCase


def test_ACL():
    assert ACL.MANAGE == "manage"
    assert ACL.WRITE == "write"
    assert ACL.READ == "read"
    assert ACL.AUTH == "auth"
    assert ACL.NONE == "none"
    assert isinstance(ACL.READ, ACL)


def test_testcase():
    requester = "requester"
    target = "target"
    testcase = ACLTestCase(requester=requester, target=target)
    assert testcase.requester == requester
    assert testcase.target == target
    assert testcase.acl == ACL.READ
    assert testcase.acl == "read"
    assert testcase.attributes == []
