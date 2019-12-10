commend to run cron automatic notice in the backend
*/5 * * * * source /Users/Yi/Documents/class/final-project-term1/final-project-back/env/bin/activate && /usr/bin/python3 /Users/Yi/Documents/class/final-project-term1/final-project-back/lliregistration_back/manage.py runcrons >> /Users/Yi/Documents/class/final-project-term1/final-project-back/cronjob.log
