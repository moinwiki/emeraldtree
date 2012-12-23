# Copyright (c) 1999-2007 by Fredrik Lundh
#               2008 Bastian Blank <bblank@thinkmo.de>
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.

from __future__ import generators

__all__ = [
    # public symbols
    "Comment",
    "dump",
    "Element", "ElementTree",
    "fromstring", "fromstringlist",
    "iterparse",
    "Node",
    "parse", "ParseError",
    "PI", "ProcessingInstruction",
    "QName",
    "SubElement",
    "tostring", "tostringlist",
    "TreeBuilder",
    "XML",
    "XMLParser", "XMLWriter",
    ]

##
# The <b>Element</b> type is a flexible container object, designed to
# store hierarchical data structures in memory. The type can be
# described as a cross between a list and a dictionary.
# <p>
# Each element has a number of properties associated with it:
# <ul>
# <li>a <i>tag</i>. This is a string identifying what kind of data
# this element represents (the element type, in other words).</li>
# <li>a number of <i>attributes</i>, stored in a Python dictionary.</li>
# <li>a <i>text</i> string.</li>
# <li>an optional <i>tail</i> string.</li>
# <li>a number of <i>child elements</i>, stored in a Python sequence</li>
# </ul>
#
# To create an element instance, use the {@link #Element} constructor
# or the {@link #SubElement} factory function.
# <p>
# The {@link #ElementTree} class can be used to wrap an element
# structure, and convert it from and to XML.
##

import ElementPath

class ParseError(SyntaxError):
    pass

# --------------------------------------------------------------------

class Node(object):
    """
    Node class.
    """

    def write(self, write, encoding=None, namespaces={}, method=None, document=False):
        if not method or method == "xml":
            Writer = XMLWriter
        elif method == "html":
            Writer = HTMLWriter
        elif method == "polyglot":
            Writer = PolyglotWriter
        else:
            Writer = TextWriter

        Writer(encoding, namespaces).write(write, self, document=document)


##
# Element class.  This class defines the Element interface, and
# provides a reference implementation of this interface.
# <p>
# The element name, attribute names, and attribute values can be
# either 8-bit ASCII strings or Unicode strings.
#
# @param tag The element name.
# @param attrib An optional dictionary, containing element attributes.
# @param **extra Additional attributes, given as keyword arguments.
# @see Element
# @see SubElement
# @see Comment
# @see ProcessingInstruction

class Element(Node):
    # <tag attrib>text<child/>...</tag>tail

    ##
    # (Attribute) Element tag.

    tag = None

    ##
    # (Attribute) Element attribute dictionary.  Where possible, use
    # {@link #Element.get},
    # {@link #Element.set},
    # {@link #Element.keys}, and
    # {@link #Element.items} to access
    # element attributes.

    attrib = None

    ##
    # (Attribute) Text before first subelement.  This is either a
    # string or the value None, if there was no text.

    @property
    def text(self):
        if len(self) and isinstance(self[0], basestring):
            return self[0]

    ##
    # (Attribute) Text after this element's end tag, but before the
    # next sibling element's start tag.  This is either a string or
    # the value None, if there was no text.

    @property
    def tail(self):
        raise RuntimeError('The tail argument is not supported')

    def __init__(self, tag, attrib=None, children=(), **extra):
        if attrib:
            if isinstance(attrib, dict):
                attrib = attrib.copy()
            else:
                raise TypeError('attrib')
        else:
            attrib = {}
        attrib.update(extra)
        self.tag = tag
        self.attrib = attrib
        self._children = list(children)

    def __repr__(self):
        return "<Element %s at %x>" % (repr(self.tag), id(self))

    ##
    # Returns the number of subelements.
    #
    # @return The number of subelements.

    def __len__(self):
        return len(self._children)

    def __nonzero__(self):
        return True

    ##
    # Returns the given subelement.
    #
    # @param index What subelement to return.
    # @return The given subelement.
    # @exception IndexError If the given element does not exist.

    def __getitem__(self, index):
        return self._children.__getitem__(index)

    ##
    # Replaces the given subelement.
    #
    # @param index What subelement to replace.
    # @param element The new element value.
    # @exception IndexError If the given element does not exist.
    # @exception AssertionError If element is not a valid object.

    def __setitem__(self, index, element):
        self._children.__setitem__(index, element)

    ##
    # Deletes the given subelement.
    #
    # @param index What subelement to delete.
    # @exception IndexError If the given element does not exist.

    def __delitem__(self, index):
        self._children.__delitem__(index)

    ##
    # Adds a subelement to the end of this element.
    #
    # @param element The element to add.
    # @exception AssertionError If a sequence member is not a valid object.

    def append(self, element):
        self._children.append(element)

    ##
    # Appends subelements from a sequence.
    #
    # @param elements A sequence object with zero or more elements.
    # @exception AssertionError If a subelement is not a valid object.
    # @since 1.3

    def extend(self, elements):
        self._children.extend(elements)

    ##
    # Inserts a subelement at the given position in this element.
    #
    # @param index Where to insert the new subelement.
    # @exception AssertionError If the element is not a valid object.

    def insert(self, index, element):
        self._children.insert(index, element)

    ##
    # Removes a matching subelement.  Unlike the <b>find</b> methods,
    # this method compares elements based on identity, not on tag
    # value or contents.
    #
    # @param element What element to remove.
    # @exception ValueError If a matching element could not be found.
    # @exception AssertionError If the element is not a valid object.

    def remove(self, element):
        self._children.remove(element)

    ##
    # Removes all subelements.

    def remove_all(self):
        self._children = []

    ##
    # Finds the first matching subelement, by tag name or path.
    #
    # @param path What element to look for.
    # @return The first matching element, or None if no element was found.
    # @defreturn Element or None

    def find(self, path):
        return ElementPath.find(self, path)

    ##
    # Finds text for the first matching subelement, by tag name or path.
    #
    # @param path What element to look for.
    # @param default What to return if the element was not found.
    # @return The text content of the first matching element, or the
    #     default value no element was found.  Note that if the element
    #     has is found, but has no text content, this method returns an
    #     empty string.
    # @defreturn string

    def findtext(self, path, default=None):
        return ElementPath.findtext(self, path, default)

    ##
    # Finds all matching subelements, by tag name or path.
    #
    # @param path What element to look for.
    # @return A list or iterator containing all matching elements,
    #    in document order.
    # @defreturn list of Element instances

    def findall(self, path):
        return ElementPath.findall(self, path)

    ##
    # Resets an element.  This function removes all subelements, clears
    # all attributes, and sets the text and tail attributes to None.

    def clear(self):
        self.attrib.clear()
        self.remove_all()

    ##
    # Gets an element attribute.
    #
    # @param key What attribute to look for.
    # @param default What to return if the attribute was not found.
    # @return The attribute value, or the default value, if the
    #     attribute was not found.

    def get(self, key, default=None):
        return self.attrib.get(key, default)

    ##
    # Sets an element attribute.
    #
    # @param key What attribute to set.
    # @param value The attribute value.

    def set(self, key, value):
        self.attrib[key] = value

    ##
    # Gets a list of attribute names.  The names are returned in an
    # arbitrary order (just like for an ordinary Python dictionary).
    #
    # @return A list of element attribute names.
    # @defreturn list of strings

    def keys(self):
        return self.attrib.keys()

    ##
    # Gets element attributes, as a sequence.  The attributes are
    # returned in an arbitrary order.
    #
    # @return A list of (name, value) tuples for all attributes.
    # @defreturn list of (string, string) tuples

    def items(self):
        return self.attrib.items()

    def __iter__(self):
        """
        Creates a element iterator.  The iterator loops over all children.
        """
        return self._children.__iter__()

    ##
    # Creates a tree iterator.  The iterator loops over this element
    # and all subelements, in document order, and returns all elements
    # with a matching tag.
    # <p>
    # If the tree structure is modified during iteration, new or removed
    # elements may or may not be included.  To get a stable set, use the
    # list() function on the iterator, and loop over the resulting list.
    #
    # @param tag What tags to look for (default is to return all elements).
    # @return An iterator containing all the matching elements.
    # @defreturn iterator

    def iter(self, tag=None):
        if tag == "*":
            tag = None
        if tag is None or self.tag == tag:
            yield self
        for e in self._children:
            if isinstance(e, Element):
                for e in e.iter(tag):
                    yield e
            else:
                yield e

    ##
    # Creates a text iterator.  The iterator loops over this element
    # and all subelements, in document order, and returns all inner
    # text.
    #
    # @return An iterator containing all inner text.
    # @defreturn iterator

    def itertext(self):
        for e in self:
            if isinstance(e, Element):
                for s in e.itertext():
                    yield s
            elif isinstance(e, basestring):
                yield e

    def iter_elements(self):
        """
        Creates an interator over all direct element children.
        """
        for child in self._children:
            if child.__class__ is Element:
                yield child

    def iter_elements_tree(self):
        """
        Creates an interator over all elements in document order.
        """
        work = [(self ,)]
        while work:
            cur = work.pop()
            for i in cur:
                yield i
                work.append(i.iter_elements())


##
# Subelement factory.  This function creates an element instance, and
# appends it to an existing element.
# <p>
# The element name, attribute names, and attribute values can be
# either 8-bit ASCII strings or Unicode strings.
#
# @param parent The parent element.
# @param tag The subelement name.
# @param attrib An optional dictionary, containing element attributes.
# @param **extra Additional attributes, given as keyword arguments.
# @return An element instance.
# @defreturn Element

def SubElement(parent, tag, attrib=None, **extra):
    attrib = attrib and attrib.copy() or {}
    attrib.update(extra)
    element = parent.makeelement(tag, attrib)
    parent.append(element)
    return element

##
# Comment element factory.  This factory function creates a special
# element that will be serialized as an XML comment by the standard
# serializer.
# <p>
# The comment string can be either an 8-bit ASCII string or a Unicode
# string.
#
# @param text A string containing the comment string.
# @return An element instance, representing a comment.
# @defreturn Element

class Comment(Node):
    def __init__(self, text = None):
        self.text = text

##
# PI element factory.  This factory function creates a special element
# that will be serialized as an XML processing instruction by the standard
# serializer.
#
# @param target A string containing the PI target.
# @param text A string containing the PI contents, if any.
# @return An element instance, representing a PI.
# @defreturn Element

class ProcessingInstruction(Node):
    def __init__(self, target, text = None):
        self.target, self.text = target, text

PI = ProcessingInstruction

class QName(unicode):
    """
    QName wrapper.  This can be used to wrap a QName attribute value, in
    order to get proper namespace handling on output.

    @ivar name: local part of the QName
    @type name: unicode
    @ivar uri: URI part of the QName
    @type uri: unicode
    """
    __slots__ = 'name', 'uri'

    def __new__(cls, name, uri=None):
        text = name = unicode(name)

        if name[0] == '{':
            if uri is not None:
                raise ValueError
            i = name.find('}')
            if i == -1:
                raise ValueError
            uri = name[1:i]
            name = name[i + 1:]

        if uri is not None:
            uri = unicode(uri)
            text = '{' + uri + '}' + name

        ret = unicode.__new__(cls, text)
        unicode.__setattr__(ret, 'name', name)
        unicode.__setattr__(ret, 'uri', uri)

        return ret

    def __getnewargs__(self):
        return self.name, self.uri

    def __getstate__(self):
        pass

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.name, self.uri)

    def __setattr__(self, key, value):
        raise AttributeError('read-only')
    __delattr__ = __setattr__

# --------------------------------------------------------------------

##
# ElementTree wrapper class.  This class represents an entire element
# hierarchy, and adds some extra support for serialization to and from
# standard XML.
#
# @param element Optional root element.
# @keyparam file Optional file handle or file name.  If given, the
#     tree is initialized with the contents of this XML file.

class ElementTree(object):

    def __init__(self, element=None, file=None):
        assert element is None or isinstance(element, Node)
        self._root = element # first node
        if file:
            self.parse(file)

    ##
    # Gets the root element for this tree.
    #
    # @return An element instance.
    # @defreturn Element

    def getroot(self):
        return self._root

    ##
    # Loads an external XML document into this element tree.
    #
    # @param source A file name or file object.
    # @keyparam parser An optional parser instance.  If not given, the
    #     standard {@link XMLParser} parser is used.
    # @return The document root element.
    # @defreturn Element

    def parse(self, source, parser=None):
        if not hasattr(source, "read"):
            source = open(source, "rb")
        if not parser:
            parser = XMLParser(target=TreeBuilder())
        while 1:
            data = source.read(32768)
            if not data:
                break
            parser.feed(data)
        self._root = parser.close()
        return self._root

    ##
    # Creates a tree iterator for the root element.  The iterator loops
    # over all elements in this tree, in document order.
    #
    # @param tag What tags to look for (default is to return all elements)
    # @return An iterator.
    # @defreturn iterator

    def iter(self, tag=None):
        assert self._root is not None
        return self._root.iter(tag)

    getiterator = iter

    ##
    # Finds the first toplevel element with given tag.
    # Same as getroot().find(path).
    #
    # @param path What element to look for.
    # @return The first matching element, or None if no element was found.
    # @defreturn Element or None

    def find(self, path):
        assert self._root is not None
        if path[:1] == "/":
            path = "." + path
            import warnings
            warnings.warn(
                "This search is broken in 1.3 and earlier; if you rely "
                "on the current behaviour, change it to %r" % path,
                FutureWarning
                )
        return self._root.find(path)

    ##
    # Finds the element text for the first toplevel element with given
    # tag.  Same as getroot().findtext(path).
    #
    # @param path What toplevel element to look for.
    # @param default What to return if the element was not found.
    # @return The text content of the first matching element, or the
    #     default value no element was found.  Note that if the element
    #     has is found, but has no text content, this method returns an
    #     empty string.
    # @defreturn string

    def findtext(self, path, default=None):
        assert self._root is not None
        if path[:1] == "/":
            path = "." + path
            import warnings
            warnings.warn(
                "This search is broken in 1.3 and earlier; if you rely "
                "on the current behaviour, change it to %r" % path,
                FutureWarning
                )
        return self._root.findtext(path, default)

    ##
    # Finds all toplevel elements with the given tag.
    # Same as getroot().findall(path).
    #
    # @param path What element to look for.
    # @return A list or iterator containing all matching elements,
    #    in document order.
    # @defreturn list of Element instances

    def findall(self, path):
        assert self._root is not None
        if path[:1] == "/":
            path = "." + path
            import warnings
            warnings.warn(
                "This search is broken in 1.3 and earlier; if you rely "
                "on the current behaviour, change it to %r" % path,
                FutureWarning
                )
        return self._root.findall(path)

    ##
    # Writes the element tree to a file, as XML.
    #
    # @param file A file name, or a file object opened for writing.
    # @keyparam encoding Optional output encoding (default is US-ASCII).
    # @keyparam method Optional output method ("xml" or "html"; default
    #     is "xml".
    # @keyparam xml_declaration Controls if an XML declaration should
    #     be added to the file.  Use False for never, True for always,
    #     None for only if not US-ASCII or UTF-8.  None is default.

    def write(self, file,
              # keyword arguments
              encoding="us-ascii",
              xml_declaration=None,
              default_namespace=None,
              method=None,
              namespaces={}):
        assert self._root is not None
        if not hasattr(file, "write"):
            file = open(file, "wb")
        write = file.write
        if not encoding:
            encoding = "us-ascii"

        if default_namespace:
            namespaces = namespaces.copy()
            namespaces[default_namespace] = ''

        self._root.write(write, encoding=encoding, namespaces=namespaces, method=method, document=True)

# --------------------------------------------------------------------
# serialization support

# --------------------------------------------------------------------

##
# Generates a string representation of an XML element, including all
# subelements.
#
# @param element An Element instance.
# @return An encoded string containing the XML data.
# @defreturn string

def tostring(element, encoding=None, method=None):
    data = tostringlist(element, encoding, method)
    return "".join(data)

##
# Generates a string representation of an XML element, including all
# subelements.  The string is returned as a sequence of string fragments.
#
# @param element An Element instance.
# @return A sequence object containing the XML data.
# @defreturn sequence
# @since 1.3

def tostringlist(element, encoding=None, method=None):
    class dummy(object):
        pass
    data = []
    file = dummy()
    file.write = data.append
    ElementTree(element).write(file, encoding, method=method)
    # FIXME: merge small fragments into larger parts
    return data

##
# Writes an element tree or element structure to sys.stdout.  This
# function should be used for debugging only.
# <p>
# The exact output format is implementation dependent.  In this
# version, it's written as an ordinary XML file.
#
# @param elem An element tree or an individual element.

def dump(elem):
    # debugging
    import sys
    if not isinstance(elem, ElementTree):
        elem = ElementTree(elem)
    elem.write(sys.stdout)
    tail = elem.getroot().tail
    if not tail or tail[-1] != "\n":
        sys.stdout.write("\n")

# --------------------------------------------------------------------
# parsing

##
# Parses an XML document into an element tree.
#
# @param source A filename or file object containing XML data.
# @param parser An optional parser instance.  If not given, the
#     standard {@link XMLParser} parser is used.
# @return An ElementTree instance

def parse(source, parser=None):
    tree = ElementTree()
    tree.parse(source, parser)
    return tree

##
# Parses an XML document into an element tree incrementally, and reports
# what's going on to the user.
#
# @param source A filename or file object containing XML data.
# @param events A list of events to report back.  If omitted, only "end"
#     events are reported.
# @param parser An optional parser instance.  If not given, the
#     standard {@link XMLParser} parser is used.
# @return A (event, elem) iterator.

def iterparse(source, events=None, parser=None):
    if not hasattr(source, "read"):
        source = open(source, "rb")
    if not parser:
        parser = XMLParser(target=TreeBuilder())
    return _IterParseIterator(source, events, parser)

class _IterParseIterator(object):

    def __init__(self, source, events, parser):
        self._file = source
        self._events = []
        self._index = 0
        self.root = self._root = None
        self._parser = parser
        # wire up the parser for event reporting
        parser = self._parser._parser
        append = self._events.append
        if events is None:
            events = ["end"]
        for event in events:
            if event == "start":
                try:
                    parser.ordered_attributes = 1
                    parser.specified_attributes = 1
                    def handler(tag, attrib_in, event=event, append=append,
                                start=self._parser._start_list):
                        append((event, start(tag, attrib_in)))
                    parser.StartElementHandler = handler
                except AttributeError:
                    def handler(tag, attrib_in, event=event, append=append,
                                start=self._parser._start):
                        append((event, start(tag, attrib_in)))
                    parser.StartElementHandler = handler
            elif event == "end":
                def handler(tag, event=event, append=append,
                            end=self._parser._end):
                    append((event, end(tag)))
                parser.EndElementHandler = handler
            elif event == "start-ns":
                def handler(prefix, uri, event=event, append=append):
                    try:
                        uri = uri.encode("ascii")
                    except UnicodeError:
                        pass
                    append((event, (prefix or "", uri)))
                parser.StartNamespaceDeclHandler = handler
            elif event == "end-ns":
                def handler(prefix, event=event, append=append):
                    append((event, None))
                parser.EndNamespaceDeclHandler = handler

    def next(self):
        while 1:
            try:
                item = self._events[self._index]
            except IndexError:
                if self._parser is None:
                    self.root = self._root
                    raise StopIteration
                # load event buffer
                del self._events[:]
                self._index = 0
                data = self._file.read(16384)
                if data:
                    self._parser.feed(data)
                else:
                    self._root = self._parser.close()
                    self._parser = None
            else:
                self._index += 1
                return item

    def __iter__(self):
        return self

##
# Parses an XML document from a string constant.  This function can
# be used to embed "XML literals" in Python code.
#
# @param source A string containing XML data.
# @param parser An optional parser instance.  If not given, the
#     standard {@link XMLParser} parser is used.
# @return An Element instance.
# @defreturn Element

def XML(text, parser=None):
    if not parser:
        parser = XMLParser(target=TreeBuilder())
    parser.feed(text)
    return parser.close()

##
# Parses an XML document from a string constant, and also returns
# a dictionary which maps from element id:s to elements.
#
# @param source A string containing XML data.
# @param parser An optional parser instance.  If not given, the
#     standard {@link XMLParser} parser is used.
# @return A tuple containing an Element instance and a dictionary.
# @defreturn (Element, dictionary)

def XMLID(text, parser=None):
    if not parser:
        parser = XMLParser(target=TreeBuilder())
    parser.feed(text)
    tree = parser.close()
    ids = {}
    for elem in tree.getiterator():
        id = elem.get("id")
        if id:
            ids[id] = elem
    return tree, ids

##
# Parses an XML document from a string constant.  Same as {@link #XML}.
#
# @def fromstring(text)
# @param source A string containing XML data.
# @return An Element instance.
# @defreturn Element

fromstring = XML

##
# Parses an XML document from a sequence of string fragments.
#
# @param sequence A list or other sequence containing XML data fragments.
# @param parser An optional parser instance.  If not given, the
#     standard {@link XMLParser} parser is used.
# @return An Element instance.
# @defreturn Element
# @since 1.3

def fromstringlist(sequence, parser=None):
    if not parser:
        parser = XMLParser(target=TreeBuilder())
    for text in sequence:
        parser.feed(text)
    return parser.close()

# --------------------------------------------------------------------

##
# Generic element structure builder.  This builder converts a sequence
# of {@link #TreeBuilder.start}, {@link #TreeBuilder.data}, and {@link
# #TreeBuilder.end} method calls to a well-formed element structure.
# <p>
# You can use this class to build an element structure using a custom XML
# parser, or a parser for some other XML-like format.
#
# @param element_factory Optional element factory.  This factory
#    is called to create new Element instances, as necessary.

class TreeBuilder(object):

    def __init__(self, element_factory=None):
        self._data = [] # data collector
        self._elem = [] # element stack
        self._last = None # last element
        if element_factory is None:
            element_factory = Element
        self._factory = element_factory

    ##
    # Flushes the builder buffers, and returns the toplevel document
    # element.
    #
    # @return An Element instance.
    # @defreturn Element

    def close(self):
        assert len(self._elem) == 0, "missing end tags"
        assert self._last is not None, "missing toplevel element"
        return self._last

    def _flush(self):
        if self._data:
            text = "".join(self._data)
            self._elem[-1].append(text)
            self._data = []

    ##
    # Adds text to the current element.
    #
    # @param data A string.  This should be either an 8-bit string
    #    containing ASCII text, or a Unicode string.

    def data(self, data):
        self._data.append(data)

    ##
    # Opens a new element.
    #
    # @param tag The element name.
    # @param attrib A dictionary containing element attributes.
    # @return The opened element.
    # @defreturn Element

    def start(self, tag, attrs):
        self._flush()
        self._last = elem = self._factory(tag, attrs)
        if self._elem:
            self._elem[-1].append(elem)
        self._elem.append(elem)
        return elem

    ##
    # Closes the current element.
    #
    # @param tag The element name.
    # @return The closed element.
    # @defreturn Element

    def end(self, tag):
        self._flush()
        self._last = self._elem.pop()
        assert self._last.tag == tag,\
               "end tag mismatch (expected %s, got %s)" % (
                   self._last.tag, tag)
        return self._last

##
# Element structure builder for XML source data, based on the
# <b>expat</b> parser.
#
# @keyparam target Target object.  If omitted, the builder uses an
#     instance of the standard {@link #TreeBuilder} class.
# @keyparam html Predefine HTML entities.  This flag is not supported
#     by the current implementation.
# @keyparam encoding Optional encoding.  If given, the value overrides
#     the encoding specified in the XML file.
# @see #ElementTree
# @see #TreeBuilder

class XMLParser(object):

    def __init__(self, html=0, target=None, encoding=None):
        try:
            from xml.parsers import expat
        except ImportError:
            raise ImportError(
                "No module named expat; use SimpleXMLTreeBuilder instead"
                )
        parser = expat.ParserCreate(encoding, "}")
        if target is None:
            target = TreeBuilder()
        # underscored names are provided for compatibility only
        self.parser = self._parser = parser
        self.target = self._target = target
        self._error = expat.error
        self._names = {} # name memo cache
        # callbacks
        parser.DefaultHandlerExpand = self._default
        parser.StartElementHandler = self._start
        parser.EndElementHandler = self._end
        parser.CharacterDataHandler = self._data
        # let expat do the buffering, if supported
        try:
            self._parser.buffer_text = 1
        except AttributeError:
            pass
        # use new-style attribute handling, if supported
        try:
            self._parser.ordered_attributes = 1
            self._parser.specified_attributes = 1
            parser.StartElementHandler = self._start_list
        except AttributeError:
            pass
        self._doctype = None
        self.entity = {}
        try:
            self.version = "Expat %d.%d.%d" % expat.version_info
        except AttributeError:
            pass # unknown

    def _raiseerror(self, value):
        err = ParseError(value)
        err.code = value.code
        err.position = value.lineno, value.offset
        raise err

    def _fixname(self, key):
        # expand qname, and convert name string to ascii, if possible
        if key in self._names:
            return self._names[key]
        if '}' in key:
            uri, name = key.split('}', 1)
            name = QName(name, uri)
        else:
            name = QName(key)
        self._names[key] = name
        return name

    def _start(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = {}
        for key, value in attrib_in.items():
            attrib[fixname(key)] = value
        return self.target.start(tag, attrib)

    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = {}
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[fixname(attrib_in[i])] = attrib_in[i+1]
        return self.target.start(tag, attrib)

    def _data(self, text):
        return self.target.data(text)

    def _end(self, tag):
        return self.target.end(self._fixname(tag))

    def _default(self, text):
        prefix = text[:1]
        if prefix == "&":
            # deal with undefined entities
            try:
                self.target.data(self.entity[text[1:-1]])
            except KeyError:
                from xml.parsers import expat
                err = expat.error(
                    "undefined entity %s: line %d, column %d" %
                    (text, self._parser.ErrorLineNumber,
                    self._parser.ErrorColumnNumber)
                    )
                err.code = 11 # XML_ERROR_UNDEFINED_ENTITY
                err.lineno = self._parser.ErrorLineNumber
                err.offset = self._parser.ErrorColumnNumber
                raise err
        elif prefix == "<" and text[:9] == "<!DOCTYPE":
            self._doctype = [] # inside a doctype declaration
        elif self._doctype is not None:
            # parse doctype contents
            if prefix == ">":
                self._doctype = None
                return
            text = text.strip()
            if not text:
                return
            self._doctype.append(text)
            n = len(self._doctype)
            if n > 2:
                type = self._doctype[1]
                if type == "PUBLIC" and n == 4:
                    name, type, pubid, system = self._doctype
                elif type == "SYSTEM" and n == 3:
                    name, type, system = self._doctype
                    pubid = None
                else:
                    return
                if pubid:
                    pubid = pubid[1:-1]
                if hasattr(self.target, "doctype"):
                    self.target.doctype(name, pubid, system[1:-1])
                self._doctype = None

    ##
    # Feeds data to the parser.
    #
    # @param data Encoded data.

    def feed(self, data):
        try:
            self._parser.Parse(data, 0)
        except self._error, v:
            self._raiseerror(v)

    ##
    # Finishes feeding data to the parser.
    #
    # @return An element structure.
    # @defreturn Element

    def close(self):
        try:
            self._parser.Parse("", 1) # end of data
        except self._error, v:
            self._raiseerror(v)
        tree = self.target.close()
        del self.target, self._parser # get rid of circular references
        return tree

class BaseWriter(object):
    def __init__(self, encoding=None, namespaces={}):
        self.encoding = encoding
        self.namespaces = namespaces

    def _escape_cdata(self, text):
        # escape character data
        # it's worth avoiding do-nothing calls for strings that are
        # shorter than 500 character, or so.  assume that's, by far,
        # the most common case in most applications.
        if "&" in text:
            text = text.replace("&", "&amp;")
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        return text

    def _escape_attrib(self, text):
        # escape attribute value
        if "\"" in text:
            text = text.replace("\"", "&quot;")
        if "\n" in text:
            text = text.replace("\n", "&#10;")
        return self._escape_cdata(text)

    def _namespaces(self, elem):
        # identify namespaces used in this tree

        # maps qnames to *encoded* prefix:local names
        qnames = {None: None}

        # maps uri:s to prefixes
        candidate_namespaces = self._namespace_map.copy()
        candidate_namespaces = {}
        candidate_namespaces.update(self.namespaces)
        used_namespaces = {}

        def add_qname(qname):
            if qname in qnames:
                return

            # calculate serialized qname representation
            try:
                if qname.uri is not None:
                    uri = qname.uri
                    prefix = used_namespaces.get(uri, None)
                    if prefix is None:
                        prefix = candidate_namespaces.get(uri, None)
                        if prefix is None:
                            prefix = "ns%d" % len(used_namespaces)
                        if prefix != "xml":
                            used_namespaces[uri] = prefix
                    if prefix:
                        qnames[qname] = "%s:%s" % (prefix, qname.name)
                    else:
                        qnames[qname] = qname.name
                else:
                    # XXX: What happens with undefined namespace?
                    qnames[qname] = qname.name
            except TypeError:
                self._raise_serialization_error(qname)

        # populate qname and namespaces table
        if elem.__class__ is Element:
            for elem in elem.iter_elements_tree():
                tag = elem.tag
                if isinstance(tag, QName):
                    add_qname(tag)
                elif isinstance(tag, basestring):
                    add_qname(QName(tag))
                elif tag is not None:
                    self._raise_serialization_error(tag)

                for key in elem.attrib.iterkeys():
                    if isinstance(key, QName):
                        add_qname(key)
                    elif isinstance(key, basestring):
                        add_qname(QName(key))
                    elif key is not None:
                        self._raise_serialization_error(key)

        return qnames, used_namespaces

    @staticmethod
    def _raise_serialization_error(text):
        raise TypeError(
            "cannot serialize %r (type %s)" % (text, type(text).__name__)
            )

    ##
    # Registers a namespace prefix.  The registry is global, and any
    # existing mapping for either the given prefix or the namespace URI
    # will be removed.
    #
    # @param prefix Namespace prefix.
    # @param uri Namespace uri.  Tags and attributes in this namespace
    #     will be serialized with the given prefix, if at all possible.
    # @raise ValueError If the prefix is reserved, or is otherwise
    #     invalid.

    @classmethod
    def register_namespace(cls, prefix, uri):
        import re
        if re.match("ns\d+$", prefix):
            raise ValueError("Prefix format reserved for internal use")
        for k, v in cls._namespace_map.items():
            if k == uri or v == prefix:
                del cls._namespace_map[k]
        cls._namespace_map[uri] = prefix

    _namespace_map = {
        # "well-known" namespace prefixes
        "http://www.w3.org/XML/1998/namespace": "xml",
        "http://www.w3.org/1999/xhtml": "html",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
        "http://schemas.xmlsoap.org/wsdl/": "wsdl",
        # xml schema
        "http://www.w3.org/2001/XMLSchema": "xs",
        "http://www.w3.org/2001/XMLSchema-instance": "xsi",
        # dublic core
        "http://purl.org/dc/elements/1.1/": "dc",
    }

    def serialize_document_start(self, write):
        pass

    def serialize(self, write, elem, qnames, namespaces={}):
        raise NotImplementedError

    def write(self, write, element, document=False):
        qnames, namespaces = self._namespaces(element)

        if self.encoding:
            def write_encode(text):
                write(text.encode(self.encoding, "xmlcharrefreplace"))
        else:
            write_encode = write

        if document:
            self.serialize_document_start(write_encode)
        self.serialize(write_encode, element, qnames, namespaces)


class TextWriter(BaseWriter):
    def serialize(self, write, elem, qnames=None, namespaces=None):
        for part in elem.itertext():
            write(part)


class MLBaseWriter(BaseWriter):
    """stuff HTML / XML writers have in common"""
    def _attrib_string(self, d, qnames):
        """create a attribute string from a dict d"""
        if not d:
            return u''
        items = d.items()
        items.sort(key=lambda x: x[0])
        result = []
        for k, v in items:
            k = qnames[k]
            if isinstance(v, QName):
                v = qnames[v]
            else:
                v = self._escape_attrib(unicode(v))
            # FIXME: handle boolean attributes for HTML
            result.append(u' %s="%s"' % (k, v))
        return u''.join(result)

    def _namespace_string(self, d):
        """create a namespace string from a dict d"""
        if not d:
            return u''
        items = d.items()
        items.sort(key=lambda x: x[1]) # sort on prefix
        result = []
        for v, k in items:
            if k:
                k = u':' + k
            result.append(u' xmlns%s="%s"' % (k, self._escape_attrib(v)))
        return u''.join(result)

    def _serialize_element(self, write, elem, qnames, namespaces):
        raise NotImplementedError

    def _serialize_comment(self, write, elem):
        write(u"<!--%s-->" % self._escape_cdata(elem.text))

    def _serialize_pi(self, write, elem):
        text = self._escape_cdata(elem.target)
        if elem.text is not None:
            text += ' ' + self._escape_cdata(elem.text)
        write(u"<?%s?>" % text)

    def _serialize_cdata(self, write, elem):
        write(self._escape_cdata(unicode(elem)))

    def serialize(self, write, elem, qnames, namespaces={}):
        if isinstance(elem, Element):
            self._serialize_element(write, elem, qnames, namespaces)
        elif isinstance(elem, Comment):
            self._serialize_comment(write, elem)
        elif isinstance(elem, ProcessingInstruction):
            self._serialize_pi(write, elem)
        else:
            self._serialize_cdata(write, elem)


class XMLWriter(MLBaseWriter):
    def _serialize_element(self, write, elem, qnames, namespaces):
        tag = qnames[elem.tag]

        if tag is not None:
            attrib_str = self._attrib_string(elem.attrib, qnames)
            namespace_str = self._namespace_string(namespaces)
            if len(elem):
                write(u"<%s%s%s>" % (tag, attrib_str, namespace_str))
                for e in elem:
                    self.serialize(write, e, qnames)
                write(u"</%s>" % tag)
            else:
                write(u"<%s%s%s />" % (tag, attrib_str, namespace_str))

        else:
            for e in elem:
                self.serialize(write, e, qnames)

    def serialize_document_start(self, write):
        if self.encoding and self.encoding not in ("utf-8", "us-ascii"):
            write(u"<?xml version='1.0' encoding='%s'?>\n" % self.encoding)


class HTMLWriter(MLBaseWriter):
    empty_elements = frozenset(("area", "base", "basefont", "br", "col", "frame", "hr",
                                "img", "input", "isindex", "link", "meta" "param"))

    def __init__(self, encoding=None, namespaces={}):
        namespaces["http://www.w3.org/1999/xhtml"] = ''
        super(HTMLWriter, self).__init__(encoding, namespaces)

    def _serialize_element(self, write, elem, qnames, namespaces):
        tag = qnames[elem.tag]

        if tag is not None:
            attrib_str = self._attrib_string(elem.attrib, qnames)
            namespace_str = self._namespace_string(namespaces)
            write(u"<%s%s%s>" % (tag, attrib_str, namespace_str))
            if tag.lower() in ('script', 'style'):
                write(u''.join(elem.itertext()))
            else:
                for e in elem:
                    self.serialize(write, e, qnames)
            if tag not in self.empty_elements:
                write(u"</%s>" % tag)

        else:
            for e in elem:
                self.serialize(write, e, qnames)


class PolyglotWriter(MLBaseWriter):
    """write a document that is valid html5 AND well-formed xml,
       see http://www.w3.org/TR/html-polyglot/ """
    void_elements = frozenset(('area', 'base', 'br', 'col', 'command', 'embed', 'hr',
                               'img', 'input', 'keygen', 'link', 'meta', 'param',
                               'source', 'track', 'wbr'))

    def __init__(self, encoding=None, namespaces={}):
        namespaces["http://www.w3.org/1999/xhtml"] = ''
        super(PolyglotWriter, self).__init__(encoding, namespaces)

    def _serialize_element(self, write, elem, qnames, namespaces):
        tag = qnames[elem.tag]

        if tag is not None:
            attrib_str = self._attrib_string(elem.attrib, qnames)
            namespace_str = self._namespace_string(namespaces)
            if len(elem):
                write(u"<%s%s%s>" % (tag, attrib_str, namespace_str))
                for e in elem:
                    self.serialize(write, e, qnames)
                write(u"</%s>" % tag)
            elif tag in self.void_elements:
                write(u"<%s%s%s />" % (tag, attrib_str, namespace_str))
            else:
                write(u"<%s%s%s></%s>" % (tag, attrib_str, namespace_str, tag))

        else:
            for e in elem:
                self.serialize(write, e, qnames)

    def serialize_document_start(self, write):
        write(u"<!DOCTYPE html>\n")

