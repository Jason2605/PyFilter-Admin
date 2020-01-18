<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/Shield.png" width="200"/></a>
</p>

# PyFilter info
PyFilter aims to filter out all of the requests that are not legitimate to your server, and blocks them if too many are sent. It works by reading log files and checking if a failed request has came from the same IP address within a user configurable amount of time and adding rules to the firewall if too many attempts have been captured.

By default PyFilter is configured to read from `/var/log/auth.log` for incoming SSH requests, however there are options for `Apache, Nginx and MySQL` too.

PyFilter uses a database to store all the banned ip addresses to ensure ips aren't added more than once. PyFilter currently supports sqlite and redis, by default it is setup to use sqlite so no installation of a redis server is needed. However redis has support for cross server ban syncing (more info below).

[PyFilter Repo](https://github.com/jason2605/PyFilter)

# PyFilter-Admin

PyFilter-Admin provides you with statistical information about PyFilter, such as total bans, bans over the last 10 days, and which server the IP was banned on. Also allows manual addition of rules to the firewall if the selected datastore is redis.

## Installing

First we will clone this repo via the following command `git clone https://github.com/Jason2605/PyFilter-Admin`

Next we need to download all the python packages needed to run PyFilter-Admin, this is very simple because all the requirements are within the `requirements.txt` file. To install run `pip install -r requirements.txt`

## Configuration

Once we have cloned the repository, we need to setup the configuration for PyFilter-Admin. This is a painless process. There is an included default config file `config.default.json`, rename this to `config.json`. Inside the configuration file we need to define the backend that our PyFilter processes are using (Sqlite or Redis).
```json
{
  "settings": {
    "debug": false,
    "database": "redis",
    "ignored_ips": ["127.0.0.1"],
    "country_amount": 12
  },
  "redis": {
    "host": "",
    "password": "",
    "database": 0
  },
  "sqlite": {
    "database": "PyFilter.db"
  }
}
```
If the backend is redis, it's simply just a case of entering the Redis connection information. If the backend is sqlite, we need to update the database key within settings, and provide the path to the sqlite database in the sqlite section.

`"ignored_ips"` is a whitelist of IP addresses which are unable to be banned via the web interface.
`"country_amount"` is the amount of countries to show on the bar chart before bundling them into "other".

## Running

Once all the packages are installed you can run PyFilter-Admin with the following command `python run_server.py`

The default username is: PyFilter
The default password is: PyFilter12345

**Please change the password after the first login!**

## Screenshots

<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/PyFilter-Admin-Login.png"/></a>
</p>

<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/PyFilter-Admin.png"/></a>
</p>

<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/PyFilter-Admin-1.png"/></a>
</p>

Note: Redis only for manual ban addition and chart information.

<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/PyFilter-Admin-Redis.png"/></a>
</p>

<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/PyFilter-Chart.png"/></a>
</p>
