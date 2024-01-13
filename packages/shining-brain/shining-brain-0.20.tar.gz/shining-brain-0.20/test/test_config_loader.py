from shining_brain.config_loader import application_config


def test_config_loader():
    assert application_config["database"]["host"] == '127.0.0.1:3306'
