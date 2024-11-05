__version__ = "0.0.4"

def get_version():
    return __version__

def print_cool_banner():
    ascii_banner = f"""

                _                          
magasin's      (_)                         
     _ __  _ __ _ _ __ ___   ___ _ __ ___  
    | '_ \| '__| | '_ ` _ \ / _ \ '__/ _ \ 
    | |_) | |  | | | | | | |  __/ | | (_) |
    | .__/|_|  |_|_| |_| |_|\___|_|  \___/ 
    | |                                   Pipeline                                     
    |_|
    Version {__version__}
    https://github.com/unicef/magasin-primero-paquet

    """
    print(ascii_banner)