import py.test
from emeraldtree.tree import *

def serialize(elem, namespaces={}):
    from StringIO import StringIO
    file = StringIO()
    XMLWriter(namespaces=namespaces).write(file.write, elem)
    return file.getvalue()

def test_Element():
    elem = Element(u'a')

    assert isinstance(elem, Node)
    assert elem.tag == u'a'

def test_Element__len__():
    elem = Element(u'a', children=(u'1', u'2', u'3', u'4', u'5'))

    assert len(elem) == 5

def test_Element__nonzero__():
    elem = Element(u'a')

    assert elem
    assert len(elem) == 0

def test_Element___getitem__():
    elem = Element(u'a', children=(Element(u'b'), Element(u'c')))

    assert elem[0].tag == u'b'
    assert elem[1].tag == u'c'
    assert len(elem[:1]) == 1
    assert len(elem[:2]) == 2
    assert len(elem[:3]) == 2
    assert len(elem[1:3]) == 1
    assert len(elem[2:3]) == 0
    assert elem[:2][0].tag == u'b'
    assert elem[:2][1].tag == u'c'

def test_Element___setitem__():
    elem = Element(u'a', children=(Element(u'b1'), Element(u'b2')))

    elem[0] = Element(u'c')
    assert elem[0].tag == u'c'
    assert elem[1].tag == u'b2'

    elem[1] = Element(u'd')
    assert elem[0].tag == u'c'
    assert elem[1].tag == u'd'

    elem[0:0] = [Element(u'e')]
    assert elem[0].tag == u'e'
    assert elem[1].tag == u'c'
    assert elem[2].tag == u'd'

def test_Element___delitem__():
    elem = Element(u'a', children=(Element(u'b1'), Element(u'b2')))

    del elem[0]
    assert len(elem) == 1
    assert elem[0].tag == u'b2'

def test_Element_append():
    elem = Element(u'a')

    elem.append(Element(u'b'))
    assert len(elem) == 1
    assert elem[0].tag == u'b'

    elem.append(Element(u'c'))
    assert len(elem) == 2
    assert elem[1].tag == u'c'

    elem.append(u'd')
    assert len(elem) == 3
    assert elem[2] == u'd'

def test_Element_extend():
    pass

def test_Element_insert():
    pass

def test_Element_remove():
    pass

def test_Element_find():
    child_1 = Element(u'b1')
    child_2 = Element(u'b2')
    elem = Element(u'a', children=(child_1, child_2))

    result = elem.find(u'b1')
    assert result is child_1

    result = elem.find(u'b2')
    assert result is child_2

    child_1 = Element(QName(u'b1', u'url1'))
    child_2 = Element(QName(u'{url2}b2'))
    elem = Element(u'a', children=(child_1, child_2))

    result = elem.find(u'{url1}b1')
    assert result is child_1

def test_Element_findall():
    child_1 = Element(u'b1')
    child_2 = Element(u'b2')
    child_3 = u"text"
    elem = Element(u'a', children=(child_1, child_2, child_3))

    result = list(elem.findall(u'b1'))
    assert len(result) == 1
    assert result[0] is child_1

    result = list(elem.findall(u'b2'))
    assert len(result) == 1
    assert result[0] is child_2

    result = list(elem.findall(u'*'))
    assert len(result) == 3
    assert result[0] is child_1
    assert result[1] is child_2
    assert result[2] is child_3

    child_1 = Element(QName(u'b1', u'url1'))
    child_2 = Element(QName(u'{url2}b2'))
    elem = Element(u'a', children=(child_1, child_2))

    result = list(elem.findall(u'{url1}b1'))
    assert len(result) == 1
    assert result[0] is child_1

def test_Element_findall_tag_multimatch():
    c1 = Element(u'c')
    c2 = Element(u'c')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))

    result = list(b1.findall(u'c'))
    assert len(result) == 2
    assert result[0] is c1
    assert result[1] is c2

    result = list(a1.findall(u'c'))
    assert len(result) == 0 # no 'c' childs

    result = list(a1.findall(u'*/c'))
    assert len(result) == 2 # but 2 'c' grandchilds
    assert result[0] is c1
    assert result[1] is c2

def test_Element_findall_bracketed_tag():
    c1 = Element(u'c')
    c2 = Element(u'c')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))

    result = list(b1.findall(u'[c]'))
    assert len(result) == 1
    assert result[0] is b1 # b1 has 'c' childs

    result = list(a1.findall(u'*/[c]'))
    assert len(result) == 1
    assert result[0] is b1 # b1 has 'c' childs

def test_Element_findall_dotdot():
    py.test.skip('broken')
    c1 = Element(u'c')
    c2 = Element(u'c')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))
    
    result = list(c1.findall(u'../c'))
    assert len(result) == 2
    assert result[0] is c1
    assert result[1] is c2

def test_Element_findall_slashslash():
    py.test.skip('broken')
    c1 = Element(u'c')
    c2 = Element(u'c')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))

    a1t = ElementTree(element=a1) # we need a tree to use //
    result = list(a1t.findall(u'//c'))
    assert len(result) == 2
    assert result[0] is c1
    assert result[1] is c2

def test_Element_findall_dotslashslash():
    py.test.skip('broken')
    c1 = Element(u'c')
    c2 = Element(u'c')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))

    result = list(a1.findall(u'.//c'))
    assert len(result) == 2
    assert result[0] is c1
    assert result[1] is c2

def test_Element_findall_attribute():
    c1 = Element(u'c')
    c2 = Element(u'c', testattr='testvalue')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))

    result = list(b1.findall(u"c[@testattr='testvalue']"))
    # note: does not work without c, like b1.findall(u"[@testattr='testvalue']") - should it?
    assert len(result) == 1
    assert result[0] is c2

def test_Element_findall_position():
    py.test.skip('not supported')
    c1 = Element(u'c')
    c2 = Element(u'c')
    text = u"text"
    b1 = Element(u'b', children=(c1, text, c2))
    b2 = Element(u'b')
    a1 = Element(u'a', children=(b1, b2, ))

    result = list(b1.findall(u'c[1]')) # note: index is 1-based, [1] (not [0]) is first
    assert len(result) == 1
    assert result[0] is c1

    result = list(b1.findall(u'c[2]'))
    assert len(result) == 1
    assert result[0] is c2

def test_Element_findtext_default():
    elem = Element(u'a')
    default_text = u'defaulttext'
    result = elem.findtext(u'doesnotexist', default=default_text)
    assert result is default_text

def test_Element_findtext():
    child_text = u"text"
    child = Element(u'b', children=(child_text, ))
    elem = Element(u'a', children=(child, ))
    result = elem.findtext(u'b')
    assert result is child_text

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
    elem = Element(u'a')
    l = list(elem.iter())
    assert len(l) == 1

    elem.append(u'b')
    l = list(elem.iter())
    assert len(l) == 2

    elem.append(Element(u'c'))
    l = list(elem.iter())
    assert len(l) == 3

    elem.append(u'd')
    l = list(elem.iter())
    assert len(l) == 4

def test_Element_itertext():
    elem = Element(u'a')
    l = list(elem.itertext())
    assert len(l) == 0

    elem.append(u'b')
    l = list(elem.itertext())
    assert len(l) == 1

def test_Comment():
    elem = Comment(u'a')
    assert serialize(elem) == u'<!--a-->'
    assert isinstance(elem, Node)

def test_ProcessingInstruction():
    elem = ProcessingInstruction(u'a')
    assert serialize(elem) == u'<?a?>'
    assert isinstance(elem, ProcessingInstruction)

    elem = ProcessingInstruction(u'a', u'b')
    assert serialize(elem) == u'<?a b?>'

def test_QName___init__():
    qname = QName(u'a')
    assert qname.uri is None
    assert qname.name == u'a'
    assert isinstance(qname.name, unicode)
    assert str(qname) == u'a'
    assert qname.text == u'a'

    qname = QName(u'{b}a')
    assert qname.uri == u'b'
    assert isinstance(qname.uri, unicode)
    assert qname.name == u'a'
    assert str(qname) == u'{b}a'
    assert qname.text == u'{b}a'

    qname = QName(u'a', u'b')
    assert qname.uri == u'b'
    assert qname.name == u'a'
    assert str(qname) == u'{b}a'
    assert qname.text == u'{b}a'

    py.test.raises(ValueError, QName, u'{bau')
    py.test.raises(ValueError, QName, u'{b}a', u'c')

def test_QName___cmp__():
    qname1 = QName(u'a')
    qname2 = QName(u'a')

    assert qname1 == qname2
    assert qname1 == u'a'
    assert u'a' == qname1

    qname1 = QName(u'a', u'b')
    qname2 = QName(u'{b}a')

    assert qname1 == qname2
    assert qname1 == u'{b}a'
    assert u'{b}a' == qname1

def test_XMLParser_simple1():
    elem = XML(u'<a />')
    assert elem.tag == u'a'
    assert len(elem) == 0

def test_XMLParser_simple2():
    elem = XML(u'<a><b /></a>')
    assert elem.tag == u'a'
    assert len(elem) == 1
    assert elem[0].tag == u'b'
    assert len(elem[0]) == 0

def test_XMLParser_text1():
    elem = XML(u'<a>b</a>')
    assert elem.tag == u'a'
    assert isinstance(elem, Element)
    assert len(elem) == 1
    assert elem[0] == u'b'
    assert isinstance(elem[0], unicode)

def test_XMLParser_text2():
    elem = XML(u'<a>b<c>d</c>d</a>')
    assert elem.tag == u'a'
    assert len(elem) == 3
    assert elem[0] == u'b'
    assert elem[1].tag == u'c'
    assert elem[2] == u'd'

def test_XMLParser_namespace_1():
    elem = XML(u'<b xmlns="c" d="e"/>')
    assert isinstance(elem.tag, QName)
    assert elem.tag == QName(u'b', u'c')
    assert elem.attrib == {QName(u'd', None): u'e'}
    assert serialize(elem) == u'<ns0:b d="e" xmlns:ns0="c" />'
    assert serialize(elem, namespaces={u'c': u''}) == u'<b d="e" xmlns="c" />'

def test_XMLParser_namespace_2():
    elem = XML(u'<a:b xmlns:a="c" d="e" a:f="g"/>')
    assert isinstance(elem.tag, QName)
    assert elem.tag == QName(u'b', u'c')
    assert elem.attrib == {u'd': u'e', QName(u'f', u'c'): u'g'}
    assert serialize(elem) == u'<ns0:b d="e" ns0:f="g" xmlns:ns0="c" />'
    assert serialize(elem, namespaces={u'c': u''}) == u'<b d="e" f="g" xmlns="c" />'


