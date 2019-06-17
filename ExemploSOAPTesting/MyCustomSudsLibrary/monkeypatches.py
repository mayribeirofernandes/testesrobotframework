# Copyright 2012 Kevin Ormbrek
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import xml.dom.minidom
from suds.sax.document import Document


py_version = sys.version_info[0] + sys.version_info[1] * 0.1
if py_version < 3.3:
    class _ElementMonkeyPathes(object):
        # from http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace/

        def fixed_writexml(self, writer, indent="", addindent="", newl=""):
            writer.write(indent + "<" + self.tagName)
            attrs = self._get_attributes()
            a_names = list(attrs.keys())
            a_names.sort()
            for a_name in a_names:
                writer.write(" %s=\"" % a_name)
                xml.dom.minidom._write_data(writer, attrs[a_name].value)
                writer.write("\"")
            if self.childNodes:
                if len(self.childNodes) == 1 \
                        and self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
                    writer.write(">")
                    self.childNodes[0].writexml(writer, "", "", "")
                    writer.write("</%s>%s" % (self.tagName, newl))
                    return
                writer.write(">%s" % newl)
                for node in self.childNodes:
                    node.writexml(writer, indent + addindent, addindent, newl)
                writer.write("%s</%s>%s" % (indent, self.tagName, newl))
            else:
                writer.write("/>%s" % newl)

        xml.dom.minidom.Element.writexml = fixed_writexml


class _DocumentMonkeyPatches(object):
    # fixes AttributeError in debug log event that fails the keyword

    def str(self):
        s = []
        s.append(self.DECL)
        s.append('\n')
        s.append(self.root().str() if self.root() is not None else '<empty>')
        return ''.join(s)

    Document.str = str
