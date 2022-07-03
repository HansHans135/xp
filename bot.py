import datetime
import discord
import json
import random
import os
import random, string
import requests


      
print("#############################")
print("##請著名來源,亨哥保有解釋權力##")
print("#############################")


#設定
with open ("config.json",mode="r",encoding="utf-8") as filt:
    data = json.load(filt)
PREFIX = data["prefix"]
op_id = data["owner_id"]
TOKEN = data["token"]
V_NOW = "1.2"


r=requests.get('https://raw.githubusercontent.com/HansHans135/xp/main/now.json')
V_GET = r.json()
V_NEW = V_GET["v"]

client = discord.Client()

@client.event   
async def on_ready():
    print("版本檢查中...")
    if V_NOW == V_NEW:
        print(f"版本檢查完成\n目前為最新版本:{V_NEW}")
    else:
        print(f"目前不是最新版本\n是否需要下載更新?[y/n]\n(目前:{V_NOW},最新:{V_NEW})")
        i = 1
        while i == 1:
            a = input("你的選擇[y/n]:")
            if a == "y" or a == "n":
                if a == "y":
                    print("下載中...")
                    url = "https://raw.githubusercontent.com/HansHans135/xp/main/bot.py"
                    myfile = requests.get(url)
                    open('bot.py', 'wb').write(myfile.content)
                    print(f"下載完成!!重啟`bot.py`即可生效")
                    i = 0
                if a == "n":
                    print(f"已取消下載")
                    i = 0
            else:
                print("請輸入正確的回答")
            
        print(f"版本檢查完成\n目前:{V_NOW},最新:{V_NEW}")
        
    print('機器人已啟動，目前使用的bot：',client.user)
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
    await client.change_presence(status= status_w, activity=activity_w)
    
@client.event
async def on_message(message):
#help
    if message.content == f"{PREFIX}help":
        await message.delete()
        embed = discord.Embed(title="指令清單", description=f"前輟是[{PREFIX}]", color=0x04f108)
        embed.add_field(name=f"{PREFIX}help", value="操作手冊")
        embed.add_field(name=f"{PREFIX}info", value="關於")
        embed.add_field(name=f"{PREFIX}oc", value="開啟/關閉功能(預設為關閉,第一次設定會自動開啟)")
        embed.add_field(name=f"{PREFIX}start <通知訊息發送頻道id(若為0將會發送到預設的頻道)> <多少訊息上升一等>", value="設定")
        embed.add_field(name=f"{PREFIX}me", value="看你的等級和訊息量")
        embed.add_field(name=f"{PREFIX}xp id", value="看別人的資料")
        embed.add_field(name=f"{PREFIX}set id", value="將指定id等級紀錄歸零")
        embed.add_field(name=f"{PREFIX}up", value="檢查版本")
        await message.channel.send(content=None, embed=embed)

    #info
    if message.content == f"{PREFIX}info":
        await message.delete()
        embed = discord.Embed(title="關於", description=f"前輟是{PREFIX}", color=0x04f108)
        embed.add_field(name="目前版本", value=f"v {V_NOW}")
        embed.add_field(name="關於此機器人:", value="來自開源: https://github.com/HansHans135/xp")
        await message.channel.send(content=None, embed=embed)

#start
    if message.content.startswith(f'{PREFIX}start'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            tmp = message.content.split(" ",2)
            CL = tmp[1]
            tmp = message.content.split(f"{CL} ",2)
            msg = tmp[1]
            filepath = f"data/{message.guild.id}/config.json"
            if os.path.isfile(filepath):
                with open (f"data/{message.guild.id}/config.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                data["cl"] = int(CL)
                data["msg"] = int(msg)
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                if CL == "0":
                    cls = "預設"
                else:
                    cls = f"<#{CL}>"
                await message.channel.send(f"{message.author.mention}設定完成!\n目前設定:\n\n提示頻道: {cls}\n升級所需訊息數: {msg}")
            else:
                os.mkdir(f"data/{message.guild.id}")
                if CL == "0":
                    cls = "預設"
                else:
                    cls = f"<#{CL}>"
                data = {"cl":CL,"msg":msg,"open":"1"}
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                    await message.channel.send(f"{message.author.mention}設定完成!\n目前設定:\n\n提示頻道: {cls}\n升級所需訊息數: {msg}")
        else:
            await message.channel.send(f"{message.author.mention}你需要有管理權限才能設定")

    if message.content == f"{PREFIX}me":
        with open (f"data/{message.guild.id}/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}\n你目前等級:`{data['now']}`\n說話的次數:`{data['msg']}`")

    if message.content.startswith(f'{PREFIX}xp'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("你查誰的xp？")
      else:
        with open (f"data/{message.guild.id}/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}id`{tmp[1]}`\n他目前等級:`{data['now']}`\n說話的次數:`{data['msg']}`")

    #set
    if message.content.startswith(f'{PREFIX}set'):
        if message.author.guild_permissions.manage_messages:
          await message.delete()
          tmp = message.content.split(" ",2)
          崁入一 = tmp[1]
          #亨哥0126
          if len(tmp) == 1:
            await message.channel.send(f"格式:{PREFIX}set id")
          else:
              filepath = f"data/{message.guild.id}/{message.author.id}.json"
              with open (f"data/{message.guild.id}/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
              data["msg"] = 0
              data["now"] = 0
              if os.path.isfile(filepath):
                with open (f"data/{message.guild.id}/{崁入一}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                await message.channel.send(f"已將id:`{崁入一}`等級紀錄歸零")
              else:
                await message.channel.send(f"找不到關於id:`{崁入一}`的紀錄")
        else:
            await message.channel.send(f"{message.author.mention}你沒有權限")

    if message.content == f"{PREFIX}oc":
        if message.author.guild_permissions.manage_messages:
            with open (f"data/{message.guild.id}/config.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            if data["open"] == "1":
                data["open"] = "0"
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    data = json.dump(data,filt)
                await message.channel.send(f"{message.author.mention}已`關閉`等級功能")
            else:
                data["open"] = "1"
                with open (f"data/{message.guild.id}/config.json",mode="w",encoding="utf-8") as filt:
                    data = json.dump(data,filt)
                await message.channel.send(f"{message.author.mention}已`開啟`等級功能")

    if message.author.bot:
        return
    else:
        filepath = f"data/{message.guild.id}/config.json"
        if os.path.isfile(filepath):
            with open (f"data/{message.guild.id}/config.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
                up_msg = data["msg"]
                up_cl = data["cl"]
            if data["open"] == "1":
                filepath = f"data/{message.guild.id}/{message.author.id}.json"
                if os.path.isfile(filepath):
                    with open (f"data/{message.guild.id}/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                        data = json.load(filt)
                    next_msg = int(data["msg"]) + 1
                    IF_msg = int(next_msg) // int(up_msg)
                    if int(IF_msg) > int(data["now"]):
                        up = int(data["now"]) + 1
                        data["msg"] = next_msg
                        data["now"] = int(IF_msg)
                        with open (f"data/{message.guild.id}/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                            data = json.dump(data,filt)
                        if up_cl == 0:
                            await message.channel.send(f"{message.author.mention}恭喜你升級到`{up}`等")
                        else:
                            channel = client.get_channel(int(up_cl))
                            await channel.send(f"{message.author.mention} 恭喜你升級到`{up}`等")
                    else:
                        next_msg = int(data["msg"]) + 1
                        data["msg"] = next_msg
                        with open (f"data/{message.guild.id}/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                            data = json.dump(data,filt)
                else:
                    with open (f"data/{message.guild.id}/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                        data = {"msg":"1","now":"0"}
                        data = json.dump(data,filt)
            

client.run(TOKEN)