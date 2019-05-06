#!/usr/bin/env python
"""part_logger.py
An inventory management system to manage car parts
Provided functionalities include:
* Add a new part
* Remove a part
* Search for a part by ID
* Search for all parts with a specific field value
"""

__author__ = "Dipesh Singh Reen"


from collections import defaultdict

class Part(object):
      """ Data class to store all Part specific information and methods

      """
      def __init__(self, make: str , model: str , year: str , part_id: int):
            self.make, self.model, self.year, self.part_id = make, model, year, part_id


class Part_Logger(object):
      """ A logging system for car parts with functionalities including:
      1. Add a new part
      2. Remove a part
      3. Search for a part by ID
      4. Search for all parts with a specific field value
      
      To Use:
      >>> logger = Part_Logger()
      >>> logger.add_part(make='<part_make>', model='<part_model>', year='<part_year>')
      1
      >>> logger.remove_part(1)
      Part object at 0x...
      >>> logger.search_by_id(1)
      Part object at 0x... (None if the part doesn't exist)
      >>> logger.search_by_fields(field='make', value='make_1')
      [<all Part objects satisfying the criteria>]
      """

      def __init__(self):
            self.parts_by_field = {
                  'make': defaultdict(list),
                  'model': defaultdict(list),
                  'year': defaultdict(list)
                  }
            self.parts_by_id = defaultdict()


      ######## ADDING A NEW PART ########

      def _get_new_id(self) -> int:
            """ Gets the largest Car Part ID already in the system +1 as the ID for a new part
            
            Returns:
                int -- newly generated ID
            """
            return list(self.parts_by_id)[-1] + 1 if self.parts_by_id else 1

      def _add_to_field_dict(self, part: object):
            """ Adds the new part_id to the corresponding fields of 'parts_by_field' data structure
            
            Arguments:
                part {object} -- object of class Part being added to the log system
            """
            for field, field_dict in self.parts_by_field.items():
                  field_dict[getattr(part,field)].append(part.part_id)

      def _add_to_id_dict(self, part: object):
            """ Adds the new part to the 'parts_by_id' data structure 
            
            Arguments:
                part {object} -- object of class Part being added to the log system
            """
            self.parts_by_id[part.part_id] = part
      
      def add_part(self, make: str, model: str, year: str) -> int:
            """ Handles the following functionalities:
            1. creating part object from the input arguments
            2. Adding of new part to 'parts_by_id' and 'parts_by_field'
            
            Arguments:
                make {str} -- make of the new car part
                model {str} -- model of the new car part
                year {str} -- year of the new car part
            
            Raises:
                TypeError: if the arguments aren't all strings
                ValueError: if any argument is an empty string
                ValueError: if value for the argument 'year' isn't a positive string integer
            
            Returns:
                int -- newly generated ID
            """
            
            if type(make) != str or type(model) != str or type(year) != str:
                  raise TypeError("'make', 'model' and 'year' should be of string type")
            elif make=='' or model=='' or year=='':
                  raise ValueError("Parameter values cannot be empty")
            elif not (year.isdigit()):
                  raise ValueError("'year' should be in the form of string digits")
            
            new_part_id = self._get_new_id()
            new_part = Part(make, model, year, new_part_id)
            self._add_to_field_dict(new_part)
            self._add_to_id_dict(new_part)
            return new_part_id

      
      ######## SEARCH FOR PART(S) ########

      def search_by_field(self, field: str, value: str) -> list:
            """ Returns a list of parts that satisfy the query 
            
            Arguments:
                field {str} -- 'make', 'model' or 'year'
                value {str} -- value of the field for which the parts are to be returned
            
            Raises:
                TypeError: if the arguments aren;t strings
                ValueError: if field isn't 'make', 'model' or 'year'
                ValueError: if value argument is an empty string 
                ValueError: if field is 'year' and value isn't a positive string integer
            
            Returns:
                list -- list of objects (parts) that satisfy the required query 
            """
            
            if type(field) != str or type(value) != str:
                  raise TypeError("'field' and 'value' should be of string type")
            elif not field in ('make', 'model', 'year'):
                  raise ValueError("'field' must be 'make', 'model' or 'year'")
            elif value == '':
                  raise ValueError("'value' parameter cannot be empty")
            elif field == 'year' and not (value.isdigit()):
                  raise ValueError("'year' should be in the form of string digits")

            return [self.parts_by_id.get(part_id) for part_id in self.parts_by_field[field][value]]

      def search_by_id(self, part_id: int) -> object:
            """ Returns a single object with the corresponding part_id if present, else return None
            
            Arguments:
                part_id {int} -- part_id of the part to be returned
            
            Raises:
                TypeError: if part_id isn't an integer
                ValueError: if part_id isn't greater than 0
            
            Returns:
                object -- part (object) with the required part_id
            """
            
            if type(part_id) != int:
                  raise TypeError("'part_id' to search should be of integer type")
            elif part_id <= 0:
                  raise ValueError("'part_id' to search should be a positive integer")
            
            return self.parts_by_id.get(part_id)


      ######## Removing a specific part ########

      def _remove_from_field_dict(self, part: object):
            """ Remove the part_id of the specific part from 'parts_by_field' 
            
            Arguments:
                part {object} -- part object to be removed
            """
            for field, field_dict in self.parts_by_field.items():
                  field_dict[getattr(part,field)].remove(part.part_id)
                  if len(field_dict[getattr(part,field)]) == 0:
                        del field_dict[getattr(part,field)]

      def _remove_from_id_dict(self, part_id: int):
            """[Remove the part_id to part mapping from 'parts_by_id'
            
            Arguments:
                part_id {int} -- part_id of the part to be removed
            """
            del self.parts_by_id[part_id]

      def remove_part(self, part_id: int) -> object:
            """ Remove the specified part from 'parts_by_field' and 'parts_by_id'
            
            Arguments:
                part_id {int} -- part_id of the part to be removed
            
            Raises:
                TypeError: if the argument isn;t an integer
                ValueError: if the argument isn't greater than 0
            
            Returns:
                object -- part that is being removed
            """
            if type(part_id) != int:
                  raise TypeError("'part_id' to remove should be of integer type")
            elif part_id <= 0:
                  raise ValueError("'part_id' to remove should be a positive integer")

            if part_id in self.parts_by_id:
                  part_to_remove = self.parts_by_id[part_id]
                  self._remove_from_field_dict(part_to_remove)
                  self._remove_from_id_dict(part_id)
                  return part_to_remove
            else:
                  return None