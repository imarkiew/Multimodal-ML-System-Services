FROM python:3.6
WORKDIR /server
ARG requirements=requirements.txt
COPY ./${requirements} ${requirements}
RUN pip install -r ${requirements}
ARG proxy_server=server.py
COPY ./${proxy_server} ${proxy_server}
ARG utilities=utilities.py
COPY ./${utilities} ${utilities}
ARG examinations=examinations.py
COPY ./${examinations} ${examinations}
ENV proxy_server_env=$proxy_server
ENV config_type=DEFAULT
CMD ["sh", "-c", "python ${proxy_server_env} --config_file_path ./proxy_server_config.json --config_type ${config_type}"]
