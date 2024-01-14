#   _____ _____ __  __ _____  _      ______  
#  / ____|_   _|  \/  |  __ \| |    |  ____| 
# | (___   | | | \  / | |__) | |    | |__    
#  \___ \  | | | |\/| |  ___/| |    |  __|   
#  ____) |_| |_| |  | | |    | |____| |____  
# |_____/|_____|_|__|_|_|_   |______|______| 
# |  __ \ \   / /__   __| |  | |/ __ \| \ | |
# | |__) \ \_/ /   | |  | |__| | |  | |  \| |
# |  ___/ \   /    | |  |  __  | |  | | . ` |
# | |      | |     | |  | |  | | |__| | |\  |
# |_|____  |_|     |_| _|_|__|_|\____/|_| \_|
#  / ____|   /\   |  \/  |  ____|            
# | |  __   /  \  | \  / | |__               
# | | |_ | / /\ \ | |\/| |  __|              
# | |__| |/ ____ \| |  | | |____             
#  \_____/_/    \_\_|  |_|______|            
                                                                               
import os,sys,time
import requests,TimePrint
from bs4 import BeautifulSoup
FirstInit = 0

# If you're a developer and just curious what this module is, i left a few messages to explain my code !
# I know that this code can be much shorter but i don't want it so here we are.

class Init:
    
    os.system("cls")
    
    def __init__(self) -> None:
        global FirstInit
        
        if FirstInit != 0:
            Init.menu()
            #Self starting function, it runs when we call Init() only. like a shortcut to the menu function.
        else:
            #Check game version only once
            GameVersion = "1.4"
            FirstInit = 1
            servers(GameVersion)
        
    def menu():
        import os
        
        os.system("cls")
        
        Selections = [1] #It's my selections list, and it will become much longer when I add new games.
        #What does this list do ?;
        # As you can see from the code below, it checks whether the value is written in this list. If it's not, it will break.

        TimePrint.TP(2,"Welcome To The Simple Python Game Module!\nYou can select a game to play:\n")
        TimePrint.P("1) Number Guessing Game\n2 and more Coming soon!")
        selection = int(input("= "))
        if selection not in Selections: #this is the code below
            #and this code can be written by another way like this => "if not any(selection == value for value in Selections):"
            TimePrint.TP(3,"Please enter a value that counts.")
            Init()
        else:
            if selection == 1:
                Init.NumberGuessingGame() # We're redirecting to the game class
            
    class NumberGuessingGame:
        
        def __init__(self) -> None:
            Init.NumberGuessingGame.menu()
            #And using another self starting function for shortcut

        def menu() -> None:
            """
            # Main Menu of The Number Guessing Game
            
            ## Params;
            ### range -> integer & lives -> integer
            
            ## Redirects;
            ### .NumberGuessingGame.start()
            """
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
                    Exit()
            else:
                TimePrint.TP(3,"You can't enter a live value less than 0")
                Init.NumberGuessingGame.menu()

        @staticmethod
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
                    Exit()
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
            Exit()

class servers:
    def __init__(self,GameVersionData) -> None:
        self.server1(GameVersionData)
        
    def server1(self,GameVersionData) -> None:
        try:
            print("Checking for updates...")
            reqServer = requests.get("https://rentry.co/SPG_Version/raw")
            if reqServer.status_code == 200:
                DataFromServer = BeautifulSoup(reqServer.content, 'html.parser')
                DataFromServer = str(DataFromServer)
                if DataFromServer == GameVersionData:
                    Init()
                else:
                    q = int(input(f"WARNING: New Version Available ({DataFromServer}), to install automaticly please enter '1', to contiune without install please enter '0'.\n= "))
                    if q == 1:
                        os.system(f"pip install SimplePythonGame=={DataFromServer}")
                        print("Update Succesful please re-start.")
                        Exit()
                    else:
                        Init()
            else:
                TimePrint.TP(1,"Something went wrong and we couldn't check for the updates... please try again later. you're redirecting to the game in 2 seconds.")
                time.sleep(2)
                Init()
        except ConnectionError:
            TimePrint.TP(1,"Couldn't check for version! please check your internet and try again later. you're redirecting to the game in 2 seconds.")
            time.sleep(2)
            Init()
            
    def server2() -> None: ...
    def server3() -> None: ...
    def server4() -> None: ...
    def server5() -> None: ...
          
        

class Exit:
    def __init__(self) -> None:
        sys.exit()
#EOF#