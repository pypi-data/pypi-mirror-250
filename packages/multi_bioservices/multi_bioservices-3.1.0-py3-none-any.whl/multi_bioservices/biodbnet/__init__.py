import logging

from multi_bioservices.biodbnet.db2db import db2db
from multi_bioservices.biodbnet.dbFind import dbFind
from multi_bioservices.biodbnet.dbOrtho import dbOrtho
from multi_bioservices.biodbnet.dbReport import dbReport
from multi_bioservices.biodbnet.dbWalk import dbWalk
from multi_bioservices.biodbnet.input_database import InputDatabase
from multi_bioservices.biodbnet.output_database import OutputDatabase
from multi_bioservices.biodbnet.taxon_id import TaxonID

# Catch bioDBnet logging messages
biodbnet_logger = logging.getLogger("bioservices.BioDBNet")
biodbnet_logger.disabled = True
