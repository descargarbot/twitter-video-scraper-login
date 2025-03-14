# x / twitter video scraper with cookies
<div align="center">
  
![DescargarBot](https://www.descargarbot.com/v/download-github_twitter.png)
  
[![Reddit](https://img.shields.io/badge/on-descargarbot?logo=github&label=status&color=green
)](https://github.com/descargarbot/twitter-video-scraper-login/issues "Twitter with login")
</div>

<h2>dependencies</h2>
<code>Python 3.9+</code>
<code>requests</code>
<br>
<br>
<h2>install dependencies</h2>
<ul>
<li><h3>requests</h3></li>
  <code>pip install requests</code><br>
  <code>pip install -U 'requests[socks]'</code>
  <br>
<br>
</ul>
<br>
  
  > [!NOTE]\
  >  To get the cookies file you can use <a href="https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc" > this</a> browser extension
  <br><br>

<h2>use case example</h2>

    #import the class TwitterVideoScraperLogin
    from twitter_video_scraper_with_login import TwitterVideoScraperLogin
    
    # set x/tw video url
    x_url_post = 'your x/twitter video url'

    cookies_path = 'tw_cookies.txt'

    # create scraper video object
    tw_video = TwitterVideoScraperLogin()

    # set the proxy (optional, u can run it with ur own ip),
    #tw_video.set_proxies('', '')

    # get post id from url
    restid = tw_video.get_restid_from_tw_url(x_url_post)

    # get guest token, set it in cookies(deprecate)
    #tw_video.get_guest_token()

    # perform login(deprecate)
    #tw_video.tw_login(username, password, cookies_path)

    tw_video.load_cookies_from_file(cookies_path)

    # get video url and thumbnails from video id
    video_url_list, video_thumbnails, video_nsfw = tw_video.get_video_url_by_id_graphql(restid)

    # perform logout (deprecate)
    #tw_video.tw_logout()

    # get the videos filesize
    #items_filesize = tw_video.get_video_filesize(video_url_list)
    #[print('filesize: ~' + str(filesize) + ' bytes') for filesize in items_filesize]

    # download video by url
    downloaded_video_list = tw_video.download(video_url_list)

    tw_video.tw_session.close()

    
  > [!NOTE]\
  >  you can use the CLI
  <br><br>
  > <code>python3 twitter_video_scraper_with_login.py --cookies PATH_TO_COOKIES_FILE TWITTER_URL</code>
<br><br>

> [!WARNING]\
> Accounts used with the scraper are quite susceptible to suspension. <b>Do not use your personal account</b>.
<br>
<h2>online</h2>
<ul>
  ⤵
  <li> web 🤖 <a href="https://descargarbot.com" >  DescargarBot.com</a></li>
  <li> <a href="https://t.me/xDescargarBot" > Telegram Bot 🤖 </a></li>
  <li> <a href="https://discord.gg/gcFVruyjeQ" > Discord Bot 🤖 </a></li>
</ul>

