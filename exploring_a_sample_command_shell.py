import os
from cmd import Cmd

class MyPrompt(Cmd):

  prompt = 'pb> '
  intro = "Welcome! Type ? to list commands"

  def do_exit(self, inp):
    print("Bye")
    return True
    
  def help_exit(self):
    print('exit the application. Shorthand: x q Ctrl-D.')

  def do_add(self, inp):
    print("adding '{}'".format(inp))

    first_num = inp[0]
    second_num = inp[2]

    # verify the first number isn't empty and it is a valid numeric string
    if first_num == '' or not first_num.isnumeric():
      print("Invalid number received: {}".format(first_num))
      return

    # verify the second number isn't empty and it is a valid numeric string
    if second_num == '' or not second_num.isnumeric():
      print("Invalid number received: {}".format(second_num))
      return

    first_num = float(first_num)
    second_num = float(second_num)

    result = first_num + second_num
    print("result is {}".format(result))

  def help_add(self):
    print("Add a new entry to the system.")

  def do_list(self, inp):
    '''List the content for the current directory'''
    # get the target directory from input if the input isn't empty
    target = inp if inp != '' else os.getcwd()

    try:
      for r, d, f in os.walk(target):

        for dir in d:
          # print all sub folders inside the directory
          print(os.path.join(r, dir))

        for file in f:
          # print all files inside the directory
          print(os.path.join(r, file))

    except Exception:
      print("list: no such file or directory: {}".format())

  def help_list(self):
    print("List the content for the current direcotry.")

  def default(self, inp):
    if inp == 'x' or inp == 'q':
      return self.do_exit(inp)

    print("Default: {}".format(inp))

  do_EOF = do_exit
  help_EOF = help_exit
 
if __name__ == '__main__':
    MyPrompt().cmdloop()
