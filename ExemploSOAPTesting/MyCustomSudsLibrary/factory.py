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

from suds.sudsobject import Object as SudsObject


class _FactoryKeywords(object):

    def set_wsdl_object_attribute(self, object, name, value):
        """Sets the attribute of a WSDL object.

        Example:
        | ${order search request}=  | Create Wsdl Object      | OrderSearchRequest |      |
        | Set Wsdl Object Attribute | ${order search request} | id                 | 4065 |
        """
        self._assert_is_suds_object(object)
        getattr(object, name)
        setattr(object, name, value)

    def get_wsdl_object_attribute(self, object, name):
        """Gets the attribute of a WSDL object.

        Extendend variable syntax may be used to access attributes; however,
        some WSDL objects may have attribute names that are illegal in Python,
        necessitating this keyword.

        Example:
        | ${sale record}= | Call Soap Method          | getLastSale    |       |
        | ${price}=       | Get Wsdl Object Attribute | ${sale record} | Price |
        """
        self._assert_is_suds_object(object)
        return getattr(object, name)

    def create_wsdl_object(self, type, *name_value_pairs):
        """Creates a WSDL object of the specified `type`.

        Requested `type` must be defined in the WSDL, in an import specified
        by the WSDL, or with `Add Doctor Import`. `type` is case sensitive.

        Example:
        | ${contact}=               | Create Wsdl Object | Contact |              |
        | Set Wsdl Object Attribute | ${contact}         | Name    | Kelly Newman |
        Attribute values can be set by passing the attribute name and value in
        pairs. This is equivalent to the two lines above:
        | ${contact}=               | Create Wsdl Object | Contact | Name         | Kelly Newman |
        """
        if len(name_value_pairs) % 2 != 0:
            raise ValueError("Creating a WSDL object failed. There should be "
                             "an even number of name-value pairs.")
        obj = self._client().factory.create(type)
        for i in range(0, len(name_value_pairs), 2):
            self.set_wsdl_object_attribute(obj, name_value_pairs[i], name_value_pairs[i + 1])
        return obj

    # private

    def _assert_is_suds_object(self, object):
        if not isinstance(object, SudsObject):
            raise ValueError("Object must be a WSDL object (suds.sudsobject.Object).")
