import time
import pandas as pd
import numpy as np

CITIES = { 'Chicago': 'chicago.csv',
           'New York': 'new_york_city.csv',
           'Washington': 'washington.csv' }
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'All']

print()
print('Hello! Let\'s explore some US bikeshare data!')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Get user input for city
    city = input('\nWould you like to see data for Chicago, New York, or Washington? (Not case-sensitive): ')
    city = city.title() # Capitalize first letter of each word
    month = [] # Month will be determined by user selection
    day = [] # day will be determined by user selection
    print()

    while city not in CITIES: # This is to handle invalid input
        city = input('Oops! Something is not right. Please check your spelling to make sure you type the correct city name. Let\'s try this again: ')
        city = city.title()
        print()

    # Ask user if they would like to filter the data by month, day or not at all
    options = ['Month','Day','None'] # Create a list of valid input
    choice = input('You selected the data from {}. Would you like to filter the data by month, day, or not at all? Please specify by typing "month", "day", or "none": '.format(city))
    choice = choice.title()
    print()

    while choice not in options: #  This is to handle invalid input
        choice = input('Oops! Something is not right. Please check your spelling to make sure you make the correct selection. Let\'s try this again: ')
        choice = choice.title()
        print()

    # Determine a specific month as the filter
    if choice == 'Month':
        day = 'All' # If the user chooses to filter by month, all the days of week will be selected
        # Get user input for a specific month
        month = input('Which month - January, February, March, April, May, or June? ')
        month = month.title()
        while month not in MONTHS: # This is to handle invalid input
            month = input('Oops! Something is not right. Please check your spelling to make sure you type in the correct month. Let\'s try this again: ')
            month = month.title()
            print()

     # Determine a specific weekday as the filter
    elif choice == 'Day':
        month = 'All' # If the user chooses to filter by day, all the months will be selected
        # Get user input for a specific day of week
        day = input('Which day of week - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ')
        day = day.title()
        while day not in DAYS: # This is to handle invalid input
            day = input('Oops! Something is not right. Please check your spelling to make sure you type in the correct day. Let\'s try this again: ')
            day = day.title()
            print()

    else: # If the user chooses to not filter the data, all the months and weekdays will be selected
        month = 'All'
        day = 'All'

    print('-'*40)
    return city, month, day

# Use the filter returned by get_filter() to create a new dataframe
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
    # Load data file of the user-selected city into a dataframe
    df = pd.read_csv(CITIES[city])

    # Convert the 'Start Time' column into datetime Series
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hours from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Week Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

   # If user selected 'month' as filter criteria
    if month != 'All':
        month = MONTHS.index(month) + 1 # Use the index of the months list to get the corresponding int for  the month
        df = df[df['Month'] == month] # Create a new dataframe according to the selected month

    # If user selected 'day' as filter criteria
    if day != 'All':
        df = df[df['Week Day'] == day] # Create a new dataframe according to the selected weekday

    return df


# Get the most frequent times of travel
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = int(df['Month'].mode()) # Set the value to be int
    print('1. The most common month for travel is', MONTHS[common_month - 1]) # Convert 'common_month' into the index to find 'months' list to find the corresponding month name from the 'months' list
    print()

    # Display the most common day of week
    common_day = df['Week Day'].mode()
    print('2. The most common day of week for travel is', common_day[0])
    print()

    # Display the most common start hour
    common_hour = df['Hour'].mode()
    print('3. The most common hour for travel is', common_hour[0])
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Get the most popular stations and trips
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Station Combination'] = 'from ' + df['Start Station'] + ' to ' + df['End Station'] # Create a new column for the combination of start and end stations

    # Display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('1. The most commonly used start station is', common_start)
    print()

    # Display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('2. The most commonly used end station is', common_end)
    print()


    # Display most frequent combination of start station and end station trip
    common_combo = df['Station Combination'].mode()[0]
    print('3. The most frequent combination of start and end station trip is', common_combo)
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Get the total and average trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in terms of hours and seconds
    totaltime = df['Trip Duration'].sum()
    hours = "{:,}".format(int(totaltime // 3600)) # Convert seconds into integral hours
    minutes = int(totaltime % 3600 // 60) # Convert the remaining seconds from the seconds-to-hour conversion into minutes
    print('1. The total travel time is {} hours and {} minutes '.format(hours,minutes))
    print()

    # Display the mean travel time
    avgtime = df['Trip Duration'].mean()
    hours = int(avgtime // 3600)
    minutes = int(avgtime % 3600 // 60)
    print('2. The average travel time is {} hours and {} minutes '.format(hours,minutes))
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Get the statistics on bike share users - This function is for Chicago and New York as both data files contain user gener and birth year
def user_stats_a(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertypes = df['User Type'].value_counts()
    print('1. Following are the counts of users by user type: \n\n', usertypes)
    print()


    # Display counts of user gender
    genders = df['Gender'].value_counts()
    print('2. Following are the counts of users by gender: \n\n', genders)
    print()


    # Display the earliest, most recent, and most common year of birth
    earliest = int(df['Birth Year'].min())
    latest = int(df['Birth Year'].max())
    commonyear = int(df['Birth Year'].mode()[0])
    print('3. The earliest birth year of those users is {}, the most recent birth year is {}, and the most common birth year is {}.'.format(earliest,latest,commonyear))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Get the statistics on bike share users - This function is for Washington as the data file does not contain user gener and birth year
def user_stats_b(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertypes = df['User Type'].value_counts()
    print('Following are the counts of users by user type: \n\n', usertypes)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Display 5 rows of data at a time depending on user input
        display = input ('\nThanks for your patience! The data is filtered according to your selection: City - {}, Month - {}, Day of Week - {}.\n\nWould you like to see the raw data first? Type yes or no:  '.format(city,month,day))
        display = display.title()
        i = 0 # This is row counter for displaying data
        print()

        # If the user answers 'yes,' print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of the data.
        # The script will continue prompting and printing the next 5 rows at a time until the user chooses 'no,'
        while display != 'No':
            while display not in ['Yes','No']:
                display = input('\nSomething is not right, please try again by typing yes or no: ')
                display = display.title()
                print()
            print(df[i:i+5]) # Only print 5 rows at a time
            i += 5 # Increase the row counter by five in preparation for printing the next 5 rows
            display = input('\n\nWould you like to see the next 5 rows? Type yes or no: ')
            display = display.title()

        print('\nThanks! Here are the statistics:\n')

        print('-'*40)

        # Run through all the functions for statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # If the user selected 'Washington', only display the counts of user by user type because the data file does not contain user gender and birth year
        if city != 'Washington':
            user_stats_a(df)
        else:
            user_stats_b(df)

        restart = input('\nAnalysis completed! Would you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
