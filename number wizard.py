# minimum and maximum when starting the game, never changes
qmini = 0
qmaxi = 1000000


# ends program when the player tries guessing a value that they already passed
def cheatdetect():
    global mini, maxi
    if maxi - mini == 1:
        print("\nbruh")
        end()


# asks player if they want to play again, then resets everything
def end():
    global hasWon, mini, maxi, guess, attempts
    if input("\nPlay again? ") == "yes":
        mini = qmini
        maxi = qmaxi
        guess = round((qmaxi + qmini) / 2)
        attempts = 1
        hasWon = False
        return print("")
    else:
        hasWon = True


# sets the game up
hasWon = False
attempts = 1
mini = qmini
maxi = qmaxi
guess = round((qmaxi + qmini) / 2)

print("I am the number wizard! I can guess any integer (eventually)!\nThink of a number between " +
      str(mini) + " and " + str(maxi) + "!\n")

# asks player whether their guess is higher, lower, or equal to the number the player is thinking of,
# then makes a new guess based on the answer
try:
    while hasWon is False:
        answer = input("Is your number higher, lower, or equal to " + str(guess) + "? ")
        if answer == "equal":
            print("\nI guessed it!")
            if attempts == 1:
                print("And it only took " + str(attempts) + " try.")
            else:
                print("And it only took " + str(attempts) + " tries.")
            end()
        elif answer == "higher":
            attempts += 1
            mini = guess
            guess = round((maxi + mini) / 2)
            cheatdetect()
        elif answer == "lower":
            attempts += 1
            maxi = guess
            guess = round((maxi + mini) / 2)
            cheatdetect()
        else:
            print("Not a valid response.")
# gets rid of errors from ending the program without inputting anything
except KeyboardInterrupt:
    print("\n\nEnded too early :(")
