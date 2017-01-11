import networkx as nx
from pymongo import MongoClient

import copy

def ConnectDB(db, table):
    host = 'mongodb://mongo:123456@222.197.180.150'
    try:
        cursor = MongoClient(host).\
            get_database(db).\
            get_collection(table)
    except:
        raise "Oho"
    return cursor

# 创建数据库链接和创建图

tweet_cr = ConnectDB('election_data', 'unique_tweet')
favoriter_cr = ConnectDB('election_data', 'favoriters_ids')
retweet_cr = ConnectDB('election_data', 'retweeters_ids')
conversation_cr = ConnectDB('election_data', 'conversation_tweet')
user_cr = ConnectDB('twitter_user_tweet', 'user')

number_of_tweets = 1000

# 网络数据

g = nx.DiGraph()

cnt = 0

error = 0
# 基于 Tweet 的网络
try:
    for tweet in tweet_cr.find().limit(1500):

        cnt += 1
        if cnt % 100 == 0:
            print('Processing...  %d/%d'%(cnt,number_of_tweets))

        try:
            if 'id' not in tweet.keys() or 'account_id' not in tweet.keys():
                error += 1
                continue

            # 保存 Tweet 信息
            tweet_id = tweet['id']
            g.add_node(tweet_id, category='tweet')
            g.add_node(tweet['account_id'], category='user')
            g.add_edge(tweet['account_id'], tweet_id, category='publish')

            # 点赞参与
            favorite = favoriter_cr.find_one({'id': tweet_id})
            if favorite and 'favorited_ids' in favorite.keys():
                for user in favorite['favorited_ids']:
                    g.add_node(user, category='user')
                    g.add_edge(tweet_id, user, category='favorite')


            # 评论参与
            if 'conversation_count' in tweet.keys() and tweet['conversation_count'] > 0:
                for con_id in tweet['conversation_ids']:
                    con = conversation_cr.find_one({'id': con_id})
                    if con:
                        user = con['account_id']
                        g.add_node(user, category='user')
                        g.add_edge(tweet_id, user, category='conversation')

            # 转发参与
            retweet = retweet_cr.find_one({'tweet_id': tweet_id},{'ids':1})
            if retweet and 'ids' in retweet.keys():
                for user in retweet['ids']:
                    user = con['account_id']
                    g.add_node(user, category='user')
                    g.add_edge(tweet_id, user, category='retweeted')
                    g.add_edge(user, tweet_id, category='retweet')


            # 保存文件
            if cnt % 100 == 0:
                tg = copy.deepcopy(g)
                # 保存原始网络
                nx.write_gexf(tg, './result/tweet_%d.gexf' % cnt)
                # 保存删去冗余节点（出度为0）的网络
                nodes = [n for n, d in tg.out_degree_iter() if d == 0]
                tg.remove_nodes_from(nodes)
                nx.write_gexf(tg, './result/tweet_%d_without_0_outer.gexf' % cnt)

        except:
            continue
except:
    print('ERROR')



# 基于人物的网络



# 保存原始网络
nx.write_gexf(g, './result/tweet_%d.gexf'%cnt)

# 保存删去冗余节点（出度为0）的网络

nodes = [n for n, d in g.out_degree_iter() if d == 0]

g.remove_nodes_from(nodes)

nx.write_gexf(g, './result/tweet_%d_without_0_outer.gexf'%cnt)



# users = g.nodes()
# users_set = set(users)
# for n in users:
#     user_info = user_cr.find_one({'account_id':n}, {'friends_ids':1,'followers_ids':1})
#     if user_info:
#         for friend in user_info['friends_ids']:
#             if friend in users_set:
#                 g.add_edge(friend, n, category='follow')
#         for follower in user_info['followers_ids']:
#             if follower in users_set:
#                 g.add_edge(n, follower, category='follow')

