aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
docker build --platform linux/amd64 -t c11-nixie-lnhm-etl .
docker tag c11-nixie-lnhm-etl:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-nixie-lnhm-etl:latest
docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-nixie-lnhm-etl:latest