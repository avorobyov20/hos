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
sudo apt-get install jenkins=2.361.1

user="avorobyov2"
pass="***"

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/locale/226.v008e1b_58cb_b_0/locale.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/github/1.37.0/github.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/git/5.0.0/git.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/extended-choice-parameter/359.v35dcfdd0c20d/extended-choice-parameter.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-cps/3641.vf58904a_b_b_5d8/workflow-cps.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/ws-cleanup/0.44/ws-cleanup.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-job/1282.ve6d865025906/workflow-job.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-rest-api/2.31/pipeline-rest-api.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-stage-view/2.31/pipeline-stage-view.hpi

java -jar jenkins-cli.jar -auth $user:$pass -s http://192.168.0.10:8080/ -webSocket safe-restart

java -jar jenkins-cli.jar -auth $user:$pass -s http://localhost:8080 create-job webhook_catcher < webhook_catcher.xml
java -jar jenkins-cli.jar -auth $user:$pass -s http://localhost:8080 create-job deployer < deployer.xml
