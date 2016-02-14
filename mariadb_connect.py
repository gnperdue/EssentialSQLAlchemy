import os

docdir = '/Documents/ProgrammingTokens/MariaDB/'
username_file = os.environ['HOME'] + docdir + 'my_username.txt'
passwd_file = os.environ['HOME'] + docdir + 'my_passwd.txt'
with open(username_file, 'r') as f:
    username = f.readline().strip()
with open(passwd_file, 'r') as f:
    passwd = f.readline().strip()

conn_str = 'mysql+pymysql://' + username + ':' + passwd + \
           '@localhost/essential_alchemy'
