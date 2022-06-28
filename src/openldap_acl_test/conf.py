from pathlib import Path

import yaml

from openldap_acl_test.testcase import ACLTestCase


def load_conf(conffile: str) -> dict:
    """
    設定ファイルの読み込みを実施する関数

    YAMLファイルを読み込み ``acltest`` というキーの辞書を読み込む。
    """
    confpath = Path(conffile)
    confdata = {}
    with confpath.open() as fd:
        data = yaml.safe_load(fd)
        confdata = data.get("acltest", {})
    return confdata


def load_testcases(confdict: dict) -> list[ACLTestCase]:
    testcase_conf_list = confdict.get("testcases", {})
    default_acl = "read"
    default_attribute = ["objectClass", "cn", "uid"]
    testcases: list[ACLTestCase] = []
    for testcase_conf in testcase_conf_list:
        testcase = ACLTestCase(
            testcase_conf["requester"],
            testcase_conf["target"],
            testcase_conf.get("acl", default_acl),
            testcase_conf.get("attribute", default_attribute),
        )
        testcases.append(testcase)

    return testcases
