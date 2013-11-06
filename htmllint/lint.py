import pytest


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--htmllint', action='store_true', dest='htmllint')


def pytest_collect_file(path, parent):
    if parent.config.option.htmllint:
        if path.ext == '.html':
            return HtmlItem(path, parent)


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

