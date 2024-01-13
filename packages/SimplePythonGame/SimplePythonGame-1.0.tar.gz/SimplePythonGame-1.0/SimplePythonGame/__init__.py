import os
class TimePrint:
    """
        ### This is a side package of TimePrintOnPyPI module
        ### Author Email: osmntn08@gmail.com
        ### Project GitHub Page: https://github.com/SForces/TimePrint
        ### Project PyPi Page: https://pypi.org/project/TimePrintOnPYPI/
    """
    def TP(seconds: int, text: str) -> str:
        import time
        import sys
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(int(seconds)/len(text))
        print("")
    def P(text:str) -> str:
        import time
        import sys
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.001)
        print("")    

class Init:
    os.system("cls")
    def __init__(self) -> None:
        Init.menu()
        
    def menu():
        import time
        import os
        
        os.system("cls")
        
        Selections = [1]

        TimePrint.TP(2,"Welcome To The Simple Python Game Module!\nYou can select a game to play:\n")
        TimePrint.P("1) Number Guessing Game\n2 and more Coming soon!")
        selection = int(input("= "))
        if not any(selection == value for value in Selections):
            TimePrint.TP(3,"Please enter a value that counts.")
            Init()
        else:
            if selection == 1:
                Init.NumberGuessingGame()
            
    class NumberGuessingGame:
        
        def __init__(self) -> None:
            Init.NumberGuessingGame.menu()
            
        def menu() -> None:
            """
            # Main Menu of The Number Guessing Game
            
            ## Params;
            ### range -> integer & lives -> integer
            
            ## Redirects;
            ### .NumberGuessingGame.start()
            """
            import random
            import time
            import os
            
            print("Please select a number range to play: ",end="")
            rang = int(input("0-"))
            while rang < 1:
                TimePrint.TP(2, "You can't enter a range less than or equal to 0")
                rang = int(input(TimePrint.TP(1,"Please select a number range to play: 0-")))
                
            TimePrint.TP(1,"Please select your lives to guess:")
            lives = int(input(""))
            if not lives < 0:
                os.system("cls")
                TimePrint.TP(1,f"You've selected a game range 0-{rang} and you have {lives} to guess it,\n if its ok press enter to start, if its not enter anything else to exit.")
                question = input()
                if not question:
                    Init.NumberGuessingGame.start(rang,lives)
                else:
                    Init()
            else:
                TimePrint.TP(3,"You can't enter a live value less than 0")
                Init.NumberGuessingGame.menu()

        
        def start(game_range:int ,lives:int) -> None:
            """
                ### Function that starts and plays the game.
            """
            from random import randint
            from os import system
            
            tutulan_sayi = randint(0,game_range)
            system("cls")
            TimePrint.TP(1,f"The Game Is Starting!\n\n» The generated number is between 0 and {game_range}.\n» You have exactly {lives} attempts to guess this number.\n Good luck!")
            live = lives
            for _ in range(live):
                tahmin = int(input("Please guess a number: "))
                if tahmin == tutulan_sayi:
                    TimePrint.TP(1,"Congratulations! You have guessed the number correctly. Please enter an input to exit.")
                    input()
                    Init()
                elif tahmin > tutulan_sayi:
                    live -= 1
                    TimePrint.TP(1,f"You guessed a large number! Try a 'Smaller' number. You have {live} lives remaining.")
                    continue
                elif tahmin < tutulan_sayi:
                    live -= 1
                    TimePrint.TP(1,f"You guessed a small number! Try a 'Larger' number. You have {live} lives remaining.")
                    continue    
            TimePrint.TP(1,f"You have run out of attempts, and you lost. The generated number was {tutulan_sayi}.\nEnter an input to exit.")    
            input()  
            Init()  
                                                      