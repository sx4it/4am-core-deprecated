#!/usr/bin/env python

from database import Session
from database.entity import *

firstname = 'erwin'  
lastname = 'erwin'
mail = 'erwin@erwin.com'
password = 'erwin'
key = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA3b6BPEz90IwOHmlC2fm340hxRuWvecDlCw6vpOfc68rtTzjvRt8VhP4GglujscAKiJKcD/7PNwlv1V1wWBju4h3AmaZNzvUeBtracNA6GE1JSNwYo3bK/jsUhJR63WP22vyRmI7hrGfBLlwsJCwvZs6b/EvwJhrd90zF59I5jkF0XMmi2EUucdheJCNGUWjG/c2xxsqhrxheTYN4lRW1nea/XqpyttjuIKGRNwdwvz5p3KObTfsg0WTu6F0g2RcTk2EFXHVqxUjKvkpYRPPMwfpP0h1ST6ccWJXLWabWLXixOMsQxAIjU45YzC/E2nIssK0ETTfEmWtuNnCBd46Dxw== keld@keld-laptop'


user1 = user.User(firstname, lastname, mail, password)
user1.userkey = [userKey.UserKey(key, 'type')]

Session._userRequest.addUser(user1)
