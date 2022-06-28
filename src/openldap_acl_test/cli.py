import click

from openldap_acl_test import __name__, __version__
from openldap_acl_test.conf import load_conf, load_testcases
from openldap_acl_test.log import init_logger
from openldap_acl_test.testcase import ACLTestCase


@click.command()
@click.version_option(version=__version__, package_name=__name__)
@click.help_option("-h", "--help")
@click.option(
    "-c",
    "--conffile",
    help="conffile path",
    type=click.Path(exists=True),
    default="acltest_conf.yml",
    show_default=True,
    envvar="ACLTEST_CONFFILE",
)
@click.option("-v", "--verbose", help="verbose output", is_flag=True)
def main(verbose, conffile):
    logger = init_logger("INFO")
    if verbose:
        logger = init_logger("DEBUG")
    logger.info("run script")
    logger.debug(f"load conffile {conffile=}")
    testcases: list[ACLTestCase] = []
    try:
        confdata = load_conf(conffile)
        testcases = load_testcases(confdata)
    except Exception as error:
        raise click.FileError(conffile, hint=error)

    for testcase in testcases:
        logger.info(f"RUN TEST {testcase.requester} -> {testcase.target}")
