async def voice_binds(message, binds, bot, players, server):
    found = False
    for key in binds:
        if key == message.content:
            found = True
            break
    if not found:
        return
    if players and players[server[0].id].is_playing():
        players[server[0]].stop()
    if bot.is_voice_connected(server[0]):
        voice = bot.voice_client_in(server[0])
        player = voice.create_ffmpeg_player('sounds/' + binds[message.content])
        players[server[0].id] = player
        player.start()
