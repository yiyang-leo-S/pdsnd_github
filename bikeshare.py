#time how long the actions take each
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input("Please specify city to analyze (chicago/new york city/washington):").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Invalid input,try again: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please specify month (from 'january' to 'june' or type 'all'): ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Invalid input,try again: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please specify day of week (or type 'all'): ").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("Invalid input,try again: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start & End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mon = df['month'].mode()[0]
    print(f'Most Frequent month: {mon}')

    # display the most common day of week
    dow = df['day_of_week'].mode()[0]
    print(f'Most Frequent day of week: {dow}')

    # display the most common start hour
        # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f'Most Frequent Start Hour: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].mode()[0]
    print(f'The most commonly used start station: {start}')

    # display most commonly used end station
    end = df['End Station'].mode()[0]
    print(f'The most commonly used end station: {end}')

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    secombo = df['routes'].mode()[0]
    print(f'The most frequent combination of start station and end station trip: {secombo}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    ttt = df['duration'].sum()
    print(f'Total travel time: {ttt}')

    # display mean travel time
    mtt = df['duration'].mean()
    print(f'Mean travel time: {mtt}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'Counts of user types: {user_types}')

    if city != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(f'Counts of gender: {gender}')

        # Display earliest, most recent, and most common year of birth
        earl = int(df['Birth Year'].min())
        mrecent = int(df['Birth Year'].max())
        mcomm = int(df['Birth Year'].mode()[0])
        print(f'The earliest year of birth: {earl}\nThe most recent year of birth: {mrecent}\nThe most common year of birth: {mcomm}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
     Display five lines of raw data if the user indicates that they want to see
     raw data. It should keep asking the user until he/she says no.
    """
    start = 0
    end = 5
    display = input("Do you want to see more raw data? Enter yes or no ").lower()

    if display == 'yes':
        while end <= df.shape[0] - 1:
            print(df.iloc[start:end,:])
            start += 5
            end += 5

            end_display = input("Do you wish to continue or not?: ").lower()
            if end_display == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
