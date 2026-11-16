pipeline {
    agent any

    // Automatic triggering: GitHub webhook (githubPush) with SCM polling as fallback
    triggers {
        githubPush()
        pollSCM('H/2 * * * *')
    }

    environment {
        IMAGE_NAME = 'smart-url-shortener'
        VENV       = '.venv'
        PATH       = "/opt/homebrew/bin:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    ${VENV}/bin/pip install --upgrade pip
                    make PYTHON=${VENV}/bin/python install
                '''
            }
        }

        // Component 1 Enhancement, Option A: automated tests before packaging
        stage('Test') {
            steps {
                sh 'make PYTHON=${VENV}/bin/python test'
            }
        }

        stage('Build') {
            steps {
                sh 'make PYTHON=${VENV}/bin/python build'
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'dist/*.whl', fingerprint: true
            }
        }

        // Component 1 Enhancement, Option B: image tag = build number + git SHA
        stage('Docker Build') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    script {
                        def sha = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                        env.IMAGE_TAG = "${env.BUILD_NUMBER}-${sha}"
                    }
                    sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                }
            }
        }
    }

    post {
        success { echo "Build ${env.BUILD_NUMBER} succeeded" }
        failure { echo "Build ${env.BUILD_NUMBER} failed" }
    }
}
