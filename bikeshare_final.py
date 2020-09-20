import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ["January", "February", "March", "April", "May", "June", "All"]
DAY_DATA = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("\nWhich of the following cities would you like to examine:\n")
    # send to make_menu() to generate menu for selection
    city_choice = make_menu(list(CITY_DATA))    
    city = CITY_DATA.get(list(CITY_DATA)[city_choice - 1])     

    # get user input for month (all, january, february, ... , june)
    print("\nWhich of the following months would you like to examine:\n")
    # send to make_menu() to generate menu for selection
    month_choice = make_menu(MONTH_DATA) 
    month = MONTH_DATA[month_choice - 1]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nWhich of the following days would you like to examine:\n")
    # send to make_menu() to generate menu for selection
    day_choice = make_menu(DAY_DATA)  
    day = DAY_DATA[day_choice - 1]

    print('-'*40)
    return city, month, day

def make_menu(menu_list):
    """
    Take the lists/list versions of CITY_DATA, MONTH_DATA, or DAY_DATA and turn
    them into menus for the user to select from.

    Args:
        (list) menu_list - list of options for menu
    Returns:
        (str) choice - user choice
    """
    # while loop to work with any length of passed in list
    index = 1
    while index < len(menu_list):
      for item in menu_list:
        print("{}. {}".format(index, item.title()))
        index += 1
    while True:
      try:
        choice = int(input("Your choice (1 - {}): ".format(len(menu_list))))
      except ValueError:
        print("Sorry I didn't understand that.")
        continue
      if choice not in range(1, len(menu_list) + 1):
        print("Please make a valid choice:")
        continue
      else:
        break          

    return choice

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
        
    # Convert "Start Time" using to_datetime()
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract and create new columns from "Start Time"
    df["Month"] = df["Start Time"].dt.month
    df["Day"] = df["Start Time"].dt.weekday_name
    df["Hour"] = df["Start Time"].dt.hour

    # Get index of month to create new df
    if month != "All":
      month = MONTH_DATA.index(month)      
      df = df[df["Month"] == month + 1]

    # Create new df using day
    if day != "All":
      df = df[df["Day"] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # take mode of "Month" and account for starting from 1 to get index of MONTH_DATA
    print("The most common month for usage is {}.".format(MONTH_DATA[df["Month"].mode()[0] - 1]))
    
    # display the most common day of week
    print("The most common day for usage is {}.".format(df["Day"].mode()[0]))

    # display the most common start hour                                     
    print("The most common starting hour is {}:00.".format(df["Hour"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station using mode() on "Start Station"
    print("The most common starting station is: {}.".format(df["Start Station"].mode()[0]))

    # display most commonly used end station using mode() on "End Station"
    print("The most common starting station is: {}.".format(df["End Station"].mode()[0]))

    # display most frequent combination of start station and end station trip
    df["frequent_combo"] = df['Start Station'] + "," + df['End Station']

    frequent_combo = df["frequent_combo"].mode()[0]
    frequent_combo_start, frequent_combo_end = frequent_combo.split(",")
    print("The most frequent combination of starting and ending station is: {} and {}".format(frequent_combo_start, frequent_combo_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_sum = df["Trip Duration"].sum()
    tot_days = int(trip_sum / 86400)
    tot_hours = int((trip_sum % 86400) / 60)
    tot_minutes = int(((trip_sum % 86400) % 60))
    print("The total travel time for the filtered data is: {} Days, {} Hours, and {} Minutes.".format(tot_days, tot_hours, tot_minutes))

    # display mean travel time
    trip_mean = df["Trip Duration"].mean()
    
    # Account for possible mean time over 1 hour
    mean_hours = int(trip_mean / 3600)
    
    # Most likely duration mean times
    mean_minutes = int((trip_mean % 3600) / 60)
    mean_seconds = int((trip_mean % 3600) % 60)
    
    print("The mean travel time for the filtered data is: {} Days, {} Hours, and {} Minutes.".format(mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats for the filtered data...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser Type counts:")
    print(df["User Type"].value_counts())

    # Display counts of gender
    # Only works for DataFrames with the column "Gender"
    if "Gender" in df.columns:
        print("\nUser Gender counts:")
        print(df["Gender"].value_counts())
    else:
        print("\nThe data for you chosen city does not contain data on the gender of users.")  

    # Display earliest, most recent, and most common year of birth
    # Only works for DataFrames with the column "Birth Year"
    if "Birth Year" in df.columns:
        print("\nUser birth years:")
        oldest_users = int(df["Birth Year"].min())
        youngest_users = int(df["Birth Year"].max())
        most_common = int(df["Birth Year"].mode())        
        print("The oldest user(s) were born in: {}".format(oldest_users))
        print("The youngest user(s) were born in: {}".format(youngest_users))
        print("The most common birth year is: {}".format(most_common))
    else:
        print("\nThe data for you chosen city does not contain data on the birth year of users.") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw DataFrame data if the user chooses to see it"""
    position = 0

    while True:
      choice = input("Would you like to examine the data five (5) rows at a time? \n[y]es or [n]o: ").lower()
      if choice != "y" and choice != "n":
        print("Please make a valid choice:")
        continue
      else:
        break         

    while choice != "n":
      print(df.iloc[position : (position + 5)])
      position += 5

      while True:
        choice = input("Continue? [y]es or [n]o: ")
        if choice != "y" and choice != "n":
          print("Please make a valid choice:")
          continue
        else:
          break  
          
def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()