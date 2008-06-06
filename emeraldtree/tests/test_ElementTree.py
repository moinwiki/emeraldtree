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

    assert isinstance(elem, Node)
    assert elem.tag == 'a'

def test_Element__len__():
    elem = Element('a', children = range(10))

    assert len(elem) == 10

def test_Element__nonzero__():
    elem = Element('a')

    assert elem
    assert len(elem) == 0

def test_Element___getitem__():
    elem = Element('a', children = [Element('b'), Element('c')])

    assert elem[0].tag == 'b'
    assert elem[1].tag == 'c'
    assert len(elem[:1]) == 1
    assert len(elem[:2]) == 2
    assert len(elem[:3]) == 2
    assert len(elem[1:3]) == 1
    assert len(elem[2:3]) == 0
    assert elem[:2][0].tag == 'b'
    assert elem[:2][1].tag == 'c'

def test_Element___setitem__():
    elem = Element('a', children = [Element('b1'), Element('b2')])

    elem[0] = Element('c')
    assert elem[0].tag == 'c'
    assert elem[1].tag == 'b2'

    elem[1] = Element('d')
    assert elem[0].tag == 'c'
    assert elem[1].tag == 'd'

    elem[0:0] = [Element('e')]
    assert elem[0].tag == 'e'
    assert elem[1].tag == 'c'
    assert elem[2].tag == 'd'

def test_Element___delitem__():
    elem = Element('a', children = [Element('b1'), Element('b2')])

    del elem[0]
    assert len(elem) == 1
    assert elem[0].tag == 'b2'

def test_Element_append():
    elem = Element('a')

    elem.append(Element('b'))
    assert len(elem) == 1
    assert elem[0].tag == 'b'

    elem.append(Element('c'))
    assert len(elem) == 2
    assert elem[1].tag == 'c'

    elem.append('d')
    assert len(elem) == 3
    assert elem[2] == 'd'

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
    assert isinstance(elem, Element)
    assert len(elem) == 1
    assert elem[0] == 'b'
    assert isinstance(elem[0], unicode)

def test_XMLParser_text2():
    elem = XML('<a>b<c>d</c>d</a>')
    assert elem.tag == 'a'
    assert len(elem) == 3
    assert elem[0] == 'b'
    assert elem[1].tag == 'c'
    assert elem[2] == 'd'

def test_XMLParser_namespace():
    elem = XML('<a:a xmlns:a="a"/>')
    assert elem.tag == QName('a', 'a')
    assert serialize(elem) == '<ns0:a xmlns:ns0="a" />'

    elem = XML('<a:a xmlns:a="a" a="a"/>')
    assert elem.tag == QName('a', 'a')
    assert elem.attrib == {'a': 'a'}
    assert serialize(elem) == '<ns0:a a="a" xmlns:ns0="a" />'

    elem = XML('<a:a xmlns:a="a" a:a="a"/>')
    assert elem.tag == QName('a', 'a')
    assert elem.attrib == {QName('a', 'a'): 'a'}
    assert serialize(elem) == '<ns0:a ns0:a="a" xmlns:ns0="a" />'

