
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

    stage('Détection de changements') {
      steps {
          script {
            try {
                sh '''
                    pwd
                    jobs_previous="Data/jobs_previous.csv"
                    jobs="Data/jobs.csv"

                    if [ -f "$jobs_previous" ]; then
                        sha256sum "$jobs_previous" | awk '{print $1}' > jobs_previous_sha
                        sha256sum "$jobs" | awk '{print $1}' > jobs_sha

                        if [ $(cat jobs_previous_sha) = $(cat jobs_sha) ]; then
                            echo " fichier identique "
                            exit 0
                        else
                            echo "🔄 Changements détectés – concaténation"
                            cat "$jobs" >> "$jobs_previous"
                        fi
                    else
                        echo "le fichier n'existe  pas"
                        cp "$jobs" "$jobs_previous"
                    fi

                '''
            } catch (Exception e){
                currentBuild.result = "FAILURE"
                error(" Error stage DetectChanges: ${e.message} >> logs/log.txt ")
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

//     stage('Archive') {
//       steps {
//         archiveArtifacts artifacts: '**/*.csv', allowEmptyArchive: true
//       }
//     }
    stage('Deploy dans nginx local') {
      steps {
      //jenkins ne peut pas ecrire dans /var/www/html car n'a pas les droits sur le dossier html qui est root comme proprieatire, root comme groupe
      //on va modifier le groupe du dossier html par le groupe www-data et laisser le proprieatire root : chown -R root:www-data /var/www/html/
      //on ajoute l'utlisateur jenkins a ce groupe www-data : usermod -aG www-data jenkins
      // on permet au groupe d'ecrire dans le repertoire html : chmod g+w /var/www/html
      //redemarrer jenkins pour que les modifications soient prises en compte
      // pourquoi utiliser le groupe www-data car il a été crée lors de l'installation de nginx et pointe sur le repertoire /var/www avec le user www-data
        sh '''
            whoami
            scp public/index.html /var/www/html/
            echo "Déploiement réussie"
        '''
      }
    }
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

