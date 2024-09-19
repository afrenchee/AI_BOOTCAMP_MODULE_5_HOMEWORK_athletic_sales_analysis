import os, sys

windows_is_the_OS = False # This variable is set by the main programmer to ensure that Terminal / Command Prompt commands are correctly executed in clear_screen() and end_program()



def clear_screen():
	if windows_is_the_OS:
		os.system('cls')
	else:
		os.system('clear')



def end_program():
	if windows_is_the_OS:
		os.system('dir')
	else:
		os.system('pwd')
		os.system('ls')
	print("")
	sys.exit()



if __name__ == '__main__':
	clear_screen()