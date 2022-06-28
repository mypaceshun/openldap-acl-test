from openldap_acl_test.conf import load_conf, load_testcases
from openldap_acl_test.testcase import ACL, ACLTestCase


def test_conf(success_conf):
    confdata = load_conf(success_conf)
    assert isinstance(confdata, dict)


def test_testcase(success_conf):
    confdata = {
        "testcases": [
            {
                "requester": "cn=admin,dc=example,dc=com",
                "target": "uid=testuser,ou=User,dc=example,dc=com",
                "acl": "manage",
                "attribute": ["cn"],
            }
        ]
    }
    testcases = load_testcases(confdata)
    assert len(testcases) == 1
    testcase = testcases[0]
    assert isinstance(testcase, ACLTestCase)
    assert testcase.requester == "cn=admin,dc=example,dc=com"
    assert testcase.acl == ACL.MANAGE
