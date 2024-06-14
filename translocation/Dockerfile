FROM public.ecr.aws/lambda/python:latest
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements.txt
COPY requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

COPY translocation.py .

CMD ["summarise.lambda_handler"]