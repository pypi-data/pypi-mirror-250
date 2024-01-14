from .location_local_constants import LocationLocalConstants
from .point import Point


class LocationsUtil:

    def extract_coordinates_and_replace_by_point(
            data_json: dict,
            point_column_name: str = None) -> dict:

        point_column_name = point_column_name or LocationLocalConstants.DEFAULT_POINT_COLUMN_NAME  # noqa501

        # Extract longitude and latitude values
        longitude = data_json.pop(f'ST_X({point_column_name})', None)
        latitude = data_json.pop(f'ST_Y({point_column_name})', None)

        if longitude is not None and latitude is not None:
            # Create Point object
            point = Point(longitude=longitude, latitude=latitude)

            # Add 'point' key to the dictionary
            data_json['point'] = point

        return data_json

    def location_test_entity_creator(number: int, is_test_data: bool = True):
        '''creates a dummy json for location entity '''
        point = Point(0, 0)
        return {
            'number': number,
            'is_test_data': is_test_data,
            'coordinate': point
        }
