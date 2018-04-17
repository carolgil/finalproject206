# finalproject
I pulled all my data from Trip Advisor to find the top three activities per state. I crawled tripadvisor.com, and scraped data off of the website.

To run my program, a user can type one of four commands that generate plotly charts:
1) "rankings" - this command creates a bar chart showing how many activities rank #1, #2, and #3
2) "reviews" - this command creates a scatter plot that depicts the sum of every states top three activity reviews
3) "type" - this command creates a pie chart that sorts all activities by type, showing how many activities fall under each category
4) "activities [State]" - for this command, a user inputs "activities" followed by a state capitalized (i.e. "activities Michigan" or "activities New York") and the program produces a table of the top three activities to do in the state specified

I first cache all my data into two caches (one cache was too large for github), and then I sort through 2 caches to create my database tables: "Activities," "ActivityInfo," and "States." My Activities table contains a foreign key (Activities.State) that points to the States.Id values. Each States.Id value is correlated with a state name (States.StateName).

The functions drop_db(), create_tables(), and init_db() are commented out because they generate my caches and initialize my database.

My State class initializes a state based on name, attraction, location, and url. It also defines a state string.

My function get_activities() using my state class and returns a list of the top three activities to do in a state by grabbing the activities from my database (trip.db).
