import wget
# Define the remote file to retrieve
remote_url = 'http://www.cs7ns1.scss.tcd.ie/gilbridj'
# Define the local filename to save data
local_file = 'gilbridj'
# Make http request for remote file data
wget.download(remote_url, local_file)