wsl --status
# Default Version: 2

Docker for Windows/ Settings/ Resources/ WSL Integration/ Enable integration with additional distros [Off] Ubuntu

wsl --unregister Ubuntu
wsl --install -d Ubuntu

lsb_release -a
# Ubuntu 22.04.2 LTS

Docker for Windows/ Settings/ Resources/ WSL Integration/ Enable integration with additional distros [On] Ubuntu

sudo apt update && sudo apt upgrade -y

sudo apt install tree
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible

sudo apt install python3-pip
sudo pip install pre-commit

pre-commit --version

git clone --branch master https://github.com/avorobyov20/hos.git
cd hos

git config --global user.name "Артем Воробьев"
git config --global user.email "avorobyov2@gmail.com"

pre-commit install
pre-commit run --all-files

cd app
sudo apt install python3-venv
sudo python3 -m venv env
cd ..

sudo docker-compose up -d --build
sudo docker-compose exec web_dev python manage.py check
sudo docker-compose exec web_dev python manage.py loaddata db.json
sudo docker-compose exec web_dev python manage.py create_user

git push origin master

ssh-keygen
cat .ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDDUkN ansible@local
ubuntu@remote:~$ echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDDUkN ansible@local' >> ~/.ssh/authorized_keys

ssh-keygen -f "/home/ansible/.ssh/known_hosts" -R "192.168.0.24"
ansible-playbook provisioning/site.yml -i provisioning/hosts.yml

git init
git config --global user.name "Артем Воробьев"
git config --global user.email "avorobyov2@gmail.com"
git add .

# Подключиться к контейнеру db_dev и посмотреть созданные базы, пользователей и таблицы
sudo docker-compose exec db_dev psql --username=django_user --dbname=django_db
\l
\dt
выведется база django_db и список созданных через миграцию таблиц
\q

# Проверить, что был создан том для базы
sudo docker volume ls
sudo docker volume inspect project_postgres_volume

# Остановить контейнеры и удалить том
sudo docker-compose down
sudo docker volume ls
sudo docker volume rm project_postgres_volume

# Остановить и удалить контейнеры, объявленные в docker-compose.yml вместе со всеми их volumes
sudo docker-compose down -v
# Выполнить билд и запуск контейнеров используя файл docker-compose.prod.yml
sudo docker-compose -f docker-compose.prod.yml up -d --build

sudo docker-compose -f docker-compose.prod.yml down -v
sudo docker-compose -f docker-compose.prod.yml up -d --build
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

# Эти файлы должны отображаться на обоих контейнерах т.к. они работают с одним томом
sudo docker exec project-nginx-1 ls /home/app/web/static
sudo docker exec project-web-1 ls /home/app/web/static

# Для проверки медиа файлов, которые будут загружаться через Django, можно создать пустой файл
sudo docker exec project-nginx-1 touch /home/app/web/media/test.txt
# и выполнить к нему запрос, который не должен завершаться ошибкой 404
curl localhost:1337/media/test.txt
