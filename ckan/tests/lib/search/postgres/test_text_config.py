# encoding: utf-8
import pytest
import sqlalchemy as sa

from ckan import model


@pytest.mark.usefixtures("clean_db")
def test_creating_the_table_creates_the_text_search_config():
    """`ckan db init` creates the tables from the models, without running
    the migration that used to create the ``ckan_english`` configuration."""
    with model.ensure_engine().begin() as conn:
        conn.execute(sa.text("DROP TABLE package_search_index"))
        conn.execute(sa.text("DROP TEXT SEARCH CONFIGURATION ckan_english"))
        conn.execute(sa.text("DROP TEXT SEARCH DICTIONARY ckan_english_stem"))

        model.package_search_index_table.create(conn)

        found = conn.execute(sa.text(
            "SELECT count(*) FROM pg_ts_config WHERE cfgname = 'ckan_english'"
        )).scalar()
    assert found == 1
