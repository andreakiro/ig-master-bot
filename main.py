from igbot import InstaBot
from settings import username, pw
from sys import argv

def execute_script(InstaBot):
	InstaBot.get_unfollowers()
	#InstaBot.unfollow()
	#InstaBot.follow()
	#InstaBot.remove_followers()

def isheadless():
	if len(argv) > 1:
		if argv[1] == 'head':
			return False
		else:
			raise ValueError("optional arg must be : 'head'")
	return True

if __name__ == '__main__':
	bot = None
	headless = isheadless()
	if headless:
		bot = InstaBot(username, pw, True)
	else:
		bot = InstaBot(username, pw)

	if bot.legal:
		execute_script(bot)
		bot.close_session()