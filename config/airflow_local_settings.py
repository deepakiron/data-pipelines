from airflow.configuration import conf

# Set the LOAD_EXAMPLES configuration to False
conf.load_test_config()
conf.set("core", "load_examples", "False")
