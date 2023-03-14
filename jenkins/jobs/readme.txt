Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.boot_timeout = 900
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 22, host: 2224, id: "ssh"
  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end
end

vagrant up

sudo apt update
sudo apt upgrade

sudo apt-add-repository ppa:ansible/ansible
sudo apt update
sudo apt install ansible

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
    /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
    https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
    /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install fontconfig openjdk-11-jre
sudo apt install jenkins=2.387.1

sudo apt install xclip
xclip -o > file.txt
sudo cat /var/lib/jenkins/secrets/initialAdminPassword | xclips

echo admin:$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword) > creds

http://192.168.0.10:8080/

Нажать "Select plugins to install"
Нажать "None" (все галки очистятся)
Находим плагин "Locale"
Жмем "Install"
Создаем пользователя
Жмем "Save and Finish"
Жмем "Start using Jenkins"

Жмем "Настроить Jenkins"
Жмем "Конфигурация системы"
Количество сборщиков = 1
В разделе "Locale" заполняем "Default Language" значением en
Ставим галку [v] Ignore browser preference and force this language to all users
Нажимаем "Сохранить". Интерфейс переключится на английский язык
Идем "Manage Jenkins" > "Jenkins CLI"
Копируем ссылку на jenkins-cli.jar
Возвращаемся в консоль
wget http://192.168.0.10:8080/jnlpJars/jenkins-cli.jar

locale:226.v008e1b_58cb_b_0
github:1.37.0
git:5.0.0
extended-choice-parameter:359.v35dcfdd0c20d
workflow-cps:3641.vf58904a_b_b_5d8
ws-cleanup:0.44
workflow-job:1282.ve6d865025906
pipeline-stage-view:2.31

java -jar jenkins-cli.jar -auth $user:$pass -s http://localhost:8080 create-job webhook_catcher < webhook_catcher.xml
java -jar jenkins-cli.jar -auth $user:$pass -s http://localhost:8080 create-job deployer < deployer.xml

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket safe-restart
java -jar jenkins-cli.jar -auth admin:$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword) -s http://localhost:8080/ -webSocket safe-restart

