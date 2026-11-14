from src import config


def test_project_root_contains_readme():
    assert (config.PROJECT_ROOT / "README.md").exists()


def test_data_directories_exist():
    for path in (config.RAW_DIR, config.INTERIM_DIR, config.PROCESSED_DIR):
        assert path.exists()


def test_seed_is_integer():
    assert isinstance(config.RANDOM_SEED, int)