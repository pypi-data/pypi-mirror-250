from bk_notice_sdk import config
from bk_notice_sdk.utils import return_json_response, api_call


def get_content_from_content_list(content_list: list, language: str, default_language: str) -> str:
    if len(content_list) == 0:
        return ""
    if len(content_list) == 1:
        return content_list[0].get("content", "")
    filtered_dict = {
        content_data["language"]: content_data["content"]
        for content_data in content_list
        if content_data.get("language") in (language, default_language)
    }

    return filtered_dict.get(language, filtered_dict.get(default_language, content_list[0].get("content", "")))


@return_json_response
def get_current_information(request):
    """获得当前平台的通知公告信息"""
    res = api_call(
        api_method="announcement_get_current_announcements",
        success_message="平台获取通知公告信息成功",
        error_message="获取通知公告异常",
        params={"platform": config.PLATFORM},
    )

    data_list = res.get("data")
    if data_list is None:
        return res

    default_language = config.DEFAULT_LANGUAGE
    language = request.COOKIES.get(config.LANGUAGE_COOKIE_NAME, default_language)

    content_lists = [data.pop("content_list", []) for data in data_list]
    lst = [
        {
            **data,
            "content": get_content_from_content_list(
                content_list=content_list, language=language, default_language=default_language
            ),
        }
        for data, content_list in zip(data_list, content_lists)
    ]

    res["data"] = lst
    return res
