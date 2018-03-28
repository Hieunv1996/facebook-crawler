import configuration
import requests
import json
import traceback

BASE_URL = "https://graph.facebook.com/v2.11/"

GET_POST_URL = BASE_URL + configuration.GROUP_ID + "/feed?access_token=" + configuration.ACCESS_TOKEN


def run():
    posts_text = requests.get(GET_POST_URL).text
    while posts_text:
        posts_json = json.loads(posts_text, encoding='utf-8')
        posts = posts_json.get('data')
        for post in posts:
            post_message = post.get('message')
            if post_message:
                print("POST: " + post_message)
            post_id = post.get('id')
            comment_url = BASE_URL + str(post_id) + "/comments?access_token=" + configuration.ACCESS_TOKEN
            comments_text = requests.get(comment_url).text
            while comments_text:
                comments_json = json.loads(comments_text, encoding='utf-8')
                comments = comments_json.get('data')
                index = 0
                for comment in comments:
                    comment_message = comment.get('message')
                    if comment_message:
                        print(index, comment_message)
                        index += 1
                try:
                    comment_url = comments_json.get('paging').get('next')
                    comments_text = requests.get(comment_url).text
                except:
                    comments_text = None
        try:
            next_page_url = posts_json.get('paging').get('next')
            posts_text = requests.get(next_page_url).text
        except:
            traceback.print_exc()
            exit(0)


if __name__ == '__main__':
    run()
