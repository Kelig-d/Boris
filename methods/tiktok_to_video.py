import urllib.request
from TikTokApi import TikTokApi

def TiktokToVideo(link):
    api = TikTokApi.get_instance()

    tiktok = api.get_tiktok_by_url(url=link, custom_verifyFp="verify_ky2rdaop_V2qTzwqt_UDBs_4APu_81Cm_U8Qi5aXVKGSG")
    link = tiktok["itemInfo"]["itemStruct"]["video"]["downloadAddr"]
    urllib.request.urlretrieve(link, 'videos/tiktok.mp4')