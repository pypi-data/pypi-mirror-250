from hotconsole.hotconsole import Command, Hotkey, Runner

command = Command("greet", "Приветствует мир", lambda _: print("Hello, World!"))
hotkey = Hotkey("alt+shift+9", command, None)
Runner().run([hotkey])
