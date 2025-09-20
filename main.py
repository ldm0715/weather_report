import requests as re
from requests import Response
import os
from time import localtime, struct_time, strftime
from loguru import logger
from pprint import pp
# from dotenv import load_dotenv
from typing import Dict
import json

# load_dotenv("config.env")


# 从测试号信息获取
appID: str | None = os.getenv("APP_ID")
appSecret: str | None = os.getenv("APP_SECRET")
# 收信人ID即 用户列表中的微信号
openId: str | None = os.getenv("OPEN_ID")
# 天气预报模板ID
weather_template_id: str | None = os.getenv("TEMPLATE_ID")

weather_key: str | None = os.getenv("WEATHER_KEY")
location: str | None = os.getenv("LOCATION")


def test_env_info() -> None:
    print(weather_key, location)


def get_current_time() -> str:
    """获取当前时间

    Returns:
        str: 格式化后的时间字符串
    """
    now: struct_time = localtime()
    return strftime("%Y-%m-%d %H:%M:%S", now)


def get_one_verse() -> Dict:
    """
    返回随机的一句诗

    Returns:
        Dict: 数据

    Example:
    {
        "content" : "来日绮窗前，寒梅著花未。",
        "origin" : "杂诗三首 / 杂咏三首",
        "author" : "王维",
        "category" : "古诗文-植物-梅花"
    }
    """
    response: Response = re.get("https://v1.jinrishici.com/all.json")

    if response.status_code == 200:
        return response.json()

    return {}


def get_weather_data() -> Dict:
    """
    通过心知天气获取天气实况
    api ：https://api.seniverse.com/v3/weather/now.json

    Returns:
        dict: 天气数据，json格式
    """

    data: Response = re.get(
        "https://api.seniverse.com/v3/weather/now.json",
        params={"key": weather_key, "location": location},
    )

    # pp(data.url)
    logger.info(f"{get_current_time} 请求的url为{data.url}")

    result: dict = {}

    if data.status_code == 200:
        logger.success(f"{get_current_time()} 获取天气数据成功")
        result["code"] = 200
        result["data"] = data.json()
        result["message"] = "success"
    else:
        logger.error(f"{get_current_time()} 获取天气数据失败 {data.json()["status"]}")
        result["code"] = 500
        result["message"] = "fail"
        result["data"] = {}
    return result


def send_weather(access_token: str, weather_data: Dict, verse_data: Dict) -> None:
    """
    根据模板来发送消息到微信公众号

    Args:
        weather_data (Dict): 天气信息
        verse_data (Dict): 诗句信息
    """

    weather: str = weather_data["results"][0]["now"]["text"]
    temperature: str = weather_data["results"][0]["now"]["temperature"] + "°C"
    region: str = weather_data["results"][0]["location"]["name"]

    today_verse: str = verse_data["content"]

    print(weather, temperature, region, today_verse)

    body: dict = {
        "touser": openId,
        "template_id": weather_template_id,
        "url": "https://weixin.qq.com",
        "data": {
            "date": {"value": get_current_time()},
            "region": {"value": region},
            "weather": {"value": weather},
            "temp": {"value": temperature},
            "today_verse": {"value": today_verse},
        },
    }
    url: str = (
        f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    )
    print(re.post(url, json.dumps(body)).text)


def get_access_token() -> str | None:
    """
    获取access token的url

    Returns:
        _type_: access_token
    """
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
        appID, appSecret
    )
    response: dict = re.get(url).json()
    pp(response)
    access_token: str | None = response.get("access_token")
    logger.info(f"获取access_token成功 {access_token}")
    return access_token


def main():
    weather_data: dict = get_weather_data()["data"]
    verse_data: Dict = get_one_verse()

    access_token = get_access_token()

    if access_token is not None:
        send_weather(access_token, weather_data, verse_data)
    # test_env_info()


if __name__ == "__main__":
    main()
# POST https://api.weixin.qq.com/cgi-bin/message/template/subscribe?access_token=ACCESS_TOKEN
