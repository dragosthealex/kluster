import pytest
from licenta.dao import DAO
from licenta.sql_models import Peer
from mock import patch, MagicMock, sentinel


def test_get_providers():
    # Test no args
    mock_query = MagicMock()
    (mock_query.filter.return_value
     .order_by.return_value.all.return_value) = sentinel.providers
    mock_session = MagicMock()
    mock_session.query.return_value = mock_query

    print(mock_session.query)

    dao_object = DAO()
    dao_object.session_maker = lambda: mock_session

    # Call method we test
    providers = dao_object.get_providers()

    # Expected calls
    mock_session.query.assert_called_once_with(Peer)
    mock_session.query.return_value.filter.assert_called_once()
    (mock_session.query.return_value.filter.return_value.order_by
     .assert_called_once())
    (mock_session.query.return_value.filter.return_value.order_by.return_value
     .all.assert_called_once())
    assert providers is sentinel.providers


def test_register_peer():
    pass


def test_update_status():
    pass


def test_update_rating():
    pass
