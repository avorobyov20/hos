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

sudo apt-get update
sudo apt-get upgrade

sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
    /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
    https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
    /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt-get update
sudo apt-get install fontconfig openjdk-11-jre
sudo apt-get install jenkins=2.387.1

sudo cat /var/lib/jenkins/secrets/initialAdminPassword
66863d75cd4244caadf4a43c05ccc323

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

user="avorobyov2"
pass="***"

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/locale/226.v008e1b_58cb_b_0/locale.hpi


java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/script-security/1228.vd93135a_2fb_25/script-security.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/extended-choice-parameter/359.v35dcfdd0c20d/extended-choice-parameter.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-api/1208.v0cc7c6e0da_9e/workflow-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-input-step/466.v6d0a_5df34f81/pipeline-input-step.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-stage-step/296.v5f6908f017a_5/pipeline-stage-step.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-graph-analysis/202.va_d268e64deb_3/pipeline-graph-analysis.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-rest-api/2.31/pipeline-rest-api.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/commons-lang3-api/3.12.0-36.vd97de6465d5b_/commons-lang3-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/credentials/1189.vf61b_a_5e2f62e/credentials.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/display-url-api/2.3.7/display-url-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/okhttp-api/4.9.3-108.v0feda04578cf/okhttp-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/instance-identity/142.v04572ca_5b_265/instance-identity.hpi


java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/token-macro/321.vd7cc1f2a_52c8/token-macro.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/github-api/1.303-400.v35c2d8258028/github-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/github/1.37.0/github.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-scm-step/400.v6b_89a_1317c9a_/workflow-scm-step.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/jakarta-mail-api/2.0.0-5/jakarta-mail-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/jakarta-activation-api/2.0.0-2/jakarta-activation-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/mailer/438.v02c7f0a_12fa_4/mailer.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/trilead-api/2.84.v72119de229b_7/trilead-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/ssh-credentials/305.v8f4381501156/ssh-credentials.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-step-api/639.v6eca_cd8c04a_a_/workflow-step-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/scm-api/631.v9143df5b_e4a_a/scm-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/plain-credentials/143.v1b_df8b_d3b_e48/plain-credentials.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/credentials-binding/523.vd859a_4b_122e6/credentials-binding.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/jsch/0.1.55.61.va_e9ee26616e7/jsch.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/apache-httpcomponents-client-4-api/4.5.13-138.v4e7d9a_7b_a_e61/apache-httpcomponents-client-4-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/git-client/4.0.0/git-client.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/structs/324.va_f5d6774f3a_d/structs.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/git/5.0.0/git.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/resource-disposer/0.20/resource-disposer.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/bootstrap5-api/5.1.3-6/bootstrap5-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/plugin-util-api/2.16.0/plugin-util-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/checks-api/1.7.4/checks-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/echarts-api/5.3.2-1/echarts-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/jackson2-api/2.13.4.20221013-295.v8e29ea_354141/jackson2-api.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/junit/1119.1121.vc43d0fc45561/junit.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/matrix-project/785.v06b_7f47b_c631/matrix-project.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/ws-cleanup/0.44/ws-cleanup.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-stage-view/2.31/pipeline-stage-view.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/ionicons-api/31.v4757b_6987003/ionicons-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/caffeine-api/2.9.3-65.v6a_47d0f4d1fe/caffeine-api.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-support/839.v35e2736cfd5c/workflow-support.hpi
java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-cps/3641.vf58904a_b_b_5d8/workflow-cps.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-job/1282.ve6d865025906/workflow-job.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket safe-restart

java -jar jenkins-cli.jar -auth $user:$pass -s http://localhost:8080 create-job webhook_catcher < webhook_catcher.xml
java -jar jenkins-cli.jar -auth $user:$pass -s http://localhost:8080 create-job deployer < deployer.xml
