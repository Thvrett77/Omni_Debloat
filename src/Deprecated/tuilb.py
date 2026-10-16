def print_with_color(color: str,bold: bool):
    codeb =""
    code = ""
    match color:
        case "red":
            code = "\x1b[0;31m"
            codeb = "\x1b[1;31m"
        case "green":
            code = "\x1b[0;32m"
            codeb = "\x1b[1;32m"
        case "blue":
            code = "\x1b[0;34m"
            codeb = "\x1b[1;34m"
        case "aqua":
            code = "\x1b[0;36m"
            codeb = "\x1b[1;36m"
        case "yellow":
            code = "\x1b[0;33m"
            codeb = "\x1b[1;33m"
        case "purple":
            code = "\x1b[0;35m"
            codeb = "\x1b[1;35m"
        case "white":
            code = "\x1b[0;37m"
            codeb = "\x1b[1;37m"
        case _:
            code = ""
            
    if bold == True:

        
        return codeb
    else:
        
        return code
    


def prt(text: str,color: str,bold: bool):
    reset = "\x1b[0m"
    print(print_with_color(color=color,bold=bold)+text+reset)
    



#print_with_color("1hrk","red",bold=True)


def fancy_input(text: str,color: str,bold: bool):
    reset = "\x1b[0m"
    inp = input(print_with_color(color=color,bold=bold)+f"╭── {text} ──╮\n╰➤ "+reset)
    return inp
    
#result = fancy_input("test")
#prt(color="blue",bold=True,text=result)


# example i will make on the real program 

ascii_greet = r"""                           /$$                     /$$       /$$             /$$           /$$       /$$                       /$$                        
                          | $$                    |__/      | $$            | $$          | $$      | $$                      | $$                        
  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$  /$$  /$$$$$$$        /$$$$$$$  /$$$$$$ | $$$$$$$ | $$  /$$$$$$   /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
 |____  $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$       /$$__  $$ /$$__  $$| $$__  $$| $$ /$$__  $$ |____  $$|_  $$_/   /$$__  $$ /$$__  $$
  /$$$$$$$| $$  \ $$| $$  | $$| $$  \__/| $$  \ $$| $$| $$  | $$      | $$  | $$| $$$$$$$$| $$  \ $$| $$| $$  \ $$  /$$$$$$$  | $$    | $$$$$$$$| $$  \__/
 /$$__  $$| $$  | $$| $$  | $$| $$      | $$  | $$| $$| $$  | $$      | $$  | $$| $$_____/| $$  | $$| $$| $$  | $$ /$$__  $$  | $$ /$$| $$_____/| $$      
|  $$$$$$$| $$  | $$|  $$$$$$$| $$      |  $$$$$$/| $$|  $$$$$$$      |  $$$$$$$|  $$$$$$$| $$$$$$$/| $$|  $$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$$| $$      
 \_______/|__/  |__/ \_______/|__/       \______/ |__/ \_______/       \_______/ \_______/|_______/ |__/ \______/  \_______/   \___/   \_______/|__/      
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          """

#print(print_with_color(color="blue",bold=True)+ascii_greet)
#prt(color="blue",bold=True,text=ascii_greet)
