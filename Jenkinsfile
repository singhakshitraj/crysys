pipeline {
    agent any

    parameters {
        string(name:'IMAGE_NAME', defaultValue:'singhakshitraj/crysys', description:'')
        string(name:'IMAGE_TAG', defaultValue:'1.0', description:'')
    }

    stages {

        stage("build image") {
            steps {
                sh "docker build -t ${params.IMAGE_NAME}:${params.IMAGE_TAG} ."
            }
        }

        stage('login to dockerhub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',usernameVariable: 'DOCKER_USER',passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('push image') {
            steps {
                sh "docker push ${params.IMAGE_NAME}:${params.IMAGE_TAG}"
            }
        }

        stage('migrations') {
            steps {
                withCredentials([file(credentialsId: 'crysys-env-file',variable: 'ENV_FILE')]) {

                    sh """
                        docker run --rm \
                          --env-file $ENV_FILE \
                          ${params.IMAGE_NAME}:${params.IMAGE_TAG} \
                          alembic upgrade head
                    """
                }
            }
        }

        stage('deploy container') {
            steps {
                withCredentials([file(credentialsId: 'crysys-env-file',variable: 'ENV_FILE')]) {

                    sh """
                        docker rm -f crysys_app || true

                        docker run -d \
                          --name crysys_app \
                          --env-file $ENV_FILE \
                          -p 8000:8000 \
                          ${params.IMAGE_NAME}:${params.IMAGE_TAG}
                    """
                }
            }
        }
    }
}
