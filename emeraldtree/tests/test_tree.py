import py.test
from emeraldtree.tree import *

def serialize(elem, namespaces={}):
    from StringIO import StringIO
    file = StringIO()
    XMLWriter(namespaces=namespaces).write(file.write, elem)
    return file.getvalue()

def test_Element():
    elem = Element('a')

    assert isinstance(elem, Node)
    assert elem.tag == 'a'

def test_Element__len__():
    elem = Element('a', children=['1', '2', '3', '4', '5'])

    assert len(elem) == 5

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

def test_Element_extend():
    pass

def test_Element_insert():
    pass

def test_Element_remove():
    pass

def test_Element_find():
    child_1 = Element('b1')
    child_2 = Element('b2')
    elem = Element('a', children=[child_1, child_2])

    result = elem.find('b1')
    assert result is child_1

    result = elem.find('b2')
    assert result is child_2

    child_1 = Element(QName('b1', 'url1'))
    child_2 = Element(QName('{url2}b2'))
    elem = Element('a', children=[child_1, child_2])

    result = elem.find('{url1}b1')
    assert result is child_1

def test_Element_findtext():
    pass

def test_Element_findall():
    child_1 = Element('b1')
    child_2 = Element('b2')
    child_3 = u"text"
    elem = Element('a', children=[child_1, child_2, child_3])

    result = list(elem.findall('b1'))
    assert len(result) == 1
    assert result[0] is child_1

    result = list(elem.findall('b2'))
    assert len(result) == 1
    assert result[0] is child_2

    result = list(elem.findall('*'))
    assert len(result) == 3
    assert result[0] is child_1
    assert result[1] is child_2
    assert result[2] is child_3

    child_1 = Element(QName('b1', 'url1'))
    child_2 = Element(QName('{url2}b2'))
    elem = Element('a', children=[child_1, child_2])

    result = list(elem.findall('{url1}b1'))
    assert len(result) == 1
    assert result[0] is child_1

def test_Element_clear():
    pass

def test_Element_get():
    pass

def test_Element_set():
    pass

def test_Element_keys():
    pass

def test_Element_items():
    pass

def test_Element_iter():
    elem = Element('a')
    l = list(elem.iter())
    assert len(l) == 1

    elem.append('b')
    l = list(elem.iter())
    assert len(l) == 2

    elem.append(Element('c'))
    l = list(elem.iter())
    assert len(l) == 3

    elem.append('d')
    l = list(elem.iter())
    assert len(l) == 4

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

def test_QName___init__():
    qname = QName('a')
    assert qname.uri is None
    assert qname.name == 'a'
    assert isinstance(qname.name, unicode)
    assert str(qname) == 'a'
    assert qname.text == 'a'

    qname = QName('{b}a')
    assert qname.uri == 'b'
    assert isinstance(qname.uri, unicode)
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

def test_QName___cmp__():
    qname1 = QName('a')
    qname2 = QName('a')

    assert qname1 == qname2
    assert qname1 == 'a'
    assert 'a' == qname1

    qname1 = QName('a', 'b')
    qname2 = QName('{b}a')

    assert qname1 == qname2
    assert qname1 == '{b}a'
    assert '{b}a' == qname1

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

def test_XMLParser_namespace_1():
    elem = XML('<b xmlns="c" d="e"/>')
    assert isinstance(elem.tag, QName)
    assert elem.tag == QName('b', 'c')
    assert elem.attrib == {QName('d', None): 'e'}
    assert serialize(elem) == '<ns0:b d="e" xmlns:ns0="c" />'
    assert serialize(elem, namespaces={'c': ''}) == '<b d="e" xmlns="c" />'

def test_XMLParser_namespace_2():
    elem = XML('<a:b xmlns:a="c" d="e" a:f="g"/>')
    assert isinstance(elem.tag, QName)
    assert elem.tag == QName('b', 'c')
    assert elem.attrib == {'d': 'e', QName('f', 'c'): 'g'}
    assert serialize(elem) == '<ns0:b d="e" ns0:f="g" xmlns:ns0="c" />'
    assert serialize(elem, namespaces={'c': ''}) == '<b d="e" f="g" xmlns="c" />'


