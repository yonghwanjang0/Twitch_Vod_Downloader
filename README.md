# Twitch_Vod_Downloader
This code is for downloading twitch vod files. 

This source code makes for windows 10. 

## Use
1. Open the option dialog (F10), set 'Finally File Save Folder' and 'Temporary Files Save Folder'. (If you have set it up before, you can skip this step.)

2. Twitch vod full url (e.g : https://www.twitch.tv/videos/42348230) or Vod ID (e.g : 42348230) input to url field box. 
(You possible use keyboard 'button 1' to shortcut url field box.)

3. Click 'Check Vod (C)' button. 
(If the streamer has set the subscriber-only option to the vod, download isn't possible.)

4. If found vod information, click 'Download Start (F2)' button.
(If there is not enough free disk space, the download will not start.)

5. Wait to the Download Finish. (The Downloader will download vod stream files and merge it into a single video file.) (If you want to lock the download status, use the Download Status Lock (Ctrl + Q). (You won't be able to click Download Stop button.))

6. File download finished.

## ScreenShot
<img src="https://user-images.githubusercontent.com/83168104/146208543-2ca7f494-bfbd-42a5-9e15-cc9bb337824e.png">
<img src="https://user-images.githubusercontent.com/83168104/146045673-a5ba84b1-b4ff-4079-a975-5a027761283c.png">

## requirements
* PySide6
* pytz
* tzlocal
* m3u8 
