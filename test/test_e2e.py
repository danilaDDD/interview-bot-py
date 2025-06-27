


@pytest.fixture
def bot(test_settings):
    # Create a mocked bot instance
    bot = AsyncMock()
    bot.token = not test_settings.BOT_TOKEN
    return bot


@pytest_asyncio.fixture
async def dispatcher(bot):
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.emit_startup(bot)
    return dp


@pytest.mark.asyncio
async def test_start_command(dispatcher, bot):
    # Create fake message
    message = types.Message(
        message_id=42,
        date=datetime.datetime.now(),
        chat=types.Chat(id=123, type="private"),
        from_user=types.User(id=456, is_bot=False, first_name="Test"),
        entities=[
            types.MessageEntity(
                type="bot_command",
                offset=0,
                length=len("/start")
            )
        ],
        text="/start",
    )
    update = types.Update(update_id=1, message=message)

    # Process the update
    await dispatcher.feed_update(bot, update)

    # Verify response
    bot.send_message.assert_awaited_once()

    # Get arguments from the call
    args, kwargs = bot.send_message.call_args
    assert kwargs['chat_id'] == 123
    assert "Welcome to Interview48 Bot! How can I assist you today?" in kwargs['text']