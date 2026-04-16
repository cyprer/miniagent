import datetime
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


@tool
def get_current_time() -> str:
    """获取当前系统时间，格式为YYYY-MM-DD HH:MM:SS"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


web_search = DuckDuckGoSearchRun(
    name="web_search",
    description="搜索互联网获取最新信息，当你需要查询实时新闻、天气预报、股票价格、实时比赛结果或其他最新数据时使用此工具"
)


def get_tools():
    return [get_current_time, web_search]
