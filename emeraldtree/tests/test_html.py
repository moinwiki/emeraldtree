import py.test
from emeraldtree.ElementTree import *
from emeraldtree.html import *

def serialize(elem, **options):
    from cStringIO import StringIO
    file = StringIO()
    tree = ElementTree(elem)
    tree.write(file, **options)
    return file.getvalue()

def test_HTMLParser_simple1():
    elem = HTML('<a></a>')
    assert elem.tag.name == 'a'
    assert len(elem) == 0

def test_HTMLParser_simple2():
    elem = HTML('<a><b /></a>')
    assert elem.tag.name == 'a'
    assert len(elem) == 1
    assert elem[0].tag.name == 'b'
    assert len(elem[0]) == 0

def test_HTMLParser_text1():
    elem = HTML('<a>b</a>')
    assert elem.tag.name == 'a'
    assert isinstance(elem, Element)
    assert len(elem) == 1
    assert elem[0] == 'b'
    assert isinstance(elem[0], unicode)

def test_HTMLParser_text2():
    elem = HTML('<a>b<c>d</c>d</a>')
    assert elem.tag.name == 'a'
    assert len(elem) == 3
    assert elem[0] == 'b'
    assert elem[1].tag.name == 'c'
    assert elem[2] == 'd'

def test_HTMLParser_ignoreend():
    elem = HTML('<br>')
    assert elem.tag.name == 'br'
    assert len(elem) == 0

    elem = HTML('<br></br>')
    assert elem.tag.name == 'br'
    assert len(elem) == 0


