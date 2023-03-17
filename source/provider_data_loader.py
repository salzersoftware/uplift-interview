import os
import json
import logging
from typing import Any

logger = logging.getLogger('source.index')


class ProviderDataLoader:
  def __init__(self):
    self.cached_data: dict[int, Any] = {}
    self.cached_data_values: list[Any] = []

    data_top_level_primitive_fields: dict[str, type] = \
      {"id": type(int), "first_name": str, "last_name": str, "sex": str, "rating": float, "company": str, "active": bool, "country": str, "language": str}

    self.allowed_filterable_fields: dict[str, type] = data_top_level_primitive_fields
    self.allowed_orderable_fields: dict[str, type] = data_top_level_primitive_fields

  def load_data_into_memory(self) -> None:
    # Get the correct absolute path of the file to load
    site_root: str = os.path.realpath(os.path.dirname(__file__))
    json_file_name: str = "data.json"
    json_url: str = os.path.join(site_root, json_file_name)
    
    # Load the file into memory, which is a list of JSON objects
    logger.debug(f"Loading JSON file {json_file_name} from full path {json_url}")
    data_list: Any = json.load(open(json_url))
    logger.debug(f"Loaded {len(data_list)} records from the JSON file")

    # Transform the list of loaded objects, into a localized dict
    # TODO: Could do some validation, around uniqueness of IDs, 
    # what to do if an ID doesn't exist on a loaded object, etc.
    for data_item in data_list:
      id: int = data_item["id"]

      if id not in self.cached_data:
        self.cached_data[id] = data_item

    # Minor performance improvement, since most of the time, access to the data
    # will be only concerned about the list itself.
    self.cached_data_values: list[Any] = list(self.cached_data.values())

    logger.debug(f"Transformed {len(self.cached_data)} records into dictionary. ({self.cached_data.keys()} present in the dictionary)")

  def get_providers(self) -> list[Any]:
    return self.cached_data_values
  
  def get_providers_with_options(
      self,
      filters: dict[str, Any] = None,
      ordering: dict[str, bool] = None
    ) -> list[Any]:
      if filters:
        # Validate filters
        for key in filters.keys():
          if key not in self.allowed_filterable_fields:
            message: str = f"Key {key} is not a filterable field."
            raise ValueError(message)

      if ordering:
        # TODO: Current restriction only allows one ordering property,
        # so consider allowing further ones.
        if len(ordering.keys()) > 1:
          message: str = f"Ordering only by one key is currently supported. {len(ordering.keys())} were specified."
          raise ValueError(message)

        # Validate ordering specification
        for key in ordering.keys():
          if key not in self.allowed_orderable_fields:
            message: str = f"Key {key} is not an orderable field."
            raise ValueError(message)

      result: list[Any] = []

      if filters:
        for provider in self.cached_data_values:
          does_provider_pass_filter: bool = True

          for key, value in filters.items():
            type_to_cast: type = self.allowed_filterable_fields[key]

            if provider.get(key) != self._cast_to_primitive_type(value, type_to_cast):
              does_provider_pass_filter = False
              break
          
          if does_provider_pass_filter:
            result.append(provider)
      else:
        result = self.cached_data_values

      if ordering:
        # TODO: Note, that the current implementation expects, and checks against,
        # only one order by argument being provided.
        key_to_order_on: str = list(ordering.keys())[0]
        sorting_order: bool = True if list(ordering.values())[0] == 1 else False

        result = sorted(result, key=lambda d: d[key_to_order_on], reverse=sorting_order)


      return result

  
  def _cast_to_primitive_type(self, value: str, prim_type: type):
    if prim_type == int:
      return int(value)
    elif prim_type == float:
      return float(value)
    elif prim_type == bool:
      lower_value: str = value.lower()

      if lower_value == 'true':
        return True
      elif lower_value == 'false':
        return False
      else:
        return bool(value)
    elif prim_type == str:
      return str(value)
    else:
      message: str = f"Unknown type: {str(type)}"
      raise ValueError(message)



