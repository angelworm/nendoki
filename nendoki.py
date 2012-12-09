# -*- coding: utf-8 -*-
import os
import sys
import tweepy
import ConfigParser
from logging import * 
import webbrowser

# function set(i) { document.forms[4][0].value = "ねんどき公社"; document.forms[4][1].value = "nendoki+"+i+"@gmail.com"; document.forms[4][2].value = "oxbow48@click";document.forms[4].submit();};set("021")

class Nendoki:
    def __init__(self):
        info("reading settings.ini.")
        cp = ConfigParser.SafeConfigParser()
        cf = os.path.join(os.path.dirname(__file__), "settings.ini")
        try:
            fp = open(cf, "r")
            cp.readfp(fp)
            fp.close()
        except IOError, x:
            critical("initialize failed")
            info("you didn't make settings.ini?")
            raise IOError, x
        
        self.consumer_key = cp.get("Tool Infomation", "consumer_key")
        self.consumer_key_secret = \
            cp.get("Tool Infomation", "consumer_key_secret")

        self.apis = []
        for k,s in cp.items("Accounts"):
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_key_secret)
            auth.set_access_token(k, s)
            self.apis.append(tweepy.API(auth_handler=auth))
        info("done")
        self._make_apis()

    def _bind_api(self, api):
        def _call(account_range, *args, **keywords):
            ret = []
            e = [] 
            for i in account_range:
                try:
                    ret.append(api(self.apis[i], *args, **keywords))
                except TweepError, x:
                    e.append(x)
            if len(e) == 0:
                return ret
            else:
                raise TweepError, e
        return _call

    def _make_apis(self):
        self.home_timeline = self._bind_api(tweepy.API.home_timeline)
        self.friends_timeline = self._bind_api(tweepy.API.friends_timeline)
        self.user_timeline = self._bind_api(tweepy.API.user_timeline)
        self.mentions = self._bind_api(tweepy.API.mentions)
        self.retweeted_by_user = self._bind_api(tweepy.API.retweeted_by_user)
        self.retweeted_by = self._bind_api(tweepy.API.retweeted_by)
        self.related_results = self._bind_api(tweepy.API.related_results)
        self.retweeted_by_ids = self._bind_api(tweepy.API.retweeted_by_ids)
        self.retweeted_by_me = self._bind_api(tweepy.API.retweeted_by_me)
        self.retweeted_to_me = self._bind_api(tweepy.API.retweeted_to_me)
        self.retweeted_by_user = self._bind_api(tweepy.API.retweeted_by_user)
        self.retweets_of_me = self._bind_api(tweepy.API.retweets_of_me)
        self.get_status = self._bind_api(tweepy.API.get_status)
        self.update_status = self._bind_api(tweepy.API.update_status)
        self.destroy_status = self._bind_api(tweepy.API.destroy_status)
        self.retweet = self._bind_api(tweepy.API.retweet)
        self.retweets = self._bind_api(tweepy.API.retweets)
        self.get_user = self._bind_api(tweepy.API.get_user)
        self._lookup_users = self._bind_api(tweepy.API._lookup_users)
        self.search_users = self._bind_api(tweepy.API.search_users)
        self.friends = self._bind_api(tweepy.API.friends)
        self.followers = self._bind_api(tweepy.API.followers)
        self.direct_messages = self._bind_api(tweepy.API.direct_messages)
        self.get_direct_message = self._bind_api(tweepy.API.get_direct_message)
        self.sent_direct_messages = self._bind_api(tweepy.API.sent_direct_messages)
        self.send_direct_message = self._bind_api(tweepy.API.send_direct_message)
        self.destroy_direct_message = self._bind_api(tweepy.API.destroy_direct_message)
        self.create_friendship = self._bind_api(tweepy.API.create_friendship)
        self.destroy_friendship = self._bind_api(tweepy.API.destroy_friendship)
        self.exists_friendship = self._bind_api(tweepy.API.exists_friendship)
        self.show_friendship = self._bind_api(tweepy.API.show_friendship)
        self._lookup_friendships = self._bind_api(tweepy.API._lookup_friendships)
        self.friends_ids = self._bind_api(tweepy.API.friends_ids)
        self.friendships_incoming = self._bind_api(tweepy.API.friendships_incoming)
        self.friendships_outgoing = self._bind_api(tweepy.API.friendships_outgoing)
        self.followers_ids = self._bind_api(tweepy.API.followers_ids)
        self.rate_limit_status = self._bind_api(tweepy.API.rate_limit_status)
        self.set_delivery_device = self._bind_api(tweepy.API.set_delivery_device)
        self.update_profile_colors = self._bind_api(tweepy.API.update_profile_colors)
        self.update_profile = self._bind_api(tweepy.API.update_profile)
        self.favorites = self._bind_api(tweepy.API.favorites)
        self.create_favorite = self._bind_api(tweepy.API.create_favorite)
        self.destroy_favorite = self._bind_api(tweepy.API.destroy_favorite)
        self.enable_notifications = self._bind_api(tweepy.API.enable_notifications)
        self.disable_notifications = self._bind_api(tweepy.API.disable_notifications)
        self.create_block = self._bind_api(tweepy.API.create_block)
        self.destroy_block = self._bind_api(tweepy.API.destroy_block)
        self.blocks = self._bind_api(tweepy.API.blocks)
        self.blocks_ids = self._bind_api(tweepy.API.blocks_ids)
        self.report_spam = self._bind_api(tweepy.API.report_spam)
        self.saved_searches = self._bind_api(tweepy.API.saved_searches)
        self.get_saved_search = self._bind_api(tweepy.API.get_saved_search)
        self.create_saved_search = self._bind_api(tweepy.API.create_saved_search)
        self.destroy_saved_search = self._bind_api(tweepy.API.destroy_saved_search)
        self.lists = self._bind_api(tweepy.API.lists)
        self.lists_memberships = self._bind_api(tweepy.API.lists_memberships)
        self.lists_subscriptions = self._bind_api(tweepy.API.lists_subscriptions)
        self.list_timeline = self._bind_api(tweepy.API.list_timeline)
        self.get_list = self._bind_api(tweepy.API.get_list)
        self.list_members = self._bind_api(tweepy.API.list_members)
        self.subscribe_list = self._bind_api(tweepy.API.subscribe_list)
        self.unsubscribe_list = self._bind_api(tweepy.API.unsubscribe_list)
        self.list_subscribers = self._bind_api(tweepy.API.list_subscribers)
        self.trends_available = self._bind_api(tweepy.API.trends_available)
        self.trends_location = self._bind_api(tweepy.API.trends_location)
        self.search = self._bind_api(tweepy.API.search)
        self.trends_daily = self._bind_api(tweepy.API.trends_daily)
        self.trends_weekly = self._bind_api(tweepy.API.trends_weekly)
        self.reverse_geocode = self._bind_api(tweepy.API.reverse_geocode)
        self.nearby_places = self._bind_api(tweepy.API.nearby_places)
        self.geo_id = self._bind_api(tweepy.API.geo_id)
        self.geo_search = self._bind_api(tweepy.API.geo_search)
        #self.geo_similar_places = self._bind_api(tweepy.API.geo_similar_places)

    def requestAccessToken(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_key_secret)

        info("requesting pin code.")
        webbrowser.open(auth.get_authorization_url())
        pin = raw_input('enter pin code: ').strip()
        token = auth.get_access_token(verifier=pin)
        
        info("writing into settings file.")
        try:
            fp = open("settings.ini", "a")
            fp.write("%s=%s\n" % (token.key, token.secret))
        except IOError,x:
            critical("failed to write into settings file: %s",x)
        finally:
            fp.close()

        auth.set_access_token(token.key, token.secret)
        self.apis.append(tweepy.API(auth_handler=auth))

        info("done")
        
