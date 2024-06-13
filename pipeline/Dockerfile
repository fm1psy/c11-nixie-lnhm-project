FROM public.ecr.aws/lambda/python:latest
WORKDIR ${LAMBDA_TASK_ROOT}

# RUN sudo apt-get update
# RUN sudo apt-get install -y freetds-dev freetds-bin libkrb5-dev
# RUN pip install --no-binary :all: pymssql --no-cache

# Copy requirements.txt
COPY requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

COPY extract.py .
COPY transform.py .
COPY load.py .
COPY pipeline.py .

CMD ["pipeline.lambda_handler"]
