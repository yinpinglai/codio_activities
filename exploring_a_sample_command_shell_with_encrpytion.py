from cmd import Cmd

import os
import base64
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MyPrompt(Cmd):

  prompt = 'pb> '
  intro = "Welcome! Type ? to list commands"

  def __init__(self) -> None:
    super().__init__()

  def _generate_salt(self):
    salt_file_name = '.salt'
    if not os.path.exists(salt_file_name):
      with open(salt_file_name, 'wb') as salt_file:
        salt_file.write(uuid.uuid4().hex)
    with open(salt_file_name, 'rb') as salt_file:
      return salt_file.read()

  def do_encrypt(self, inp):
    input_password = inp[0]
    input_data = inp[1]
    export_data_file = inp[2]

    password = input_password.encode('utf-8')
    salt = self._generate_salt()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=310000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fernet = Fernet(key)

    try:
      with open(export_data_file, 'rb') as export_file:
        encrypted_data = fernet.encrypt(input_data)
        export_data_file.write(encrypted_data)
      print('Saved to {}'.format(export_data_file))
    except Exception as exception:
      print(exception)

  def help_encrypt(self):
    print('help_encrypt')

  def do_decrypt(self, inp):
    input_password = inp[0]
    encrypted_file_path = inp[1]
  
    password = input_password.encode('utf-8')
    salt = self._generate_salt()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=310000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fernet = Fernet(key)
    try:
      with open(encrypted_file_path, 'rb') as input_file:
        data = input_file.read()
        decrypted_data = fernet.decrypt(data)
        print(str(decrypted_data))
    except Exception as exception:
      print(exception)

  def help_decrypt(self):
    print('help_decrypt')

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
          dir_path = os.path.join(r, dir)
          print(dir_path)

        for file in f:
          # print all files inside the directory
          file_path = os.path.join(r, file)
          print(file_path)

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
