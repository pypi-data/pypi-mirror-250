from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('django-rest').version
except DistributionNotFound:
    pass
