from emeraldtree.ElementTree import *

def serialize(elem, **options):
    from cStringIO import StringIO
    file = StringIO()
    tree = ElementTree(elem)
    tree.write(file, **options)
    return file.getvalue()

def test_Element___init__():
    elem = Element('a')
    assert serialize(elem) == '<a />'
    assert isinstance(elem, Node)

def test_Element_append():
    elem = Element('a')
    elem.append(Element('b'))
    assert serialize(elem) == '<a><b /></a>'
    elem.append(Element('c'))
    assert serialize(elem) == '<a><b /><c /></a>'
