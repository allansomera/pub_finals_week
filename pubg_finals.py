import os
from selenium import webdriver
import time

# from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import re
from tqdm import tqdm

driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://pgs.pubgrank.org/#leaderboard"
driver.get(url)


playerlist = []
matchlist = []
kills = []
dmglist = []
knocklist = []
assist = []

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='result']/div/div[2]/div/a[2]"))
).click()


for x in tqdm(range(1, 65)):
    playerres = driver.find_elements(
        By.XPATH,
        "//*[@id='player_stats']/div/div[3]/div/table/tbody/tr[%d]/td[2]/div/a" % x,
    )
    playerlist.append(playerres[0].text)
    # print(playerres[0].text)

    matchres = driver.find_elements(
        By.XPATH, "//*[@id='player_stats']/div/div[3]/div/table/tbody/tr[%s]/td[3]" % x
    )
    matchlist.append(matchres[0].text)

    killres = driver.find_elements(
        By.XPATH, "//*[@id='player_stats']/div/div[3]/div/table/tbody/tr[%s]/td[4]" % x
    )
    kills.append(killres[0].text)

    dmgres = driver.find_elements(
        By.XPATH, "//*[@id='player_stats']/div/div[3]/div/table/tbody/tr[%s]/td[5]" % x
    )
    dmglist.append(dmgres[0].text)

    knockres = driver.find_elements(
        By.XPATH, "//*[@id='player_stats']/div/div[3]/div/table/tbody/tr[%s]/td[6]" % x
    )
    knocklist.append(knockres[0].text)

    assistres = driver.find_elements(
        By.XPATH, "//*[@id='player_stats']/div/div[3]/div/table/tbody/tr[%s]/td[7]" % x
    )
    assist.append(assistres[0].text)

print("DONE")
df = pd.DataFrame(data=playerlist, columns=["Player"])

df["Match"] = matchlist
df["Kills"] = kills
df["Damage"] = dmglist
df["Knocks"] = knocklist
df["Assist"] = assist

df["Player"] = df["Player"].astype("str")
df["Match"] = df["Match"].apply(pd.to_numeric, errors="coerce")
df["Kills"] = df["Kills"].apply(pd.to_numeric, errors="coerce")
df["Damage"] = df["Damage"].apply(pd.to_numeric, errors="coerce")
df["Knocks"] = df["Knocks"].apply(pd.to_numeric, errors="coerce")
df["Assist"] = df["Assist"].apply(pd.to_numeric, errors="coerce")

# df.sort_values(by=["Damage"], ascending=False)
df2_name = df.sort_values(by=["Player"], ascending=True)
df2_name["Team"] = (
    df2_name.Player.str.extract(r"(([\w]+)(?=_))", expand=True).astype(str).iloc[:, [1]]
)
dff = df2_name.loc[df2_name.Match == 20, :]
df3 = dff.groupby("Team")

for _, group in df3:
    print(group.sort_values(by=["Damage"], ascending=True).iloc[:, :])
    print("TOTAL KILLS: %d\n" % (group["Kills"].sum()))
