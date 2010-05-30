#
# The ElementTree toolkit is
#
# Copyright (c) 1999-2007 by Fredrik Lundh
#               2008-2010 Bastian Blank <bblank@thinkmo.de>
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
# --------------------------------------------------------------------

##
# Tools to build element trees from HTML files.
##

import htmlentitydefs
from HTMLParser import HTMLParser as HTMLParserBase

from . import tree


##
# ElementTree builder for HTML source code.  This builder converts an
# HTML document or fragment to an ElementTree.
# <p>
# The parser is relatively picky, and requires balanced tags for most
# elements.  However, elements belonging to the following group are
# automatically closed: P, LI, TR, TH, and TD.  In addition, the
# parser automatically inserts end tags immediately after the start
# tag, and ignores any end tags for the following group: IMG, HR,
# META, and LINK.
#
# @keyparam builder Optional builder object.  If omitted, the parser
#     uses the standard <b>elementtree</b> builder.
# @keyparam encoding Optional character encoding, if known.  If omitted,
#     the parser looks for META tags inside the document.  If no tags
#     are found, the parser defaults to ISO-8859-1.  Note that if your
#     document uses a non-ASCII compatible encoding, you must decode
#     the document before parsing.
#
# @see elementtree.ElementTree

class HTMLParser(HTMLParserBase):
    AUTOCLOSE = "p", "li", "tr", "th", "td", "head", "body"
    IGNOREEND = "img", "hr", "meta", "link", "br", "input", "col"

    namespace = "http://www.w3.org/1999/xhtml"

    def __init__(self, encoding=None, builder=None):
        HTMLParserBase.__init__(self)
        self.__stack = []
        self.__builder = builder or tree.TreeBuilder()
        self.encoding = encoding or "iso-8859-1"

    ##
    # Flushes parser buffers, and return the root element.
    #
    # @return An Element instance.

    def close(self):
        HTMLParserBase.close(self)
        return self.__builder.close()

    ##
    # (Internal) Handles start tags.

    def handle_starttag(self, tag, attrs):
        tag = tree.QName(tag.lower(), self.namespace)
        if tag.name == "meta":
            # look for encoding directives
            http_equiv = content = None
            for k, v in attrs:
                if k == "http-equiv":
                    http_equiv = v.lower()
                elif k == "content":
                    content = v
            if http_equiv == "content-type" and content:
                # use mimetools to parse the http header
                import mimetools, StringIO
                header = mimetools.Message(
                    StringIO.StringIO("%s: %s\n\n" % (http_equiv, content))
                    )
                encoding = header.getparam("charset")
                if encoding:
                    self.encoding = encoding
        if tag.name in self.AUTOCLOSE:
            if self.__stack and self.__stack[-1] == tag:
                self.handle_endtag(tag)
        self.__stack.append(tag)
        attrib = {}
        if attrs:
            for key, value in attrs:
                # Handle short attributes
                if value is None:
                    value = key
                key = tree.QName(key.lower(), self.namespace)
                attrib[key] = value
        self.__builder.start(tag, attrib)
        if tag.name in self.IGNOREEND:
            self.__stack.pop()
            self.__builder.end(tag)

    ##
    # (Internal) Handles end tags.

    def handle_endtag(self, tag):
        if not isinstance(tag, tree.QName):
            tag = tree.QName(tag.lower(), self.namespace)
        if tag.name in self.IGNOREEND:
            return
        lasttag = self.__stack.pop()
        if tag != lasttag and lasttag.name in self.AUTOCLOSE:
            self.handle_endtag(lasttag)
        self.__builder.end(tag)

    ##
    # (Internal) Handles character references.

    def handle_charref(self, char):
        if char[:1] == "x":
            char = int(char[1:], 16)
        else:
            char = int(char)
        if 0 <= char < 128:
            self.__builder.data(chr(char))
        else:
            self.__builder.data(unichr(char))

    ##
    # (Internal) Handles entity references.

    def handle_entityref(self, name):
        entity = htmlentitydefs.entitydefs.get(name)
        if entity:
            if len(entity) == 1:
                entity = ord(entity)
            else:
                entity = int(entity[2:-1])
            if 0 <= entity < 128:
                self.__builder.data(chr(entity))
            else:
                self.__builder.data(unichr(entity))
        else:
            self.unknown_entityref(name)

    ##
    # (Internal) Handles character data.

    def handle_data(self, data):
        if isinstance(data, str):
            # convert to unicode, but only if necessary
            data = unicode(data, self.encoding, "ignore")
        self.__builder.data(data)

    ##
    # (Hook) Handles unknown entity references.  The default action
    # is to ignore unknown entities.

    def unknown_entityref(self, name):
        pass # ignore by default; override if necessary

##
# Parse an HTML document or document fragment.
#
# @param source A filename or file object containing HTML data.
# @param encoding Optional character encoding, if known.  If omitted,
#     the parser looks for META tags inside the document.  If no tags
#     are found, the parser defaults to ISO-8859-1.
# @return An ElementTree instance

def parse(source, encoding=None):
    return ElementTree.parse(source, HTMLTreeBuilder(encoding=encoding))

def HTML(text):
    parser = HTMLParser()
    parser.feed(text)
    return parser.close()

if __name__ == "__main__":
    import sys
    ElementTree.dump(parse(open(sys.argv[1])))
