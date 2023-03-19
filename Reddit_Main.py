import requests
import requests.auth
import time #used for time delay as of right now

rp_file = open("rp_info.txt") #reddit password
rp_content = rp_file.read()
rp_file.close()

sc_file = open("sc_info.txt") #client secret id     
sc_content = sc_file.read()
sc_file.close()

Content = {
    "Secret_ID" : sc_content,
    "Client_ID" : "1XJr1EkenwbFksMXKbDHxQ",
    "Username" : "Starlegendgod",
    "R_Password" : rp_content
}

client_auth = requests.auth.HTTPBasicAuth(Content["Client_ID"],Content["Secret_ID"])

post_data = {
    "grant_type" : "password",
    "username" : "Starlegendgod", 
    "password" : rp_content
}

headers = {"User-Agent": "TestClient by Starlegendgod"}

response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers) #creation of token for use

token_content = response.json()

auth_content = "{0} {1}".format(token_content["token_type"],token_content["access_token"])


headers = {"Authorization": auth_content, "User-Agent": "TestClient by Starlegendgod"}

response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)


def hot_search(): #this function used to find the current most active posts recently added to the hot section(default settings)
    subreddit_input = input("put your sub to see if it exist\n\ntype here -> ")
    req_link = "https://oauth.reddit.com/r/{0}/hot".format(subreddit_input)
    res = requests.get(req_link, headers=headers,params={'limit' : 10})
    print(res.json())
    if res.json().get("message") == "Bad Request" or res.json().get("error") == 404:
        print("seems like the subreddit is no longer available or an Error has occured..Type up a new one!")
        time.sleep(2)
        hot_search()
    elif res.json()["data"]["children"]:
        print(res.json())
        print("Alright here is some Active topics for {0} subreddit currently\n--------------------------------".format(subreddit_input))
        for mini_post in res.json()["data"]["children"]:
            print(mini_post["data"]["title"]+"\n")
    else: 
        print("Doesn't seem that {0} exist on reddit let's try again!".format(subreddit_input))
        time.sleep(2)
        hot_search()

hot_search()