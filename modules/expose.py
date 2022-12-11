def expose():
    target_user = client.get_user(id=tweet.in_reply_to_user_id, user_auth=True)

    user_ID = target_user.data.id
    user_name = target_user.data.username

    print("The tweet is: " + tweet.text)

    user_info = api.get_user(user_id=user_ID)
    user_likes = user_info.favourites_count  # Get total likes of user given

    rand_num = random.randint(0, user_likes)

    message = ".@" + user_name + " es tan follawaifus que le ha dado me gusta a " \
        + str(rand_num) + " monas chinas!"
    print("The answer is: " + message)

    client.create_tweet(
        in_reply_to_tweet_id=tweet.id,
        text=message
    )

    # Save the ID in ids.txt
    f = open("ids.txt", 'a')
    f.write(str(tweet.id) + "\n")
    f.close()

    print("Se ha enviado la respuesta y guardado la ID.\n")

    start_id = tweet.id
