
pipeline {
  agent any

  environment {
    VENV_DIR = 'venv'
  }

  stages {
    stage('Preparation de l\'environnement virtuel'){
        steps{

            sh '''
                python3 -m venv $VENV_DIR
            '''
        }
    }


    stage('Installation et activation de l\'environnement virtuel') {
      steps {
        sh '''
            . $VENV_DIR/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
        '''
      }
    }

    stage('Run Scraping jobs') {
      steps {
          script {
              try {
                  sh '$VENV_DIR/bin/python scraper.py'
              } catch (Exception e){
                  currentBuild.result = "FAILURE"
                  error(" Échec du stage Run, Error: ${e.message} >> logs/log.txt")
              }
          }
      }
    }

    stage('Transformation csv to HTML') {
      steps {
          script {
              try {
                  sh '$VENV_DIR/bin/python html_generator.py Data/jobs.csv public/index.html'
              } catch (Exception e){
                  currentBuild.result = "FAILURE"
                  error(" Échec execution de la transformation: ${e.message} >> logs/log.txt ")
              }
          }
      }
    }

    stage('Validation / Tests') {
      steps {
          script {
            try {
                sh '$VENV_DIR/bin/python -m pytest -v Test/*.py'
            } catch (Exception e){
                currentBuild.result = "FAILURE"
                error(" Échec execution validation tests: ${e.message} >> logs/log.txt ")
            }
          }
      }
    }

    stage('Détection de changements') {
      steps {
          script {
            try {
                sh '''
                    pwd

                '''
            } catch (Exception e){
                currentBuild.result = "FAILURE"
                error(" Échec execution validation tests: ${e.message} >> logs/log.txt ")
            }
          }
      }
    }


//     stage('Archive') {
//       steps {
//         archiveArtifacts artifacts: '**/*.csv', allowEmptyArchive: true
//       }
//     }
   }

  post {
      always {
          sh 'rm -rf $VENV_DIR || true'
      }
      failure {
          script {
              echo ' echec du pipeline, Consultez les logs'
          }

      }
  }
}

