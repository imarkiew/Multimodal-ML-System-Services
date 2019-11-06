FROM python:3.6
WORKDIR /server
ARG requirements=requirements.txt
COPY ./${requirements} ${requirements}
RUN pip install -r ${requirements}
ARG server=scikit_server.py
COPY ./${server} ${server}
ARG utilities=utilities.py
COPY ./${utilities} ${utilities}
ARG model_representation=scikit_model.py
COPY ./${model_representation} ${model_representation}
ARG model=final_model_mlp.sav
COPY ./${model} ${model}
ENV server_env=$server
ENV model_env=$model
ENV config_type=DEFAULT
CMD ["sh", "-c", "python ${server_env} --config_file_path ./server_config.json --config_type ${config_type} --model_file_path ${model_env}"]
