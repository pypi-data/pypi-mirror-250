from bioservices import BioDBNet


class _BioDBNetCache:
    biodbnet: BioDBNet = None
    
    def __init__(self, verbose: bool, cache: bool):
        if _BioDBNetCache.biodbnet is None:
            _BioDBNetCache.biodbnet = BioDBNet(verbose=verbose, cache=cache)
        self.biodbnet = _BioDBNetCache.biodbnet


def get_biodbnet(verbose: bool, cache: bool) -> BioDBNet:
    return _BioDBNetCache(verbose=verbose, cache=cache).biodbnet
