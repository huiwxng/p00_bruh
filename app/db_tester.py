from db import auth, stories

auth.create_table()
stories.create_tables()

registered = auth.register_user("ryan", "ryan")
print(registered)

a = auth.check_creds("ryan", "ryan")
print(a)

b = auth.check_creds("adsfa", "ryan")
print(b)
