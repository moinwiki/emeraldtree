import py.test

from .. import html, tree

def serialize(elem, method):
    from StringIO import StringIO
    file = StringIO()
    elem.write(file.write, method=method)
    return file.getvalue()

def test_read_simple1():
    elem = html.HTML('<a></a>')
    assert elem.tag.name == 'a'
    assert len(elem) == 0

def test_read_simple2():
    elem = html.HTML('<a><b /></a>')
    assert elem.tag.name == 'a'
    assert len(elem) == 1
    assert elem[0].tag.name == 'b'
    assert len(elem[0]) == 0

def test_read_text1():
    elem = html.HTML('<a>b</a>')
    assert elem.tag.name == 'a'
    assert isinstance(elem, tree.Element)
    assert len(elem) == 1
    assert elem[0] == 'b'
    assert isinstance(elem[0], unicode)

def test_read_text2():
    elem = html.HTML('<a>b<c>d</c>d</a>')
    assert elem.tag.name == 'a'
    assert len(elem) == 3
    assert elem[0] == 'b'
    assert elem[1].tag.name == 'c'
    assert elem[2] == 'd'

def test_read_ignoreend():
    elem = html.HTML('<br>')
    assert elem.tag.name == 'br'
    assert len(elem) == 0

    elem = html.HTML('<br></br>')
    assert elem.tag.name == 'br'
    assert len(elem) == 0

def test_write():
    elem = html.HTML(u'<html><br><p></html>')
    h = serialize(elem, 'html')
    p = serialize(elem, 'polyglot')
    x = serialize(elem, 'xml')
    assert u'<br><p>' in h
    assert u'<br /><p></p>' in p
    assert u'<br /><p />' in x

