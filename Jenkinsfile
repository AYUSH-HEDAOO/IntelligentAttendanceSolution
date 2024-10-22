@Library("Shared") _
pipeline{
    
    agent { label "Django"}
    
    stages{
        
        stage("Hello"){
            steps{
                script{
                    hello()
                }
            }
        }
        stage("Code"){
            steps{
               script{
                    clone("https://github.com/AYUSH-HEDAOO/IntelligentAttendanceSolution.git","main")
               }
                
            }
        }
        stage("Build"){
            steps{
                script{
                    docker_build("ias","latest","prafulcoder")
                }
            }
        }
        stage("Push to DockerHub"){
            steps{
                script{
                    docker_push("ias","latest","prafulcoder")
                }
            }
        }
        stage("Deploy"){
            steps{
                echo "This is deploying the code"
                sh "docker compose down && docker compose up -d"
            }
        }
    }
}