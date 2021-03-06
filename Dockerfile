# start by pulling the python image
FROM python:3.9-slim-bullseye



# Install dependencies:
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install Werkzeug==2.0.0
RUN pip install jinja2==3.0

# switch working directory


# COPY ./docker-entrypoint.sh /docker-entrypoint.sh
# RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]
# RUN ls

# configure the container to run in an executed manner
EXPOSE 5000
ENV FLASK_APP run.py                                                                                                                
ENV FLASK_ENV development
ENV CONFIG_MODE Docker

# copy every content from the local file to the image
COPY . ./

# Docker init
RUN ["chmod", "+x", "docker-entrypoint.sh"]
RUN ["chmod", "+x", "init-sql.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]


