# arxivrec-reporter

Automated arXiv paper summarization and notification via Slack using GPT-3.5 (OpenAI)

Note: This app is specialized for Japanese. Please use a translation tool as needed to read the following description, which is provided in Japanese.

## Getting started

### Requirements
- Docker + Docker-Compose
- Incoming Webhooks URL (Slack)
- OpenAI API Key

### How to start

#### Step1.

リポジトリをクローンします．
```bash
$ git clone git@github.com:KaiSugahara/arxiv-summarizer.git
```
OR
```bash
$ git clone https://github.com/KaiSugahara/arxiv-summarizer.git
```

#### Step2.

環境変数の設定ファイルを作成します．
```bash
$ cd arxiv-summarizer
$ cp .env.example .env
```

編集して，用意した `Incoming Webhooks URL` と `OpenAI API Key` をセットします．
```bash
SLACK_URL=[your_url]
OPENAI_API_KEY=[your_key]
```

#### Step3.

コンテナを起動します．
```bash
$ docker-compose build --no-cache
$ docker-compose up -d
```
