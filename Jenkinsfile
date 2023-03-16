

pipeline {
  agent any 
  stages {


pipeline {
  agent any 
  stages {

      
stage('Build new image') {
		    steps{
            withDockerServer([uri: 'unix:///var/run/docker.sock']) {
         
			       sh "docker build -t test-back:latest ."    
		         
            }
               
            }
}
      }
      
  }
