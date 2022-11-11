from db import auth, stories

auth.create_table()
stories.create_tables()

registered = auth.register_user("ryan", "ryan")
print(registered)

a = auth.check_creds("ryan", "ryan")
print(a)

b = auth.check_creds("adsfa", "ryan")
print(b)

c = stories.create_story("adfaf", "safasdf", 231231)

for i in range(10):
    stories.add_contribution("hi", c, i)

stories.get_all_contributed_stories(1)