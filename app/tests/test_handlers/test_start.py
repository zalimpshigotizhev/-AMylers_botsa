from unittest.mock import AsyncMock
import pytest

from app.common.handlers import start
from constants.common import (
    WELCOME_MESSAGE_NOT_AUTH,
    AUTHORIZE,
    HELP
)


@pytest.mark.asyncio
async def test_start_handler(mocker):
    message = AsyncMock()
    state = AsyncMock()
    mock_redis = AsyncMock()
    mock_redis.get.return_value = 'mocked_value'
    mocker.patch('aioredis.create_redis_pool', return_value=mock_redis)
    await start(message, state)
    message.answer.assert_called_with(
        WELCOME_MESSAGE_NOT_AUTH,
        reply_markup=[AUTHORIZE, HELP]
    )
