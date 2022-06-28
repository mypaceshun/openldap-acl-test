import pytest
from openldap_acl_test.testcase import ACL, ACLTestCase, ACLTestResult
from openldap_acl_test.exceptions import ACLCheckError, ACLNoCheckAttributeError


def test_ACL():
    assert ACL.MANAGE == "manage"
    assert ACL.WRITE == "write"
    assert ACL.READ == "read"
    assert ACL.AUTH == "auth"
    assert ACL.NONE == "none"
    assert isinstance(ACL.READ, ACL)


def test_ACLTestResult():
    res = ACLTestResult(True, "msg")
    assert res.result is True
    assert res.msg == "msg"


def test_testcase():
    requester = "requester"
    target = "target"
    testcase = ACLTestCase(requester=requester, target=target)
    assert testcase.requester == requester
    assert testcase.target == target
    assert testcase.acl == ACL.READ
    assert testcase.acl == "read"
    assert testcase.attributes == []


@pytest.mark.parametrize("requester,target,acl,attributes,expect_args", [
    ("A", "B","read", None, ["-D", "A", "-b", "B"]),
    ("A", "B", "write", ["cn"], ["-D", "A", "-b", "B", "cn/write"]),
    ("A", "B", "none", ["cn"], ["-D", "A", "-b", "B", "cn"]),
    ("A", "B", "manage", ["cn", "sn"], ["-D", "A", "-b", "B", "cn/manage", "sn/manage"]),
    ("self", "B", "write", ["cn"], ["-D", "B", "-b", "B", "cn/write"]),
    ("anonymous", "B", "write", ["cn"], ["-b", "B", "cn/write"]),
    ])
def test_testcase_get_slapacl_args(requester, target, acl, attributes, expect_args):
    testcase = ACLTestCase(requester, target, acl, attributes)
    args = testcase.get_slapacl_args()
    assert args == expect_args


def test_testcase_check_slapacl_error():
    testcase = ACLTestCase("A", "B")
    line = "error line"
    with pytest.raises(ACLCheckError):
        testcase.check_slapacl(line)


def test_testcase__check_slapacl():
    acl = "read"
    attributes = ["cn"]
    testcase = ACLTestCase("A", "B", acl, attributes)
    before_text = "read cn"
    after_text = "ALLOWED"
    msg = testcase._check_slapacl(before_text, after_text)
    assert isinstance(msg, str)


def test_testcase__check_slapacl_no_check():
    acl = "read"
    attributes = ["cn"]
    testcase = ACLTestCase("A", "B", acl, attributes)
    before_text = "read sn"
    after_text = "ALLOWED"
    with pytest.raises(ACLNoCheckAttributeError):
        testcase._check_slapacl(before_text, after_text)

def test_testcase__check_slapacl_error():
    acl = "read"
    attributes = ["cn"]
    testcase = ACLTestCase("A", "B", acl, attributes)
    before_text = "write cn"
    after_text = "ALLOWED"
    with pytest.raises(ACLCheckError):
        testcase._check_slapacl(before_text, after_text)

    before_text = "read cn"
    after_text = "DENIED"
    with pytest.raises(ACLCheckError):
        testcase._check_slapacl(before_text, after_text)


def test_testcase__check_slapacl_none():
    acl = "read"
    attributes = ["cn"]
    testcase = ACLTestCase("A", "B", acl, attributes)
    before_text = "cn"
    after_text = "none(=0)"
    msg = testcase._check_slapacl_none(before_text, after_text)
    assert isinstance(msg, str)

def test_testcase__check_slapacl_none_no_check():
    acl = "read"
    attributes = ["cn"]
    testcase = ACLTestCase("A", "B", acl, attributes)
    before_text = "sn"
    after_text = "none(=0)"
    with pytest.raises(ACLNoCheckAttributeError):
        testcase._check_slapacl_none(before_text, after_text)


def test_testcase__check_slapacl_none_error():
    acl = "read"
    attributes = ["cn"]
    testcase = ACLTestCase("A", "B", acl, attributes)
    before_text = "cn"
    after_text = "read(=0)"
    with pytest.raises(ACLCheckError):
        testcase._check_slapacl_none(before_text, after_text)

def test_testcase_get_count():
    testcase = ACLTestCase("A", "B")
    testcase.result_list = [
        ACLTestResult(True, ""),
        ACLTestResult(False, ""),
        ACLTestResult(True, ""),
        ACLTestResult(True, ""),
        ACLTestResult(False, ""),
    ]
    assert testcase.get_success_count() == 3
    assert testcase.get_failure_count() == 2
    assert testcase.get_result_dots() == ".x..x"
