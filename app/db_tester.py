from db import auth, stories

auth.delete_table()
stories.delete_table()

auth.create_table()
stories.create_tables()

auth.register_user("taylorswift", "t@y10r$w1ft")
auth.register_user("shawnmendes", "$h@wnm3nd3$")

taylor_id = auth.get_user_id("taylorswift")
shawn_id = auth.get_user_id("shawnmendes")

love_story_id = stories.create_story("Love Story", "We were both young when I first saw you", taylor_id)
in_my_blood_id = stories.create_story("In My Blood", "Help me, it's like the walls are caving in", shawn_id)

stories.add_contribution("I close my eyes and the flashback starts", love_story_id, shawn_id)

stories.get_contributors(love_story_id)