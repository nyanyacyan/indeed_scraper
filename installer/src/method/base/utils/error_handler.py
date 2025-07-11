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
from method.const_str import SlackChannel

####################################################################################
# **********************************************************************************


class CriticalHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.path = BaseToPath()
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

        # const
        self.error_channel = SlackChannel.ERROR_CHANNEL.value
        self.error_file_channel = SlackChannel.ERROR_FILE_CHANNEL.value

        # date
        self.fullCurrentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    # ----------------------------------------------------------------------------------
    # テスト用ログファイルに追記

    def append_test_log(self, content: str):
        self.test_log.append_test_log(content)

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
        screenshot_path = self._get_screenshot_path()
        full_path = screenshot_path / f"warning_{self.fullCurrentDate}.png"
        self.logger.info(f"スクリーンショットの保存先: {full_path}")
        self.chrome.save_screenshot(full_path)
        self.slack.slack_image_notify(message=error_comment, channel=self.error_channel, img_path=full_path)

    # ----------------------------------------------------------------------------------
    # slack通知＋ファイル送信

    def slack_notify_with_file(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        test_log_file_path = self.test_log.get_log_file_path()
        if test_log_file_path.exists():
            self.logger.info(f"テストログファイルのパス: {test_log_file_path}")
        else:
            self.logger.error(f"テストログファイルが存在しないため送信できません: {test_log_file_path}")
            return
        self.slack.slack_textfile_notify(message=error_comment, channel=self.error_file_channel, file_path=test_log_file_path)

    # ----------------------------------------------------------------------------------
    # スクショのpath

    def _get_screenshot_path(self) -> str:
        screenshot_path = self.path.screenshot_path
        self.logger.info(f"スクリーンショットのパス: {screenshot_path}, {type(screenshot_path)} 型")
        return screenshot_path
# ----------------------------------------------------------------------------------
# **********************************************************************************


class ErrorHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.path = BaseToPath()
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

        # const
        self.error_channel = SlackChannel.ERROR_CHANNEL.value
        self.error_file_channel = SlackChannel.ERROR_FILE_CHANNEL.value

        # date
        self.fullCurrentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    # ----------------------------------------------------------------------------------
    # テスト用ログファイルに追記

    def append_test_log(self, content: str):
        self.test_log.append_test_log(content)

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
        screenshot_path = self._get_screenshot_path()
        full_path = screenshot_path / f"warning_{self.fullCurrentDate}.png"
        self.logger.info(f"スクリーンショットの保存先: {full_path}")
        self.chrome.save_screenshot(full_path)
        self.slack.slack_image_notify(message=error_comment, channel=self.error_channel, img_path=full_path)

    # ----------------------------------------------------------------------------------
    # slack通知＋ファイル送信

    def slack_notify_with_file(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        test_log_file_path = self.test_log.get_log_file_path()
        if test_log_file_path.exists():
            self.logger.info(f"テストログファイルのパス: {test_log_file_path}")
        else:
            self.logger.error(f"テストログファイルが存在しないため送信できません: {test_log_file_path}")
            return
        self.slack.slack_textfile_notify(message=error_comment, channel=self.error_file_channel, file_path=test_log_file_path)

    # ----------------------------------------------------------------------------------
    # スクショのpath

    def _get_screenshot_path(self) -> str:
        screenshot_path = self.path.screenshot_path
        self.logger.info(f"スクリーンショットのパス: {screenshot_path}, {type(screenshot_path)} 型")
        return screenshot_path
# ----------------------------------------------------------------------------------
# **********************************************************************************
# 基本は処理が成功した際に使用

class InfoHandler:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.path = BaseToPath()
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

        # const
        self.error_channel = SlackChannel.ERROR_CHANNEL.value
        self.error_file_channel = SlackChannel.ERROR_FILE_CHANNEL.value

        # date
        self.fullCurrentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    # ----------------------------------------------------------------------------------
    # テスト用ログファイルに追記

    def append_test_log(self, content: str):
        self.test_log.append_test_log(content)

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
        screenshot_path = self._get_screenshot_path()
        full_path = screenshot_path / f"warning_{self.fullCurrentDate}.png"
        self.logger.info(f"スクリーンショットの保存先: {full_path}")
        self.chrome.save_screenshot(full_path)
        self.slack.slack_image_notify(message=error_comment, channel=self.error_channel, img_path=full_path)

    # ----------------------------------------------------------------------------------
    # slack通知＋ファイル送信

    def slack_notify_with_file(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        test_log_file_path = self.test_log.get_log_file_path()
        if test_log_file_path.exists():
            self.logger.info(f"テストログファイルのパス: {test_log_file_path}")
        else:
            self.logger.error(f"テストログファイルが存在しないため送信できません: {test_log_file_path}")
            return
        self.slack.slack_textfile_notify(message=error_comment, channel=self.error_file_channel, file_path=test_log_file_path)

    # ----------------------------------------------------------------------------------
    # スクショのpath

    def _get_screenshot_path(self) -> str:
        screenshot_path = self.path.screenshot_path
        self.logger.info(f"スクリーンショットのパス: {screenshot_path}, {type(screenshot_path)} 型")
        return screenshot_path
    # ----------------------------------------------------------------------------------
# **********************************************************************************

class TestResultAction:
    def __init__(self, chrome: WebDriver= None):

        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        # chrome
        self.chrome = chrome

        # インスタンス
        self.path = BaseToPath()
        self.popup = Popup()
        self.test_log = TestLog()
        self.slack = SlackNotify()

        # const
        self.error_channel = SlackChannel.ERROR_CHANNEL.value
        self.error_file_channel = SlackChannel.ERROR_FILE_CHANNEL.value

        # date
        self.fullCurrentDate = datetime.now().strftime("%y%m%d_%H%M%S")

    # ----------------------------------------------------------------------------------
    # criticalエラーの際にポップアップを表示してsystem.exitする

    def popup_process(self, err_title: str, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        self.popup.popupCommentOnly(popupTitle=err_title, comment=error_comment)
        sys.exit(1)

    # ----------------------------------------------------------------------------------
    # テスト用ログファイルに追記

    def append_test_log(self, content: str):
        self.test_log.append_test_log(content)

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
        screenshot_path = self._get_screenshot_path()
        full_path = screenshot_path / f"warning_{self.fullCurrentDate}.png"
        self.logger.info(f"スクリーンショットの保存先: {full_path}")
        self.chrome.save_screenshot(full_path)
        self.slack.slack_image_notify(message=error_comment, channel=self.error_channel, img_path=full_path)

    # ----------------------------------------------------------------------------------
    # テスト結果ファイルをslack通知＋ファイル送信

    def test_result_file_notify(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        test_result_file_path = self._get_test_result_file_path()
        if test_result_file_path.exists():
            self.logger.info(f"テストログファイルのパス: {test_result_file_path}")
        else:
            self.logger.error(f"テストログファイルが存在しないため送信できません: {test_result_file_path}")
            return
        self.slack.slack_textfile_notify(message=error_comment, channel=self.error_file_channel, file_path=test_result_file_path)

    # ----------------------------------------------------------------------------------
    # エラーログファイルをslack通知＋ファイル送信

    def error_log_file_notify(self, err_msg: str, e: Exception):
        error_comment = f"{err_msg}\n{e}"
        self.logger.error(error_comment)
        error_log_file_path = self._get_error_log_file_path()
        if error_log_file_path.exists():
            self.logger.info(f"テストログファイルのパス: {error_log_file_path}")
        else:
            self.logger.error(f"テストログファイルが存在しないため送信できません: {error_log_file_path}")
            return
        self.slack.slack_textfile_notify(message=error_comment, channel=self.error_file_channel, file_path=error_log_file_path)

    # ----------------------------------------------------------------------------------
    # スクショのpath

    def _get_screenshot_path(self) -> str:
        screenshot_path = self.path.screenshot_path()
        self.logger.info(f"スクリーンショットのパス: {screenshot_path}, {type(screenshot_path)} 型")
        return screenshot_path

    # ----------------------------------------------------------------------------------
    # テスト用ログファイル生成

    def _get_test_result_file_path(self) -> str:
        test_log_dir = self.path.test_results_path()
        file_name = f"test_result_{self.time_minutes}_start.txt"
        log_file_path = test_log_dir / file_name
        self.logger.info(f"ログファイルのパス: {log_file_path}, {type(log_file_path)} 型")
        return log_file_path

    # ----------------------------------------------------------------------------------
    # error用ログファイル生成

    def _get_error_log_file_path(self) -> str:
        test_log_dir = self.path.error_logs_path()
        file_name = f"error_log_{self.time_minutes}_start.txt"
        log_file_path = test_log_dir / file_name
        self.logger.info(f"ログファイルのパス: {log_file_path}, {type(log_file_path)} 型")
        return log_file_path

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

    def append_test_log(self, content: str, log_file_path: str):
        self.write_log(content, log_file_path=log_file_path)

    #! ----------------------------------------------------------------------------------
    # ログファイルにinfoを追記する

    def append_info(self, content: str, log_file_path: str):
        content = f"✅[INFO] {content}"
        self.write_log(content, log_file_path=log_file_path)

    #! ----------------------------------------------------------------------------------
    # ログファイルにwarningを追記する

    def append_warning(self, content: str, log_file_path: str):
        content = f"⚠️[WARNING] {content}"
        self.write_log(content, log_file_path=log_file_path)

    #! ----------------------------------------------------------------------------------
    # ログファイルにerrorを追記する

    def append_error(self, content: str, log_file_path: str, e: Exception = None):
        content = f"❌[ERROR] {content} {e}" if e else f"❌[ERROR] {content}"
        self.write_log(content, log_file_path=log_file_path)

    #! ----------------------------------------------------------------------------------
    # ログファイルにcriticalを追記する

    def append_critical(self, content: str, log_file_path: str, e: Exception = None):
        content = f"❌❌[CRITICAL] {content} {e}" if e else f"❌❌[ERROR] {content}"
        self.write_log(content, log_file_path=log_file_path)


    #! ----------------------------------------------------------------------------------
    # ログファイルを初期化する（先頭メッセージを書き込む）

    def generate_test_log(self, log_file_path: str):
        self.write_log(content="🚀===== テスト開始 =====🚀", log_file_path=log_file_path, mode='w')

    #! ----------------------------------------------------------------------------------
    # テスト用のログを残すためのファイル生成する

    def write_log(self, content: str, log_file_path: str, mode: str = 'a') -> str | None:
        try:
            with open(str(log_file_path), mode, encoding='utf-8') as f:
                f.write(content + "\n")
            self.logger.info(f"ログに追記しました: {log_file_path}")
            return log_file_path
        except Exception as e:
            self.logger.error(f"ログファイルへの追記に失敗しました: {e}")


    # ----------------------------------------------------------------------------------
    # error用ログファイル生成

    def _get_error_log_file_path(self) -> str:
        test_log_dir = self.path.error_logs_path()
        file_name = f"error_log_{self.time_minutes}_start.txt"
        log_file_path = test_log_dir / file_name
        self.logger.info(f"ログファイルのパス: {log_file_path}, {type(log_file_path)} 型")
        return log_file_path

    # ----------------------------------------------------------------------------------
    # テスト用のログを残すためのファイル生成する

    def write_test_result_log(self, content: str):
        log_file_path = self._get_test_result_file_path()
        try:
            with open(str(log_file_path), 'a', encoding='utf-8') as f:
                f.write(content + "\n")
            self.logger.info(f"ログに追記しました: {log_file_path}")
            return log_file_path

        except Exception as e:
            self.logger.error(f"ログファイルへの追記に失敗しました: {e}")


    # ----------------------------------------------------------------------------------
    # テスト用ログファイル生成

    def _get_test_result_file_path(self) -> str:
        test_log_dir = self.path.test_results_path()
        file_name = f"test_result_{self.time_minutes}_start.txt"
        log_file_path = test_log_dir / file_name
        self.logger.info(f"ログファイルのパス: {log_file_path}, {type(log_file_path)} 型")
        return log_file_path

    # ----------------------------------------------------------------------------------
