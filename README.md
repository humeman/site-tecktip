# site-tecktip
The source code for [tecktip.today](https://tecktip.today), a _revolutionary_ website which delivers the best and brightest tecknological advice directly to a web browser near you.

## Why?
This website is a joke. It was initially a Discord bot named "teck tip bot" which would reply with _innovative_ teck tips from Linus himself after hearing certain trigger words -- and eventually, when I realized `.today` existed as a TLD, I had to make it a website.

The joke as a whole was, I think, somewhat inspired by [@LinusTechTip_ on Twitter](https://x.com/linustechtip_).

It accepts submissions from anyone, and has a neat admin panel that allows for managing tips, submissions, and images.

## Design
The backend is a simple Quart API written in Python and backed by a MySQL database. The frontend is built on SvelteKit and uses Tailwind.

Both of these are automatically deployed using GitHub Workflows and an Ansible playbook.

## Screenshots
![image](https://github.com/user-attachments/assets/715d1305-fd67-41f5-9be8-48400c2bc218)
_The tecktip.today homepage._

![image](https://github.com/user-attachments/assets/5a57d0a2-191b-4033-9aa2-97f3d15b2cad)
_The admin panel._

![image](https://github.com/user-attachments/assets/6f26b99a-da1b-4cea-9fe7-5cf67fe42acb)
_TeckGPT, a teck tip generating assistant running off of a ChatGPT fine-tuned model._

![image](https://github.com/user-attachments/assets/2825c555-9598-43ef-a596-440610ff41f7)
![image](https://github.com/user-attachments/assets/5437adc9-cf0d-49d4-84b8-39d9c358c267)
_The site allows visitors to submit their own teck tips for review._

![image](https://github.com/user-attachments/assets/712aefec-ca82-444f-8748-d235a3f36291)
_Images can be uploaded by admins. Definitely don't want submissions for that one._

![image](https://github.com/user-attachments/assets/65ba5448-201c-4f66-8810-bd60d5ef3a96)
_Full edit logs._

## Use
I'm not sure why anyone would want this... but here's how to run it:

#### Manual
To run the backend, set the following env vars:
- MYSQL_HOST 
- MYSQL_USER 
- MYSQL_PASSWORD 
- MYSQL_DB  
- HYPERCORN_CERTFILE ("/etc/letsencrypt/live/{{ site_host }}/fullchain.pem")
- HYPERCORN_KEYFILE ("/etc/letsencrypt/live/{{ site_host }}/privkey.pem")
- PORT
- IMAGE_URL
- IMAGE_FOLDER
- OPENAI_API_KEY
- OPENAI_MODEL

Then install dependencies:
```sh
cd src_api
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Then run:
```sh
python3 main.py
```

To get the frontend, first build it:
```sh
cd src_site
npm run build
```

Then start it:
```
SITE_HOST="some-host" API_PORT="backend-port" HOST="127.0.0.1" PORT=some-port node build/index.js
```

For development purposes, you can also run it with:
```sh
SITE_HOST="some-host" API_PORT="backend-port" HOST="127.0.0.1" PORT=some-port npm run dev
```

#### Ansible Playbook
Your vault needs to contain the following:
- sql.db
- sql.user
- sql.password
- site_host (ie: tecktip.today)
- cdn_host (ie: cdn.tecktip.today)
- site_name (nginx site name)
- openai_key (for TeckGPT)
- openai_model (for TeckGPT)

The server this is being deployed to must have a local MySQL instance running on it. Assuming a login is permitted with `sudo mysql -uroot` and no password, the database and user do not need to be created beforehand. Your server should be using Nginx. A records should exist for site_host and cdn_host.

You can then run the Ansible playbook:
```sh
ansible-playbook playbooks/main.yml
```

