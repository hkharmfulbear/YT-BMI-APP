import streamlit_authenticator as stauth

import database as db

usernames = ["kumagai", "rmiller"]
names = ["Kumagai Hiroki", "Rebecca Miller"]
passwords = ["kumagai", "def456"]
weight = ["65", "100"]
height=["168", "170"]
hashed_passwords = stauth.Hasher(passwords).generate()


for (username, name, hash_password, weight, height) in zip(usernames, names, hashed_passwords, weight, height):
    db.insert_user(username, name, hash_password, weight, height)