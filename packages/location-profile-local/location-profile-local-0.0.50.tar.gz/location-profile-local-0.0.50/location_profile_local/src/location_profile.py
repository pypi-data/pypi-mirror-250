import sys
import os
from datetime import date
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))

from sdk.src.utilities import is_valid_date_range                       # noqa: E402
from language_local.lang_code import LangCode                           # noqa: E402
from circles_local_database_python.generic_crud import GenericCRUD      # noqa: E402
from dotenv import load_dotenv                                          # noqa: E402

load_dotenv()
from logger_local.Logger import Logger  # noqa: E402
from .constants_location_profile import LocationProfileLocalConstants  # noqa: E402
logger = Logger.create_logger(
    object=LocationProfileLocalConstants.OBJECT_FOR_LOGGER_CODE)


class Location:
    def __init__(self, location_id, profile_id):
        self.profile_id = profile_id
        self.location_id = location_id

    def __dict__(self):
        return {
            'profile_id': self.profile_id,
            'location_id': self.location_id
        }


class LocationProfiles(GenericCRUD):
    def __init__(self):
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME)
        super().__init__(default_schema_name="location_profile")
        logger.end(INIT_METHOD_NAME)

    @staticmethod
    def get_last_location_id_by_profile_id(profile_id: int) -> int:
        GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_location_id_by_profile_id"
        logger.start(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})
        try:
            location_id_tuple_list = LocationProfiles.select_multi_tuple_by_where(LocationProfiles(),
                                                                                  view_table_name="location_profile_view",
                                                                                  select_clause_value="location_id",
                                                                                  where="profile_id = %s",
                                                                                  params=(profile_id,),
                                                                                  limit=1, order_by="start_timestamp desc")
            location_id = location_id_tuple_list[0][0]
        except IndexError:
            logger.warning("No location_id found for profile_id = " + str(profile_id))
            return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None
        else:
            logger.end(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                       object={'location_id': location_id})
            return location_id

    '''
    @staticmethod
    def get_last_location_id_by_profile_id(profile_id: int) -> int:
        GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_location_id_by_profile_id"
        logger.start(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})
        location_id_tuple_list = LocationProfiles.select_multi_tuple_by_where(LocationProfiles(), view_table_name="location_profile_view",
                                                                   select_clause_value="location_id",
                                                                   where="profile_id = %s", params=(profile_id,),
                                                                   limit=1, order_by="start_timestamp desc")
        if len(location_id_tuple_list) == 0:
            logger.warning("No location_id found for profile_id = " + str(profile_id))
            return None
        if len(location_id_tuple_list[0]) == 0:
            logger.warning("No location_id found for profile_id = " + str(profile_id))
            return None
        location_id = location_id_tuple_list[0][0]
        logger.end(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                   object={'location_id': location_id})
        return location_id
     '''

    @staticmethod
    def get_location_ids_by_profile_id(profile_id: int, limit: int = 1, datetime_range: tuple = None) -> list[Location]:
        GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME = "get_location_ids_by_profile_id"
        logger.start(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})

        if datetime_range is None:
            where_clause = f"profile_id = {profile_id}"
        else:
            if is_valid_date_range(datetime_range):
                date1: date = datetime_range[0].strftime('%Y-%m-%d')
                date2: date = datetime_range[1].strftime('%Y-%m-%d')
                where_clause = f"profile_id = {profile_id} AND updated_timestamp BETWEEN " \
                               f"'{date1} 00:00:00' AND '{date2} 23:59:59'"
            else:
                raise ValueError(
                    "Invalid time_range format. It should be 'YYYY-MM-DD'.")

        location_ids = LocationProfiles.select_multi_tuple_by_where(LocationProfiles(),
                                                                    view_table_name="location_profile_view",
                                                                    select_clause_value="location_id", where=where_clause,
                                                                    limit=limit, order_by="updated_timestamp desc")

        location_ids = [Location(
            location_id=location_id, profile_id=profile_id) for location_id in location_ids]
        location_dicts = [loc.__dict__() for loc in location_ids]
        logger.end(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME,
                   object={'location_ids': location_dicts})
        return location_ids

    @staticmethod
    def insert_location_profile(
        profile_id: int,
        location_id: int,
        title: str,
        lang_code: LangCode = LangCode.ENGLISH
    ) -> tuple:
        INSERT_LOCATION_PROFILE_METHOD_NAME = 'insert_location_profile'
        logger.start(INSERT_LOCATION_PROFILE_METHOD_NAME,
                     object={"location_id": location_id})
        data = {
            "profile_id": profile_id,
            "location_id": location_id
        }
        location_profile_id = LocationProfiles.insert(
            LocationProfiles(), table_name="location_profile_table", data_json=data)
        data = {
            "location_profile_id": location_profile_id,
            "lang_code": lang_code.value,
            "title": title,
            "title_approved": False
        }
        location_profile_ml_id = LocationProfiles.insert(
            LocationProfiles(), table_name="location_profile_ml_table", data_json=data)
        logger.end(INSERT_LOCATION_PROFILE_METHOD_NAME)
        return (location_profile_id, location_profile_ml_id)

