#-*-coding:utf-8-*-
from requests_oauthlib import OAuth1Session
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib.request
import random
import json
import time
import sys
import os


CK = 'WVuaPR454OnzIrX8aylLdwGaj'                             # Consumer Key
CS = 'qLxNgE8ELTU1HcUW28YfJvPtlDCLXBM9BOxMrZo4FOQAFZmLMs'    # Consumer Secret
AT = '900198539397083136-XizT2NOTEqmVdgJkdX32r5Vc2Ag9RYa'    # Access Token
AS = 'eXMf2X6ZY5B2Dnjch5IxbywkisPbMzvIj1PiHxFIkTAOF'         # Accesss Token Secert


class MedamachanBot(object):
    """精神疾患関連の情報を自動でTweetするBot

    パラメータ
    --------------------
    customer_key : str
                 カスタマーキー
    customer_secret : str
                 カスタマーシークレットキー
    access_token : str
                 アクセストークン
    access_token_secret : str
                 アクセストークンシークレットキー
    """

    def __init__(self ,customer_key ,customer_secret ,access_token ,access_token_secret):
        #アクセス情報を初期化
        self.customer_key = customer_key
        self.customer_secret = customer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.oath_key_dict = {
            "consumer_key": self.customer_key,
            "consumer_secret": self.customer_secret,
            "access_token": self.access_token,
            "access_token_secret": self.access_token_secret
        }

    def main(self):
        tweets = []
        tags =["#自傷","#幻覚","#拒食症","#自閉症スペクトラム","#てんかん","#癲癇","#金縛り","#多重人格","#発達障害","#統合失調症","#就労支援","#鬱","#安定剤","#ADHD","#アスペルガー","#レキソタン","#OD","#闘病","#精神病棟","#カプグラ症候群"]
        picked_up_tags = [tags[random.randint(0, len(tags) -1)],tags[random.randint(0, len(tags) -1)],tags[random.randint(0, len(tags) -1)],tags[random.randint(0, len(tags) -1)]]
        for tag in picked_up_tags:
          tweets.append(self.twitter_searcher(tag ,self.oath_key_dict))

        for tweet in tweets:
          follower , follow  = self.twitter_retweeter(tweet,self.oath_key_dict)

        self.follower_transition_log(follower , follow)
        self.transition_output()

    def create_oath_session(self,oath_key_dict):
        """Auth"""
        oath = OAuth1Session(
            oath_key_dict["consumer_key"],
            oath_key_dict["consumer_secret"],
            oath_key_dict["access_token"],
            oath_key_dict["access_token_secret"]
        )
        return oath


    def follow_probability(self,oath):
        """一定の確率でfollowする確率を求める関数

        フォロワー ** -1/20

        """

        url = 'https://api.twitter.com/1.1/users/show.json?screen_name=MedamachanBot'
        response = oath.get(url)
        json_code = json.loads(response.text)
        follow = json_code["friends_count"]
        follower = json_code["followers_count"]
        follow_probability = follow ** float(-1/5)
        follow_probability = follow_probability * 100
        if follow_probability > np.random.rand() * 100:
            status = 1
        else:
            status = 0

        return status,follow,follower

    def twitter_retweeter(self,tweets,auth):
        """特定のカテゴリに当てはまる投稿をリツイート"""
        all_amount = []
        follow_num = ""
        follower_num = ""
        oath = self.create_oath_session(auth)
        if tweets is None:
            error_message = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + ": リクエストの上限に引っかかっています\n"
            self.errorlog(error_message)
            sys.exit()
        for tweet in tweets["statuses"]:
            url = 'https://api.twitter.com/1.1/statuses/retweet/' + str(tweet['id']) + '.json' #Retweet用url
            response = oath.post(url)
            params ={'user_id' : tweet["user"]["id"]}
            retweet_res,follow_num,follower_num = self.twitter_follow_manager(params,oath)
            f = open(str(os.getcwd()) + "/action_log/" +  str(datetime.now().strftime("%Y-%m-%d")) + '.log','a+' )
            f.write("tweetID:" + str(tweet["id"]) + " " + str(response) + " UserID:" + str(tweet["user"]["id"]) + " " + str(retweet_res)+"\n")
            f.close()

        return follower_num,follow_num


    def twitter_follow_manager(self,param,oath):
        """一定の確率でfollowするメソッド"""
        probability_output,follow,follower = self.follow_probability(oath)
        if probability_output == 1:
            retweet_req = 'https://api.twitter.com/1.1/friendships/create.json'
            retweet_res = oath.post(retweet_req,params=param)
            return retweet_res,follow,follower
        else:
            return "None",follow,follower

    def twitter_searcher(self,search_word,auth):
        """Twitterから関連キーワードを取得"""
        url = "https://api.twitter.com/1.1/search/tweets.json?" #検索用url
        params = {
            "q": search_word,
            "lang": "ja",
            "result_type": "recent",
            "count": "5"
        }
        oath = self.create_oath_session(auth)
        responce = oath.get(url, params = params)
        if responce.status_code != 200:
          error_message = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + ": Error code: %d" %(responce.status_code) + "\n"
          self.errorlog(error_message)
          return None
        else:
          tweets = json.loads(responce.text)
          return tweets

    def follower_transition_log(self , follower , follow):
        follower_par_follow = follower / follow
        dataset3 = pd.DataFrame([
            [datetime.now().strftime("%Y/%m/%d/%H:%M:%S") , follower , follow ,follower_par_follow]
        ])

        with open('follwer_transition.csv', 'a') as f:
        # CSV ファイル (employee.csv) として出力
          dataset3.to_csv(f , sep = "," ,index = False , header = False)

    def errorlog(self,message):
        log_filename = str(os.getcwd()) + "/error_log/" + str(datetime.now().strftime("%Y-%m-%d")) + '.log'
        f = open(log_filename, 'a+')
        f.write(message)
        f.close()

    def transition_output(self):
        date_box = []
        follwer_transition = pd.read_csv(os.getcwd() + "/follwer_transition.csv",sep=",")
        date = np.array( list(follwer_transition['Date']) )
        follower = np.array( list(follwer_transition['follower']) )
        follow = np.array( list(follwer_transition['follow']) )
        follower_par_follow = np.array( list(follwer_transition['follower-par-follow']) )
        for d in date:
            date_split = d.split("/")
            time_split = date_split[3].split(":")
            date_box_val = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]), int(time_split[0]), int(time_split[1]), int(time_split[2]))
            date_box.append(date_box_val)
        date = np.array(date_box)

        fig = plt.figure(figsize=(15,10))
        ax1 = plt.subplot2grid((2,2), (0,0))
        ax2 = plt.subplot2grid((2,2), (0,1))
        ax3 = plt.subplot2grid((2,2), (1,0), colspan=2)

        ax1.plot(date, follow, linewidth=2,color="red")
        ax1.set_title('follow')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Transition')
        ax1.patch.set_facecolor('#2e2d2a')
        ax1.set_ylim(0,1000)
        ax1.grid(True)

        ax2.plot(date, follower, linewidth=2,color="green")
        ax2.set_title('follower')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Transition')
        ax2.patch.set_facecolor('#2e2d2a')
        ax2.set_ylim(0,1000)
        ax2.grid(True)

        ax3.plot(date, follower_par_follow, linewidth=2,color="yellow")
        ax3.set_title('Follower_par_Follow')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Transition')
        ax3.set_ylim(0,1)
        ax3.patch.set_facecolor('#2e2d2a')
        ax3.grid(True)

        filename = "./transition/output.png"
        fig.savefig(filename)

medama = MedamachanBot(CK,CS,AT,AS)
medama.main()
