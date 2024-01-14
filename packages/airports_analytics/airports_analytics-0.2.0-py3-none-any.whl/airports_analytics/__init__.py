import pkg_resources


def load_airports_data():
    # Use pkg_resources to access the file content
    try:
        airports_file = pkg_resources.resource_string(__name__, 'airports.txt')
        airports = airports_file.decode('utf-8').splitlines()
    except FileNotFoundError:
        # Handle the case when the file is not found
        airports = []
    return airports


airports = load_airports_data()


def get_station_list():
    return airports
