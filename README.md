Script for report pushing in root dir - main_wordfence.py
In script change api_key for dojo
And creds for auth user insteat user:user - your own for dojo dashboard
If you didn't find admin password for dojo you would run next in terminal:

sudo docker-compose exec uwsgi /bin/bash -c 'python manage.py createsuperuser'


Install docker and docker-compose

sudo apt update -y
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo docker-compose --version

For upping the dojo:

sudo ./dc-build.sh
sudo ./dc-up-d.sh

and wait for 15 min - db.
