import pytest


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--htmllint', action='store_true', dest='htmllint')

    parser.addini(
        'htmllint_exclude',
        type='linelist',
        help='A list of paths to exclude from HTML linting'
    )


def pytest_collect_file(path, parent):
    conf = parent.config
    if conf.option.htmllint:
        if path_is_excluded(path, conf.getini('htmllint_exclude')):
            return None
        elif path.ext == '.html':
            return HtmlItem(path, parent)
            

def path_is_excluded(path, excluded):
    for dirname in excluded:
        if path.fnmatch(dirname):
            return True

    return False


class HtmlLintViolation(Exception):
    pass


class HtmlItem(pytest.Item, pytest.File):
    def runtest(self):
        for lineno, line in enumerate(self.fspath.readlines(), start=1):
            filepath = '/'.join((self.fspath.dirname, self.fspath.basename))

            # Check for tabstops
            if '\t' in line:
                raise HtmlLintViolation('%s: Found tabstop (line %d)' % (
                    filepath, lineno
                ))

            # Check for trailing whitespace
            if len(line) != len(line.rstrip()):
                raise HtmlLintViolation(
                    '%s: Found trailing whitespace (line %d)' % (
                        filepath, lineno
                    )
                )

