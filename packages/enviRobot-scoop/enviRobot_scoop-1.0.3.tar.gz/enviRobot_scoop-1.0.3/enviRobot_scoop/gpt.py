# coding:utf-8
import openai
import datetime as dt
import os
from dotenv import load_dotenv
from .get_data import *
import time
import opencc
import cameo_eco_query

# https://www.youtube.com/watch?v=I4T--ycOpi0&ab_channel=JieJenn

load_dotenv(dotenv_path='./.env')

# deprecated
def openai_init(key_path):
    openai.api_key = os.getenv('OPENAI_KEY')

#20230825 bear add 強制轉繁體中文
def convert_to_traditional_chinese(text):
    converter = opencc.OpenCC('s2tw')
    converted_text = converter.convert(text)
    return converted_text

def eco_ask_3w_handler(str_input, image_name, lang='CH'):
    print('eco_ask_3w_handler/cameo eco query', flush=True)
    result = cameo_eco_query.get_event_gmap_info(str_input, lang)
    if result['status'] == 'error':
        return result['message']
    else: 
        result = result['data']

    if lang == 'EN':
        str_message = f"Time: {result['time']}\nLocation: {result['location']}\nIncident: {result['event']}\nGoogle Map Link: {result['gmap']}"
    elif lang == 'CH':
        str_message = f"時間：{result['time']}\n地點：{result['location']}\n案件：{result['event']}\ngoogle map link :{result['gmap']}"
    
    str_wind_info = get_cwb_wind_data(result['lat'], result['lon'], result["time"], lang)
    print('eco_ask_3w_handler/fetched wind data, fetching aiot data', flush=True)
    str_device_info = get_rawdata(result['lat'], result['lon'], result["time"], image_name, lang, mode = '10min')
    print('eco_ask_3w_handler/fetched aiot data', flush=True)

    if str_device_info != "":
        str_message += "\n\n" + str_device_info
    if str_wind_info != "":
        str_message += "\n\n" + str_wind_info
    return str_message

def location_handler(lat, lon, image_name, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    str_message = ""
    result = {}
    result["time"] = (dt.datetime.utcnow()+dt.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    str_wind_info = get_cwb_wind_data(lat, lon, result["time"], lang)
    print('eco_ask_3w_handler/fetched wind data, fetching aiot data', flush=True)
    str_device_info = get_rawdata(lat, lon, result["time"], image_name, lang)
    print('eco_ask_3w_handler/fetched aiot data', flush=True)
    if str_device_info != "":
        str_message += str_device_info
    if str_wind_info != "":
        str_message += "\n\n" + str_wind_info

    if lang == 'CH':
        str_message = convert_to_traditional_chinese(str_message)

    return str_message

def gpt_generate_report(basic_data, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    print('gpt_generate_report/start', flush=True)
    #openai_init('keys/openai')
    prompt = []
    #roles: system, assistant, user
    prompt.append({
        'role':
        'system',
        'content':
        '以下給你的「資訊」是一段環保領域相關、空氣品質的資料，請幫我依照以下的原則，整合「資訊」裡面的內容，變成一段結論：\
        - 顯示在「時間」「地點」發生了「案件」。其中，「時間」只需要到日期與幾點幾分即可，不要出現「秒」。\
        - 該「地點」的周邊天氣，請參考「氣象局測站資料」內容。「風向」的度數，轉成方位。風速可以描述依據數值描述風的大小。\
        - 如果沒有氣象測站資料的描述，就說沒有資料就好，不必做任何解釋，不要無中生有，否則會造成使用者困擾。\
        - 一公里方形內的 IoT 「pm2_5感測器濃度」是指「地點」周邊一公里內的 IoT 空氣品質的PM2.5 濃度數據。\
        - 請「不要」所有設備一顆一顆列出來，並且不要出現感測器編號。\
        - 可加上與「地點」的相對方位、距離，轉成總結。\
        - 如果沒有感測器資料，就說沒有資料就好，不必解釋，不要無中生有，否則會造成使用者困擾。\
        -' + ('請用英文回覆我' if lang=='EN' else '請用中文回覆我')
    })
    prompt.append({
        'role': 'user',
        'content': f'{basic_data}'
    })
    model = 'gpt-4-1106-preview'
    response = None
    for _ in range(5):
        try:
            client = openai.OpenAI(api_key=os.getenv('OPENAI_KEY'))
            response = client.chat.completions.create(model=model,
                                                    messages=prompt,
                                                    max_tokens=300)
            break
        except openai.error.RateLimitError:
            time.sleep(2)
            pass
    if response is None:
        content = '抱歉, 無法產生本次事件相關空氣品質報告, 或許您可以再試一次'
    else:
        content = response.choices[-1].message.content
        if lang =='CH':
            content = convert_to_traditional_chinese(content)
    print('gpt_generate_report/done', flush=True)
    return content

if __name__ == '__main__':

    str_input = '永和仁愛公園剛剛發生大火'
    #str_input = '《環境污染事件通報》第031901號\n一、案由：反映雜草火警，已派七輛消防車前往，火勢面積很大。\n二、地點：龍井區龍興路玉府天宮附近，靠近高速公路\n三、通報來源：消防局\n四、日期：112年03月19日\n (一)報案16:01\n (二)到達:已通報前往'
    #str_input = '斷稜西山在2023-03-22 10:00:00有人登頂'
    #str_input = '國道五號37路段，五分鐘前看到露天燃燒'
    #str_input = '我上禮拜一下午五點走路經過中正紀念堂看到那邊有黑煙'
    import time
    t = time.time()
    result = eco_ask_3w_handler(str_input, image_name='aaa')
    print(result, flush=True)
    print('', flush=True)
    gpt_generate_report(result)
    print(f'used {time.time()-t:.2f} seconds', flush=True)
