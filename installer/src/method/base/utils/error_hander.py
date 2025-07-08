# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import sys
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.utils.popup import Popup
from method.base.utils.path import BaseToPath
from method.base.notify.notify import SlackNotify

# ----------------------------------------------------------------------------------
####################################################################################
# **********************************************************************************


class CriticalHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    #!###################################################################################
    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------

# **********************************************************************************


class ErrorHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    #!###################################################################################
    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------

# **********************************************************************************


class WarningHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()


        self.chrome = chrome


        # インスタンス
        self.path = BaseToPath()
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    #!###################################################################################
# ----------------------------------------------------------------------------------
# テスト用ログファイルに追記


# ----------------------------------------------------------------------------------
# slack通知のみ

    def slack_notify(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.slack.send_message(error_comment)

# ----------------------------------------------------------------------------------
# slack通知+スクショ

    def slack_notify_with_screenshot(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.chrome.save_screenshot("screenshot.png")

        self.slack.slack_image_notify(self.slack.slack_notify_token, error_comment, screenshot_path)


# ----------------------------------------------------------------------------------
# slack通知＋ファイル送信

# ----------------------------------------------------------------------------------
# slack通知＋ふぁいる

# ----------------------------------------------------------------------------------
# スクショのpath
    def get_screenshot_path(self) -> str:
        self.path.
# ----------------------------------------------------------------------------------

# **********************************************************************************
# 基本は処理が成功した際に使用

class InfoHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

    #!###################################################################################
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, info_title: str, info_msg: str):

        self.logger.info(info_msg)
        self.popup.popupCommentOnly(popupTitle=info_title, comment=info_msg)

    #!###################################################################################
    # ----------------------------------------------------------------------------------



    # ----------------------------------------------------------------------------------
# **********************************************************************************


class TestLog:
    def __init__(self):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath()
        self.time_minutes = datetime.now().strftime("%H%M")

    #! ----------------------------------------------------------------------------------
    # ログファイルに追記する

    def append_test_log(self, content: str):
        self.write_log(content, mode='a')

    #! ----------------------------------------------------------------------------------
    # ログファイルにinfoを追記する

    def append_info(self, content: str):
        content = f"✅[INFO] {content}"
        self.write_log(content, mode='a')

    #! ----------------------------------------------------------------------------------
    # ログファイルにwarningを追記する

    def append_warning(self, content: str):
        content = f"⚠️[WARNING] {content}"
        self.write_log(content, mode='a')

    #! ----------------------------------------------------------------------------------
    # ログファイルにerrorを追記する

    def append_error(self, content: str, e: Exception = None):
        content = f"❌[ERROR] {content} {e}" if e else f"❌[ERROR] {content}"
        self.write_log(content, mode='a')

    #! ----------------------------------------------------------------------------------
    # ログファイルにcriticalを追記する

    def append_critical(self, content: str, e: Exception = None):
        content = f"❌❌[CRITICAL] {content} {e}" if e else f"❌❌[ERROR] {content}"
        self.write_log(content, mode='a')

    #! ----------------------------------------------------------------------------------
    # ログファイルを初期化する（先頭メッセージを書き込む）

    def generate_test_log(self):
        self.write_log("🚀===== テスト開始 =====🚀", mode='w')

    #! ----------------------------------------------------------------------------------
    # テスト用のログを残すためのファイル生成する

    def write_log(self, content: str):
        log_file_path = self.get_log_file_path()
        try:
            with open(str(log_file_path), 'a', encoding='utf-8') as f:
                f.write(content + "\n")
            self.logger.info(f"ログに追記しました: {log_file_path}")
        except Exception as e:
            self.logger.error(f"ログファイルへの追記に失敗しました: {e}")


    # ----------------------------------------------------------------------------------
    # テスト用ログファイル生成

    def get_log_file_path(self) -> str:
        test_log_dir = self.path.test_logs_path()
        file_name = f"{self.time_minutes}_start.txt"
        log_file_path = test_log_dir / file_name
        self.logger.info(f"ログファイルのパス: {log_file_path}, {type(log_file_path)} 型")
        return log_file_path

    # ----------------------------------------------------------------------------------
