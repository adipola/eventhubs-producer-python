FROM continuumio/miniconda:latest
COPY environment.yml ./
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN conda env create --file environment.yml
RUN echo "conda activate yahoofinance" > ~/.bashrc
ENV PATH /opt/conda/envs/yahoofinance/bin:$PATH
RUN python ./sendToEventHubs.py

