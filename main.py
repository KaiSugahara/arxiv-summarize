import slackweb
import arxiv
import datetime
import pytz
import openai
import os

if __name__ == '__main__':

    try:

        """
            SETUP: Incoming Webhook of Slack
        """
        slack = slackweb.Slack(url=os.getenv("SLACK_URL"))
        
        """
            SETUP: OpenAPI
        """
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        system = """与えられた論文のアブストラクトを日本語で最大3個の箇条書き（体言止め）でまとめ，以下のフォーマットで出力してください．
        ```
        • 要点1
        • 要点2
        • 要点3
        ```"""
        
        def get_abstract_summary(abstract, debug_mode=True):
        
            """
                func: OpenAIのAPIを利用して，与えられたAbstractを要約
                args:
                    - abstract: アブストラクト, str
                returns:
                    - summary: 要約文, str
                    
            """
        
            if debug_mode:
        
                summary = "• 要点A\n• 要点B\n• 要点C"
        
            else:
        
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {'role': 'system', 'content': system},
                        {'role': 'user', 'content': abstract},
                    ],
                    temperature=0.25,
                )
                summary = response["choices"][0]["message"]["content"]
            
            return summary
        
        """
            検索対象日を計算
        """
        
        date = datetime.datetime.now(pytz.timezone('Asia/Tokyo')) - datetime.timedelta(days=7) # 3日前
        date = date.strftime("%Y%m%d")
        print("対象日:", date)
        
        """
            記事の検索
        """
        
        # クエリ: 検索カテゴリ
        cats = ["cs.AI", "cs.IR", "cs.CV", "cs.SE", "cs.LG"]
        query_cat = "%28" + " OR ".join([f'cat:{cat}' for cat in cats]) + "%29"
        
        # クエリ: 検索ワード
        words = ["recommend", "recommendation", "recommender"]
        query_word = "%28" + " OR ".join([f'all:{w}' for w in words]) + "%29"
        
        # クエリ: 検索対象日
        query_date = f"submittedDate:[{date} TO {date}1235959]"
        
        # クエリを結合
        query = " AND ".join([query_cat, query_word, query_date])
        print("クエリ文:\n", query)
        
        # 検索
        search = arxiv.Search(
            query=query,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        
        """
            検索結果を整形
        """
        
        results = [
            {
                "title": result.title,
                "url": result.links[0].href,
                "time": result.published.strftime("%Y/%m/%d %H:%M"),
                "summary": get_abstract_summary(result.summary, debug_mode=False),
            }
            for result in search.results()
        ]
        
        """
            Slackに通知
        """
        
        slack.notify( text=f"{date[:4]}/{date[4:6]}/{date[6:]}に投稿されたarXiv論文（検索対象: 推薦システム）" )
        
        if len(results) > 0:
        
            for result in results:
            
                text = []
            
                text.append( f'<{result["url"]}|{result["title"]}> ({result["time"]})' )
                text.append( result["summary"] )
            
                slack.notify( text="\n".join(text) )
        
        else:
        
            slack.notify( text="文献が見つかりませんでした :sob:" )
    
    except Exception as e:
        
        print(str(e))