import random
print("                                  Hello, this is a Python program that will choose a number and you have to guess it.")
max_attempts = 5

def play_game():
    best_score = None
    while True:
        secret = random.randint(1, 10)
        attempts = 0

        while True:
            try:
                guess= int(input("Guess a number between 1 and 10 ="))
            except ValueError:
                print("                               Numbers only!!")
                continue
            if guess > 10 or guess < 1:
                print("                       Invalid Range, Enter a number between 1 and 10")
                continue
            attempts += 1 #This variable is created to add a value to attempts so it can be subtracted from max_attempts

            if guess == secret:
                total_attempts= attempts # This variable is created in a loop to show the total attempts
                print("                      You guessed it right in",total_attempts,"attempts")
                if best_score == None or total_attempts < best_score:
                    best_score = total_attempts
                    print("                      The best score is =", best_score)

                #Created a variable to show the best score and assigned it with total attempts
                break
            elif guess > secret:
                print("                         TOO HIGH!")
                x = max_attempts - attempts #This variable is used to subtract the value from attempts and displays them
                print("The attempts left are", x)
            else:
                print("                         TOO LOW!")
                x = max_attempts - attempts
                print("The attempts left are", x)

            if attempts >= max_attempts:
                print("                           You have reached the attempts limit")
                print("                            The secret number was = ",+secret)
                print("                            The best score is 0")
                break
        z = input("Do you want to play again? ")

        if z.upper() == "Yes" or z.lower() == "yes":
            continue
        else:
            break

play_game()




