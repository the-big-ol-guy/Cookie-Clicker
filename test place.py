
dad = ["im", "i'm", "i am"]

# the dad bot!!! (credit: Dehan Wiraputra)
if any(word in message.content for word in dad):

    wordvalue = 0
    remove = 0

    message = message.content.lower().split(" ")
    for item in range(len(message)):
        if item != len(message) - 1:
            for word in dad:
                if message[item] == word:
                    message[item] = "Hi"
                    wordvalue = item
                if str(message[item] + " " + message[item + 1]) == word:
                    message[item] = "Hi"
                    message[item + 1] = "fleiahwht"
                    remove += 1
                    wordvalue = item

    for item in range(len(message)):
        if item < wordvalue:
            message[item] = "fleiahwht"
            remove += 1

    print(message)

    try:
        for x in message:
            message.remove("fleiahwht")
    except ValueError:
        pass

    if message[0] == "Hi":
        await message.channel.send(str(" ".join(message)) + ", I'm dad!")
