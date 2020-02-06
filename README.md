# Instagram master bot

Enjoy many features to scrap [**Instagram**](https://instagram.com) and discover stats on your account

## Usage

Create a python file named 'settings.py' and insert the following lines:

> username = 'amanda' <br>
> pw = 'dummypassword'

Replace fields with your own username & password. <br>
**Warning**: do not share this file once you entered your credentials!

Open the main directory on a terminal and run the following command: 

> caffeinate python main.py

This is actually a [headless](https://www.built.io/blog/run-selenium-tests-in-headless-browser) WebDriver.
You can also run the following to visualize it:

> caffeinate python main.py head

Above commands will create a new directory in your main one, and store all results text files there. <br>
This may take some time to run (depending on how big is the data to scrape).

### Other functions

Other useful functions exists to follow or unfollow every accounts written down on a text file. <br>
However to use them you need to create following files:

1. Create a directory named 'awaitlist' into your main directory
2. Create a directory named '*your username*' into the *awaitlist* directory
3. Create a text file named 'unfollow.txt' to write down all the person to unfollow
4. Create a text file named 'follow.txt' to write down all the person to follow

Now, go in the execute_script function in the main.py file and uncomment the functions you want to use.

### Have fun :)
