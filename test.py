import aiotube


# channel = aiotube.Channel('@GYROOO')
# print(channel.metadata)


# video = aiotube.Video('WVDT4lSozHk')
# print(video.metadata)


# playlist = aiotube.Playlist('PL-xXQjd8X_Q-xXQjd8X_Q-xXQjd8X_Q-')
# print(playlist.metadata)


# search = aiotube.Search.video('YouTube Rewind 2018')
# print(search.metadata)









search1 = aiotube.Search.channels('ふたりぱぱ FutariPapa', 2)
print(search1)

for cid in search1:
    try:
        cmd = aiotube.Channel(cid).metadata
        print(cmd)
    except TypeError as e:
        print(f"Could not fetch metadata for channel {cid}: {e}")
    except Exception as e:
        print(f"An error occurred while processing channel {cid}: {e}")


# print(aiotube.Search.Channel('UCTV3Kj71ZW3XfZosaxTFKsw'))
# print(aiotube.Search.Channel('UC-lHJZR3Gqxm24_Vd_AJ5Yw'))
# print(aiotube.Channel('@IanSamirYepManzano'))
# print(aiotube.Channel('UC-lHJZR3Gqxm24_Vd_AJ5Yw'))
# print(aiotube.Channel('UCTV3Kj71ZW3XfZosaxTFKsw'))
# print(aiotube.Channel('UCRuo1L4EcYKQmvlgDzOKUeQ'))
# print(aiotube.Channel('UClhwhJqZmftJBBj3eKvPA7Q'))
# print(aiotube.Channel('UCzH-IRXHeF4jox0P4qBxWAQ').metadata)
# latest_vid = aiotube.Channel('UCzH-IRXHeF4jox0P4qBxWAQ').last_uploaded
latest_vid = aiotube.Channel('UCU69jxPesoWw5I4WmOMBx-Q').last_uploaded

# latest_vid = "R69et-S_ntU"
print(latest_vid)
print(aiotube.Video(latest_vid))
# print(aiotube.Search.channel('Pewdiepie'))
# print(aiotube.Search.channel('Pewdiepie').metadata) 







# search = aiotube.Search.channel('IanSamirYepManzano')
# latest_vid = search.last_uploaded
# print(latest_vid)
# print(aiotube.Video(latest_vid).metadata)





# search = aiotube.Search.playlist('Unlock Your Third Eye')
# print(search.metadata)