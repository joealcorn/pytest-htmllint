pytest_plugins = 'pytester'


tabdothtml = '''
<html>
<head>
\t<title>Hello</title>
</head>
'''

wsdothtml = '''
<html>
<title>Test!</title>  
</html>
'''


def test_tabstops(testdir):
    testdir.makefile('tab.html', tabdothtml)
    result = testdir.runpytest('--htmllint')
    assert result.parseoutcomes()['failed'] == 1


def test_trailing_ws(testdir):
    testdir.makefile('ws.html', wsdothtml)
    result = testdir.runpytest('--htmllint')
    assert result.parseoutcomes()['failed'] == 1


def test_excluded_file(testdir):
    testdir.makefile('ws.html', wsdothtml)
    testdir.makeini("""
        [pytest]
        add_opts=--htmllint
        htmllint_exclude=*.html
    """)
    result = testdir.runpytest()

    result.stdout.fnmatch_lines(['collected 0*'])

