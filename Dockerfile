FROM python:2

ADD tests /tests
ADD new_channel_bot.py /new_channel_bot.py
ADD requirements.txt /requirements.txt
ADD test-requirements.txt /test-requirements.txt

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt

CMD ["python", "/new_channel_bot.py"]
