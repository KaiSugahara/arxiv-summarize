FROM python:latest

# 環境変数
ARG SLACK_URL
ARG OPENAI_API_KEY
ENV TZ=Asia/Tokyo

# ライブラリ
RUN pip install -U pip
RUN pip install slackweb arxiv openai pytz

# 定期実行（毎朝9:00）
RUN apt update && apt -y install cron

RUN echo 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin' >> /etc/cron.d/crontab
RUN echo "SLACK_URL=$SLACK_URL" >> /etc/cron.d/crontab
RUN echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> /etc/cron.d/crontab
RUN echo "CRON_TZ=Asia/Tokyo" >> /etc/cron.d/crontab
RUN echo '00 09 * * * /usr/local/bin/python3 /main.py > /tmp.log' >> /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]