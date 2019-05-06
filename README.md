# Car-Part-Logging-System
An inventory management system to manage car parts

Provided functionalities include:
* Add a new part
* Remove a part
* Search for a part by ID
* Search for all parts with a specific field value


## Performance 
The information pertaining to all the parts is stored in two dictionaries:
* _parts_by_id_: stores a mapping for part id to part object
* _parts_by_field_: has three keys - 'make', 'model' and 'year' each of which is a mapping of a field value to the list of part ids belonging to that field

As the operation lookup is usually much more frequent for an inventory system than add or remove, choosing the above data structures enables constant time lookups for both searching by id and searching by field value. 