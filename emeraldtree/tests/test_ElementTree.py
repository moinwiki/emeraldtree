import py.test
from emeraldtree.ElementTree import *

def serialize(elem, **options):
    from cStringIO import StringIO
    file = StringIO()
    tree = ElementTree(elem)
    tree.write(file, **options)
    return file.getvalue()

def test_Element():
    elem = Element('a')
    assert serialize(elem) == '<a />'
    assert isinstance(elem, Node)

def test_Element_append():
    elem = Element('a')
    elem.append(Element('b'))
    assert serialize(elem) == '<a><b /></a>'

    elem.append(Element('c'))
    assert serialize(elem) == '<a><b /><c /></a>'

    elem.append('d')
    assert serialize(elem) == '<a><b /><c />d</a>'

def test_Element_iter():
    elem = Element('a')
    l = list(elem.iter())
    assert len(l) == 1

    elem.append('b')
    l = list(elem.iter())
    assert len(l) == 1

    elem.append(Element('c'))
    l = list(elem.iter())
    assert len(l) == 2

    elem.append('d')
    l = list(elem.iter())
    assert len(l) == 2

def test_Element_itertext():
    elem = Element('a')
    l = list(elem.itertext())
    assert len(l) == 0

    elem.append('b')
    l = list(elem.itertext())
    assert len(l) == 1

def test_Comment():
    elem = Comment('a')
    assert serialize(elem) == '<!--a-->'
    assert isinstance(elem, Node)

def test_ProcessingInstruction():
    elem = ProcessingInstruction('a')
    assert serialize(elem) == '<?a?>'
    assert isinstance(elem, ProcessingInstruction)

    elem = ProcessingInstruction('a', 'b')
    assert serialize(elem) == '<?a b?>'

def test_QName():
    qname = QName('a')
    assert qname.uri is None
    assert qname.name == 'a'
    assert str(qname) == 'a'
    assert qname.text == 'a'

    qname = QName('{b}a')
    assert qname.uri == 'b'
    assert qname.name == 'a'
    assert str(qname) == '{b}a'
    assert qname.text == '{b}a'

    qname = QName('a', 'b')
    assert qname.uri == 'b'
    assert qname.name == 'a'
    assert str(qname) == '{b}a'
    assert qname.text == '{b}a'

    py.test.raises(ValueError, QName, '{ba')
    py.test.raises(ValueError, QName, '{b}a', 'c')

def test_XMLParser_simple1():
    elem = XML('<a />')
    assert elem.tag == 'a'
    assert len(elem) == 0

def test_XMLParser_simple2():
    elem = XML('<a><b /></a>')
    assert elem.tag == 'a'
    assert len(elem) == 1
    assert elem[0].tag == 'b'
    assert len(elem[0]) == 0

def test_XMLParser_text1():
    elem = XML('<a>b</a>')
    assert elem.tag == 'a'
    assert len(elem) == 1

def test_XMLParser_text2():
    elem = XML('<a>b<c>d</c>d</a>')
    assert elem.tag == 'a'
    assert len(elem) == 3
    assert elem[0] == 'b'
    assert elem[1].tag == 'c'
    assert elem[2] == 'd'
