# from smartWebsocket import SmartWebSocket
from datetime import datetime, timedelta
from SmartApi import SmartConnect 
import pyotp
from logzero import logger
from StoreFile import token_holding_mapping_quant, token_holding_mapping_icici_prudential_smallcap, token_holding_mapping_nippon, token_holding_mapping_aditya,token_holding_mapping_quant_infra, token_holding_mapping_icici_bharat
import time
import progressbar
import telegram
import asyncio

apikey = 'uXnhCf8U'
CLIENT_CODE="A56859739"
TOTP_STRING = "PXKPG7GG42Q3S2DE4CU7NPS63Y"
pwd = '9086'
telebotApiKey = "6634396698:AAGDX_xG-0dcl4Guv548_BldaATYgOIGILQ"
telegramChannelId = "-1002041066723"

smartApi = SmartConnect(apikey)
totp = pyotp.TOTP(TOTP_STRING).now()

data = smartApi.generateSession(CLIENT_CODE, pwd, totp)
refreshToken= data['data']['refreshToken']
Authorizationt_TOKEN = data['data']['jwtToken']
FEED_TOKEN = smartApi.getfeedToken()

userProfile= smartApi.getProfile(refreshToken)
today = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')

headers = {
  'X-PrivateKey': apikey,
  'Accept': 'application/json',
  'X-SourceID': 'WEB',
  'X-ClientLocalIP': '192.168.29.24',
  'X-ClientPublicIP': '49.36.83.202',
  'X-MACAddress': '82-AC-95-CE-84-45',
  'X-UserType': 'USER',
  'Authorization': Authorizationt_TOKEN,
  'Accept': 'application/json',
  'X-SourceID': 'WEB',
  'Content-Type': 'application/json'
}
BSETokenList = ["506852","543977","539660","500245","500123"]
parameterList = [
        ["Aditya Sunlife",token_holding_mapping_aditya,47,93.07],
        ["Quant SmallCap",token_holding_mapping_quant,100,95.06],
        ["Nippon SmallCap",token_holding_mapping_nippon,205,95.98],
        ["Quant Infra",token_holding_mapping_quant_infra,25,87.66],
        ["ICICI Bharat",token_holding_mapping_icici_bharat,1,99.95],
        ["ICICI SmallCap",token_holding_mapping_icici_prudential_smallcap,90,91.76]
    ]
async def sendMessageTelegram(message,bot):
    await bot.send_message(chat_id=telegramChannelId, text=message)

def pctDiffStock(symbolToken,exchange):
    ltpData = smartApi.ltpData(exchange=exchange,symboltoken=symbolToken,tradingsymbol="")
    if ltpData['status']:
        if ltpData['data']['close'] == 0:
            print("Zero close value for token "+symbolToken)
            print("\n")
            print(ltpData)
            print("\n")
            return 0
        else:
            pctDiff = ( (ltpData['data']['ltp'] - ltpData['data']['close']) / ltpData['data']['close'] ) * 100
            return pctDiff
    else:
        print("Error for both historic Data and LTP for token = "+ symbolToken)
        return 0


def CalcChange(MFName,token_holding_mapping,BSETokenList,numberOfStocks,totalPercentage):
    print(MFName)
    total = float(0)
    i = 0
    progress = progressbar.ProgressBar(maxval=numberOfStocks, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    progress.start()
    for token in token_holding_mapping:
        i = i + 1
        # time.sleep(0.5)
        progress.update(i)
        pctDiff = 0
        if token in BSETokenList:
            pctDiff = pctDiffStock(token,"BSE")
        else:
            pctDiff = pctDiffStock(token,"NSE")
        total = total + (pctDiff * float(token_holding_mapping[token]))
    progress.finish()
    message =  str(round(float((total/totalPercentage)), 2)) + "% \n("+ str(totalPercentage) +"% Accurate)"
    return (message)
def AllCalculation():
    FinalMessage = ""
    for parameter in parameterList:
        [MFName,token_holding_mapping,numberOfStocks,totalPercentage] = parameter
        try:
            message = CalcChange(MFName,token_holding_mapping,BSETokenList,numberOfStocks,totalPercentage)
            FinalMessage = FinalMessage + "\n" + message
            print(message)
        except Exception:
            print("Oops Error Occured:"+ Exception)
        bot1 = telegram.Bot(token=telebotApiKey)
        asyncio.run(sendMessageTelegram(message,bot1))
        time.sleep(1)
    return FinalMessage

def individualCalc(tokenParameterIndex):
    print("starting")
    [MFName,token_holding_mapping,numberOfStocks,totalPercentage] = parameterList[tokenParameterIndex]
    try:
        message = CalcChange(MFName,token_holding_mapping,BSETokenList,numberOfStocks,totalPercentage)
        print(message)
    except Exception:
        print("Oops Error Occured:"+ Exception)
    # bot1 = telegram.Bot(token=telebotApiKey)
    # asyncio.run(sendMessageTelegram(message,bot1))
    time.sleep(1)
    print("ended")
    return message









