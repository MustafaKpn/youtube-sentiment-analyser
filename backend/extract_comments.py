

import sys
import json
import yt_dlp


def extract_comments(video_url):
    ydl_opts = {
        'skip_download': True,
        'getcomments': True,
        'quiet': False,
        'no_warnings': True
    }

    if "&list" in video_url:
        video_url = video_url[:video_url.find('&list')]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)


    video_data = {
        'video_id': info.get('id'),
        'title': info.get('title'),
        'channel': info.get('channel'),
        'view_count': info.get('view_count'),
        'like_count': info.get('like_count'),
        'upload_date': info.get('upload_date'),
        'comments': []
    }

    if info['comments']:
        for k in info['comments']:
            comment = {
                "text": k.get("text"),
                "author": k.get("author"),
                "like_count": k.get("like_count", 0),
                "timestamp": k.get("timestamp")
            }
            video_data["comments"].append(comment)  

    return video_data






if __name__ == "__main__":
    import time

    url = "https://www.youtube.com/watch?v=rpiv-iooqu8&list=RDrpiv-iooqu8&start_radio=1"
    start_time = time.time()
    
    data = extract_comments(url)
    
    elapsed = time.time() - start_time
    rate = len(data['comments']) / elapsed if elapsed > 0 else 0
    
    print(f"\n✓ Performance:")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Rate: {rate:.1f} comments/sec")
    with open(f"comments_{data["video_id"]}.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)   
