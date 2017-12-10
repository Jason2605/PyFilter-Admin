<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/Shield.png" width="200"/></a>
</p>

# PyFilter info
PyFilter aims to filter out all of the requests that are not legitimate to your server, and blocks them if too many are sent. It works by reading log files and checking if a failed request has came from the same IP address within a user configurable amount of time and adding rules to the firewall if too many attempts have been captured.

By default PyFilter is configured to read from `/var/log/auth.log` for incoming SSH requests, however there are options for `Apache, Nginx and MySQL` too.

PyFilter uses a database to store all the banned ip addresses to ensure ips arent added more than once. PyFilter currently supports sqlite and redis, by default it is setup to use sqlite so no installation of a redis server is needed. However redis has support for cross server ban syncing (more info below).

[PyFilter Repo](https://github.com/jason2605/PyFilter)

# PyFilter-Admin

PyFilter-Admin provides you with statistical information about PyFilter, such as total bans, bans over the last 10 days, and which server the IP was banned on. Also allows manual addition of rules to the firewall if the selected datastore is redis.

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

Note: Redis only for manual ban addition.

<p align="center">
  <a href="https://pyfilter.co.uk"><img src="https://pyfilter.co.uk/static/images/PyFilter-Admin-Redis.png"/></a>
</p>
