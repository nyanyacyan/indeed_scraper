#  coding: utf-8
# 文字列をすべてここに保管する
# ----------------------------------------------------------------------------------
# 2024/7/17 更新
# tree -I 'venv|resultOutput|__pycache__'
# ? Command + F10で大文字変換
# ----------------------------------------------------------------------------------
# import
import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------------------------------------------------------
# GSS情報


class GssInfo(Enum):

    INDEED = {
        "JSON_KEY_NAME": "sns-auto-430920-08274ad68b41.json",
        "SHEET_URL": "https://docs.google.com/spreadsheets/d/18Vo8pzbGkl-3M7PUDdHOyx52Hm1lo1apyc-U00uznw4/edit?gid=0#gid=0",
        "MASTER_WS": "Master",
        "CHATGPT_WS": "ChatGPT",

        # column名
        "SELECT_CHECK": "実施可否",
        "SEARCH_WORDS": "検索キーワード",
        "SEARCH_REGION": "検索地域",
        "EXCLUDED_WORDS_FIRST": "除外ワード_1",
        "EXCLUDED_WORDS_SECOND": "除外ワード_2",
        "EXCLUDED_WORDS_THIRD": "除外ワード_3",
        "EXCLUDED_WORDS_FOURTH": "除外ワード_4",
        "EXCLUDED_WORDS_FIFTH": "除外ワード_5",
        "ADD_WS": "追加Worksheet",
        "BASE_PROMPT": "base_prompt",

        # 追加ページColumn
        "ADD_DATE": "追加日時",
        "H2_TITLE": "タイトル",
        "WORK_PLACE": "勤務地",
        "SALARY": "給料",
        "WORKING_HOURS": "勤務時間",
        "PAGE_LINK": "リンク",

        "BASE_PROMPT_CELL": "A2",
        "EXCEPT_PROMPT_CELL": "B2",
        "MISSING_PROMPT_CELL": "C2",
    }


# ----------------------------------------------------------------------------------
# ログイン情報



class ErrCommentInfo(Enum):

    INDEED = {

        # POPUP_TITLE
        "POPUP_TITLE_SHEET_INPUT_ERR": "スプレッドシートをご確認ください。",
        "POPUP_TITLE_FACEBOOK_LOGIN_ERR": "ログインが必要です",
        "POPUP_TITLE_SHEET_CHECK": "スプレッドシートのチェックされている項目がありません",
        "POPUP_TITLE_SHEET_START_DATE": "対象の「取得開始日時」の欄が入力されてないです。",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
    }


# ----------------------------------------------------------------------------------


class PopUpComment(Enum):
    INDEED = {
        "POPUP_COMPLETE_TITLE": "処理完了",
        "POPUP_COMPLETE_MSG": "正常に処理が完了しました。",
        "": "",
    }


# ----------------------------------------------------------------------------------

class CommentFlowElement(Enum):
    INDEED = {
        "GSS_COLUMN_NAME": "コメント or いいね",
        "INPUT_WORD_COMMENT": "コメント",
        "INPUT_WORD_GOOD": "いいね",

    }


# ----------------------------------------------------------------------------------

class ChatgptInfo(Enum):
    INDEED = {
        "CHATGPT_API_URL": "https://api.openai.com/v1/chat/completions",
        "CHATGPT_MODEL": "gpt-4.1-mini",
        "CHATGPT_API_KEY": os.getenv('CHATGPT_API_KEY'),
    }


# ----------------------------------------------------------------------------------

class Element(Enum):
    INDEED = {
        "LOGIN_URL": "https://secure.indeed.com/auth?hl=ja_JP&co=JP",
        "HOME_URL": "https://jp.indeed.com/?r=us",

        # 検索窓の検知
        "BY_1": 'id',
        "VALUE_1": 'text-input-what',

        # Home画面をクリック
        "BY_2": "id",
        "VALUE_2": "indeed-globalnav-logo",

        # 地域入力
        "BY_3": "id",
        "VALUE_3": "text-input-where",

        # h2取得
        "BY_4": "tag",
        "VALUE_4": "h2",
        "PARENT_BY": "id",
        "PARENT_ID": "jobsearch-ViewjobPaneWrapper",
        "CHILDREN_CLASS": "jobsearch-JobComponent-description",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
    }

# ----------------------------------------------------------------------------------


