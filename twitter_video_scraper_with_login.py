import requests
import json
import re
import random
import urllib.parse
#import pickle
import os
import sys
from http.cookiejar import MozillaCookieJar
from typing import Optional

##################################################################
# data to start a login request
##################################################################
# deprecate since x.com request a captcha
'''
json_onboarding_login = {
            'input_flow_data': {
                'flow_context': {
                    'debug_overrides': {},
                    'start_location': {
                        'location': 'manual_link',
                    }
                }
            },
            'subtask_versions': {
                'action_list': 2,
                'alert_dialog': 1,
                'app_download_cta': 1,
                'check_logged_in_account': 1,
                'choice_selection': 3,
                'contacts_live_sync_permission_prompt': 0,
                'cta': 7,
                'email_verification': 2,
                'end_flow': 1,
                'enter_date': 1,
                'enter_email': 2,
                'enter_password': 5,
                'enter_phone': 2,
                'enter_recaptcha': 1,
                'enter_text': 5,
                'enter_username': 2,
                'generic_urt': 3,
                'in_app_notification': 1,
                'interest_picker': 3,
                'js_instrumentation': 1,
                'menu_dialog': 1,
                'notifications_permission_prompt': 2,
                'open_account': 2,
                'open_home_timeline': 1,
                'open_link': 1,
                'phone_verification': 4,
                'privacy_options': 1,
                'security_key': 3,
                'select_avatar': 4,
                'select_banner': 2,
                'settings_list': 7,
                'show_code': 1,
                'sign_up': 2,
                'sign_up_review': 4,
                'tweet_selection_urt': 1,
                'update_users': 1,
                'upload_media': 1,
                'user_recommendations_list': 4,
                'user_recommendations_urt': 1,
                'wait_spinner': 3,
                'web_modal': 1,
            }
        }
'''
##################################################################
# variables and features to send a post details request with login
##################################################################
variables_tw_post_with_login = {
                'includePromotedContent': True,
                'with_rux_injections': False,
                'withBirdwatchNotes': True,
                'withCommunity': True,
                'withDownvotePerspective': False,
                'withQuickPromoteEligibilityTweetFields': True,
                'withReactionsMetadata': False,
                'withReactionsPerspective': False,
                'withSuperFollowsTweetFields': True,
                'withSuperFollowsUserFields': True,
                'withV2Timeline': True,
                'withVoice': True,
            }

features_tw_post_with_login = {
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': False,
                'interactive_text_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'responsive_web_enhance_cards_enabled': True,
                'responsive_web_graphql_timeline_navigation_enabled': False,
                'responsive_web_text_conversations_enabled': False,
                'responsive_web_uc_gql_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
                'tweetypie_unmention_optimization_enabled': True,
                'unified_cards_ad_metadata_container_dynamic_card_content_query_enabled': True,
                'verified_phone_label_enabled': False,
                'vibe_api_enabled': True,
                'creator_subscriptions_tweet_preview_api_enabled': True, 
                'view_counts_everywhere_api_enabled': True, 
                'longform_notetweets_inline_media_enabled': True, 
                'responsive_web_media_download_video_enabled': True, 
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': True, 
                'longform_notetweets_consumption_enabled': True, 
                'freedom_of_speech_not_reach_fetch_enabled': True, 
                'longform_notetweets_rich_text_read_enabled': True, 
                'responsive_web_twitter_article_tweet_consumption_enabled': True, 
                'tweet_awards_web_tipping_enabled': True, 
                'responsive_web_graphql_exclude_directive_enabled': True
            }

#####################################################################

class TwitterVideoScraperLogin:

    def __init__(self):
        """ Initialize """
        
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'cache-control': 'no-cache',
            'origin': 'https://x.com',
            'pragma': 'no-cache',
            'referer': 'https://x.com/',
            'sec-ch-ua': '"Chromium";v="116", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }

        self.proxies = {
            'http': '',
            'https': '',
        }

        self.tw_regex = r'https?://(?:(?:www|m(?:obile)?)\.)?(?:twitter\.com|x\.com)/(?:(?:i/web|[^/]+)/status|statuses)/(\d+)(?:/(?:video|photo)/(\d+))?'

        self.tw_session = requests.Session()
    
        self.thumbnails = []

        self.nsfw = None
        
    def set_proxies(self, http_proxy: str, https_proxy: str) -> None:
        """ set proxy  """

        self.proxies['http'] = http_proxy 
        self.proxies['https'] = https_proxy


    def get_restid_from_tw_url(self, tw_post_url: str) -> str:
        """ get post id by url """
        try:
            rest_id = re.match(self.tw_regex, tw_post_url).group(1)
            return rest_id

        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting rest id')


    def load_cookies_from_file(self, path_to_cookies: str) -> None:
        """Load the cookies from Netscape format txt file."""

        try:
            cookie_jar = MozillaCookieJar(path_to_cookies)
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            self.tw_session.cookies.update(cookie_jar)
        except FileNotFoundError as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('Cookies file not found')
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('Exception loading the cookies.')

    # deprecate since x.com request a captcha
    '''
    def get_guest_token(self) -> None:
        """ this method get the guest token, and set it in cookies session """

        guest_token_endpoint = 'https://api.x.com/1.1/guest/activate.json'
        try:
            guest_token = self.tw_session.post(guest_token_endpoint, headers=self.headers, proxies=self.proxies).json()["guest_token"]
            
            self.tw_session.cookies.set('gt', guest_token, domain='.x.com')

        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting guest token')
    '''

    # deprecate since x.com request a captcha
    '''
    def tw_login(self, username: str, password: str, cookies_path: str) -> None:
        """ this method perform the login in x/tw (get ct0 and auth_token cookies),
            this is mostly used for nsfw content, 
            if you are trying to get nsfw content, you have to login, if not u can use
            <https> without login """

        self.headers['x-guest-token'] = self.tw_session.cookies.get('gt')
        self.headers['x-twitter-active-user'] = 'yes'
        self.headers['x-twitter-client-language'] = 'en'

        # check if cookies exist
        if self.tw_cookies_exist(cookies_path):
            print('loading saved cookies')
            return
        else:
            print('login')

        onboarding_task_endpoint = 'https://api.twitter.com/1.1/onboarding/task.json'

        try:
            flow_token_1 = self.tw_session.post(f'{onboarding_task_endpoint}?flow_name=login', 
                                                headers=self.headers, 
                                                proxies=self.proxies, json=json_onboarding_login).json()['flow_token']
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting flow token 1')

        try:
            flow_token_2 = self.tw_session.post(onboarding_task_endpoint, headers=self.headers, proxies=self.proxies, json={
                'flow_token': flow_token_1,
                'subtask_inputs': [
                        {
                            'subtask_id': 'LoginJsInstrumentationSubtask',
                            'js_instrumentation': {
                                'response': '{}',
                                'link': 'next_link',
                            }
                        },
                    ]
                }).json()['flow_token']
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting flow token 2')

        try:
            flow_token_3 = self.tw_session.post(onboarding_task_endpoint, headers=self.headers, proxies=self.proxies, json={
                'flow_token': flow_token_2,
                'subtask_inputs': [
                        {
                            'subtask_id': 'LoginEnterUserIdentifierSSO',
                            'settings_list': {
                                'setting_responses': [
                                    {
                                        'key': 'user_identifier',
                                        'response_data': {
                                                'text_data': {
                                                    'result': username,
                                                }
                                        }
                                    },
                                ],
                                'link': 'next_link',
                            }
                        },
                    ]
                }).json()['flow_token']
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting flow token 3')   

        try:
            flow_token_4 = self.tw_session.post(onboarding_task_endpoint, headers=self.headers, proxies=self.proxies, json={
                    'flow_token': flow_token_3,
                    'subtask_inputs': [
                        {
                            'subtask_id': 'LoginEnterPassword',
                            'enter_password': {
                                'password': password,
                                'link': 'next_link',
                            }
                        },
                    ]
                }).json()['flow_token']
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting flow token 4')

        try:
            # get cookie auth_token
            flow_token_5 = self.tw_session.post(onboarding_task_endpoint, headers=self.headers, proxies=self.proxies, json={
                'flow_token': flow_token_4,
                'subtask_inputs': [
                        {
                            'subtask_id': 'AccountDuplicationCheck',
                            'check_logged_in_account': {
                                'link': 'AccountDuplicationCheck_false',
                            }
                        },
                    ]
                }).json()
            
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting flow token 5')

        try:
            # get cookie ct0
            flow_token_6 = self.tw_session.post(onboarding_task_endpoint, headers=self.headers, proxies=self.proxies, json={
                    'flow_token': flow_token_5,
                    'subtask_inputs': [],
                })
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting flow token 6')

        # save the cookies
        with open(cookies_path, 'wb') as f:
            pickle.dump(self.tw_session.cookies, f)

    
    def tw_cookies_exist(self, cookies_path: str) -> bool:
        """ check if cookies exist and load it"""

        if os.path.isfile(cookies_path):
            with open(cookies_path, 'rb') as f:
                self.tw_session.cookies.update(pickle.load(f))
            return True

        return False
    '''

    # deprecate since x.com request a captcha
    '''
    def tw_logout(self) -> None:
        """ this method perform the logout in x/tw """

        logout_endpoint = 'https://api.x.com/1.1/account/logout.json'

        self.headers['x-twitter-auth-type'] = 'OAuth2Session'
        self.headers['content-type'] = 'application/x-www-form-urlencoded'

        try:
            logout_api_response = self.tw_session.post(logout_endpoint, 
                                                headers=self.headers,
                                                proxies=self.proxies,
                                                data={'redirectAfterLogout': 'https://x.com/account/switch',})
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error in logout')

        try:
            logout_status = logout_api_response.json()['status']
        except:
            raise SystemExit('error in logout')

        if logout_status != 'ok':
            raise SystemExit('error in logout')
    '''

    def get_video_url_by_id_graphql(self, rest_id: str) -> tuple:
        """ this method get post details and extract video/s url 
            with best bitrate, m3u8 excluded """

        self.headers['x-csrf-token'] = self.tw_session.cookies.get('ct0')
        self.headers['x-twitter-auth-type'] = 'OAuth2Session'

        #tw_post_endpoint = 'https://x.com/i/api/graphql/zZXycP0V6H7m-2r0mOnFcA/TweetDetail' # dont work rn
        tw_post_endpoint = 'https://x.com/i/api/graphql/2ICDjqPd81tulZcYrtpTuQ/TweetResultByRestId'

        variables_tw_post_with_login['tweetId'] = rest_id

        graphql_url = f"{tw_post_endpoint}?variables={urllib.parse.quote(json.dumps(variables_tw_post_with_login))}&features={urllib.parse.quote(json.dumps(features_tw_post_with_login))}"

        try:
            post_details = self.tw_session.get(graphql_url, headers=self.headers, proxies=self.proxies).json()

        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting post details')   

        # videos, but u have all tweet data in post_details
        #print(post_details)
        try:

            all_media = post_details['data']['tweetResult']['result']['tweet']['legacy']['entities']['media']
            
            nsfw = post_details['data']['tweetResult']['result']['tweet']['legacy']['possibly_sensitive']
        
        except Exception as e:
            print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
            raise SystemExit('error getting video details') 

        video_variants_list = []
        video_thumbnails = []
        for media in all_media:
            if 'video_info' in media:
                video_variants_list.append(media['video_info']['variants'])

            # thumbnails
            video_thumbnails.append(media['media_url_https'])

        videos_urls = []
        if video_variants_list:
            for video_variants in video_variants_list:
                video_best_bitrate = max( video_variants, key= lambda video_bitrate:video_bitrate['bitrate'] if 'bitrate' in video_bitrate else 0 ) # without m3u8
                videos_urls.append(video_best_bitrate['url'])
        else:
            raise SystemExit('no video found')

        return videos_urls, video_thumbnails, nsfw


    def download(self, video_url_list: list) -> list:
        """ download the video """

        downloaded_video_list = []
        for video_url in video_url_list:
            try:
                video = self.tw_session.get(video_url, headers=self.headers, proxies=self.proxies, stream=True)

            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error downloading video')

            path_filename = video_url.split('?')[0].split('/')[-1]
            try:
                with open(path_filename, 'wb') as f:
                    for chunk in video.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()

                downloaded_video_list.append(path_filename)
            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error writting video')   

        return downloaded_video_list

    """
    # not used for now. x/tw is delivering the video with the correct format
    
    def ffmpeg_fix(self, downloaded_video_list: list) -> list:

        fixed_video_list = []
        for video in downloaded_video_list:
            # this is a prefix for new features
            final_video_name = f'DescargarBot_{video}'

            ffmpeg_cmd = f'ffmpeg -hide_banner -loglevel panic -y -i "{video}" -c copy "{final_video_name}"'

            try:
                # perform fix
                os.system(ffmpeg_cmd)

                # delete tmp files
                os.system(f'rm {video}')

                fixed_video_list.append(final_video_name)
            except Exception as e:
                print(e, "\nError on line {}".format(sys.exc_info()[-1].tb_lineno))
                raise SystemExit('error with ffmpeg')

        return fixed_video_list
    """

    def get_video_filesize(self, video_url_list: list) -> list:
        """ get file size of requested video """

        items_filesize = []
        for video_url in video_url_list:
            video_size = self.get_content_length(video_url)

            if video_size == None:
                raise SystemExit('error getting video size')

            items_filesize.append(video_size/1024/1024)

        return items_filesize
    
    def get_content_length(self, url: str) -> Optional[int]:
        headers = {'user-agent': 'Twitterbot/1.0'}
        
        for attempt in range(50):
            try:
                resp_head = requests.head(url, headers=headers, allow_redirects=True)
                if 'content-length' in resp_head.headers:
                    return int(resp_head.headers['content-length'])
                
                with requests.get(url, headers={**headers, 'Range': 'bytes=0-0'}, stream=True) as resp_get:
                    if 'Content-Length' in resp_get.headers:
                        return int(resp_get.headers['Content-Length'])
                    
                    resp_full = requests.get(url, headers=headers, stream=True)
                    resp_full.close()
                    return int(resp_full.headers.get('Content-Length', 0))
                    
            except (requests.RequestException, KeyError, ValueError) as e:
                print(f"retrie {attempt + 1} fail: {str(e)}")
                time.sleep(1)
        
        return None

##################################################################

if __name__ == "__main__":

    # use case example

    # set x/tw video url
    x_url_post = ''

    if x_url_post == '':
        args = sys.argv[1:]
        if '--cookies' != args[0]:
            print("error. try:\npython3 twitter_video_scraper_with_login.py --cookies PATH_TO_COOKIES_FILE TWITTER_URL")
            exit()
        cookies_path = args[1]
        x_url_post = args[2]
    else:
        cookies_path = 'tw_cookies.txt'

    # create scraper video object
    tw_video = TwitterVideoScraperLogin()

    # set the proxy (optional, u can run it with ur own ip),
    #tw_video.set_proxies('', '')

    # get post id from url
    restid = tw_video.get_restid_from_tw_url(x_url_post)

    # get guest token, set it in cookies
    #tw_video.get_guest_token()

    # perform login(deprecate)
    #tw_video.tw_login(username, password, cookies_path)


    tw_video.load_cookies_from_file(cookies_path)

    # get video url and thumbnails from video id
    video_url_list, video_thumbnails, video_nsfw = tw_video.get_video_url_by_id_graphql(restid)

    # perform logout (deprecate)
    #tw_video.tw_logout()

    # get the videos filesize
    items_filesize = tw_video.get_video_filesize(video_url_list)
    [print('filesize: ~' + str(filesize) + ' bytes') for filesize in items_filesize]

    # download video by url
    downloaded_video_list = tw_video.download(video_url_list)

    # not used for now. x/tw is delivering the video with the correct format
    # remember install ffmpeg if u dont have it
    # fixed_video_list = tw_video.ffmpeg_fix(downloaded_video_list)

    tw_video.tw_session.close()
