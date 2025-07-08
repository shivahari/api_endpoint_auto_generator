import pytest
from loguru import logger
from .endpoint_name_generator import NameGenerator
from .endpoint_module_generator import OpenAPISpecParser

@pytest.fixture
def name_generator():
	return NameGenerator(endpoint_url="/cars/{name}",
                      if_query_param=False,
                      path_params=[('name', 'str')],
                      requestbody_type=None)

@pytest.fixture(scope="session")
def parsed_spec():
	p_spec = OpenAPISpecParser("conf/cars_api_openapi_spec.json", logger).parsed_dict
	return p_spec["cars_endpoint"]["CarsEndpoint"]["instance_methods"]