# coding=utf-8
import requests

__author__ = 'Rob Derksen <rob.derksen@hubsec.eu>'
__version__ = '0.1'


class PynoramioException(Exception):
    """ PynoramioException: class used as a custom exception for Pynoramio related errors.
    """
    pass


class Pynoramio:
    def __init__(self):
        self.base_url = 'http://www.panoramio.com/map/get_panoramas?order=popularity'

    def _request(self, lat_min, lon_min, lat_max, lon_max, start, end, picture_size=None, set_=None, map_filter=None):
        """
        Internal method to send requests to the Panoramio data API.

        :param lat_min:
            Minimum latitude of the bounding box
        :type lat_min: float
        :param lon_min:
            Minimum longitude of the bounding box
        :type lon_min: float
        :param lat_max:
            Maximum latitude of the bounding box
        :type lat_max: float
        :param lon_max:
            Maximum longitude of the bounding box
        :type lon_max: float
        :param start:
            Start number of the number of photo's to retrieve, where 0 is the most popular picture
        :type start: int
        :param end:
            Last number of the number of photo's to retrieve, where 0 is the most popular picture
        :type end: int
        :param picture_size:
            This can be: original, medium (*default*), small, thumbnail, square, mini_square
        :type picture_size: basestring
        :param set_:
            This can be: public, popular or user-id; where user-id is the specific id of a user (as integer)
        :type set_: basestring/int
        :param map_filter:
            Whether to return photos that look better together; when True, tries to avoid returning photos of the same
            location
        :type map_filter: bool
        :return: JSON response of the request formatted as a dictionary.
        """
        if not isinstance(lat_min, float):
            raise PynoramioException(
                '{0}._request requires the lat_min parameter to be a float.'.format(self.__class__.__name__))
        if not isinstance(lon_min, float):
            raise PynoramioException(
                '{0}._request requires the lon_min parameter to be a float.'.format(self.__class__.__name__))
        if not isinstance(lat_max, float):
            raise PynoramioException(
                '{0}._request requires the lat_max parameter to be a float.'.format(self.__class__.__name__))
        if not isinstance(lon_max, float):
            raise PynoramioException(
                '{0}._request requires the lon_max parameter to be a float.'.format(self.__class__.__name__))

        if not isinstance(start, int):
            raise PynoramioException(
                '{0}._request requires the start parameter to be an int.'.format(self.__class__.__name__))
        if not isinstance(end, int):
            raise PynoramioException(
                '{0}._request requires the end parameter to be an int.'.format(self.__class__.__name__))

        url = self.base_url + '&minx={0}&miny={1}&maxx={2}&maxy={3}&from={4}&to={5}'.format(lon_min, lat_min,
                                                                                            lon_max, lat_max,
                                                                                            start, end)

        if picture_size is not None and isinstance(picture_size, basestring) \
                and picture_size in ['original', 'medium', 'small', 'thumbnail', 'square', 'mini_square']:
            url += '&size={0}'.format(picture_size)

        if set_ is not None and (isinstance(set_, basestring) and set_ in ['public', 'full']) \
                or (isinstance(set_, int)):
            url += '&set={0}'.format(set_)
        else:
            url += '&set=public'

        if map_filter is not None and isinstance(map_filter, bool) and not map_filter:
            url += '&map_filter=false'

        r = requests.get(url)
        try:
            return r.json()
        except ValueError:
            # add your debugging lines here, for example, print(r.url)
            raise PynoramioException(
                'An invalid or malformed url was passed to {0}._request'.format(self.__class__.__name__))

    def get_from_area(self, lat_min, lon_min, lat_max, lon_max, picture_size=None, set_=None, map_filter=None):
        """
        Get all available photos for a specific bounding box

        :param lat_min:
            Minimum latitude of the bounding box
        :type lat_min: float
        :param lon_min:
            Minimum longitude of the bounding box
        :type lon_min: float
        :param lat_max:
            Maximum latitude of the bounding box
        :type lat_max: float
        :param lon_max:
            Maximum longitude of the bounding box
        :type lon_max: float
        :param picture_size:
            This can be: original, medium (*default*), small, thumbnail, square, mini_square
        :type picture_size: basestring
        :param set_:
            This can be: public, popular or user-id; where user-id is the specific id of a user (as integer)
        :type set_: basestring/int
        :param map_filter:
            Whether to return photos that look better together; when True, tries to avoid returning photos of the same
            location
        :type map_filter: bool
        :return: Returns the full dataset of all available photos
        """
        page_size = 100
        page = 0

        result = self._request(lat_min, lon_min, lat_max, lon_max, page * page_size, (page + 1) * page_size,
                               picture_size, set_, map_filter)

        total_photos = result['count']
        if total_photos < page_size:
            return result

        page += 1

        pages = (total_photos / page_size) + 1
        while page < pages:
            new_result = self._request(lat_min, lon_min, lat_max, lon_max, page * page_size, (page + 1) * page_size,
                                       picture_size, set_, map_filter)

            result['photos'].extend(new_result['photos'])

            page += 1

        return result

    def get_all_pictures_cursor(self, lat_min, lon_min, lat_max, lon_max, picture_size=None, set_=None,
                                map_filter=None):
        """
        Generator to get all available photos for a given bounding box

        :param lat_min:
            Minimum latitude of the bounding box
        :type lat_min: float
        :param lon_min:
            Minimum longitude of the bounding box
        :type lon_min: float
        :param lat_max:
            Maximum latitude of the bounding box
        :type lat_max: float
        :param lon_max:
            Maximum longitude of the bounding box
        :type lon_max: float
        :param picture_size:
            This can be: original, medium (*default*), small, thumbnail, square, mini_square
        :type picture_size: basestring
        :param set_:
            This can be: public, popular or user-id; where user-id is the specific id of a user (as integer)
        :type set_: basestring/int
        :param map_filter:
            Whether to return photos that look better together; when True, tries to avoid returning photos of the same
            location
        :type map_filter: bool
        :return: Yields individual dicts of photos
        """
        page_size = 100
        page = 0

        result = self._request(lat_min, lon_min, lat_max, lon_max, page * page_size, (page + 1) * page_size,
                               picture_size, set_, map_filter)

        total_photos = result['count']

        for photo in result['photos']:
            yield photo

        if total_photos < page_size:
            raise StopIteration()

        page += 1

        pages = (total_photos / page_size) + 1
        while page < pages:
            result = self._request(lat_min, lon_min, lat_max, lon_max, page * page_size, (page + 1) * page_size,
                                   picture_size, set_, map_filter)

            for photo in result['photos']:
                yield photo

            page += 1

        raise StopIteration()

__all__ = ['Pynoramio', 'PynoramioException']