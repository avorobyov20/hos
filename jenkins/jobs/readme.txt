java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/locale/226.v008e1b_58cb_b_0/locale.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/github/1.37.0/github.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/git/5.0.0/git.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/extended-choice-parameter/359.v35dcfdd0c20d/extended-choice-parameter.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-cps/3641.vf58904a_b_b_5d8/workflow-cps.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/ws-cleanup/0.44/ws-cleanup.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/workflow-job/1282.ve6d865025906/workflow-job.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket install-plugin https://updates.jenkins.io/download/plugins/pipeline-stage-view/2.31/pipeline-stage-view.hpi
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://192.168.0.10:8080/ -webSocket safe-restart

java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://localhost:8080 create-job webhook_catcher < webhook_catcher.xml
java -jar jenkins-cli.jar -auth avorobyov2:jassword -s http://localhost:8080 create-job deployer < deployer.xml
