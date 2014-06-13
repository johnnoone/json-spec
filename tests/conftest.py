import sys


def pytest_cmdline_preparse(args):
    if 'pytest_cov' in sys.modules: # pytest-xdist plugin
        args[:] = ['--cov', 'jsonspec', '--cov-report', 'html'] + args
