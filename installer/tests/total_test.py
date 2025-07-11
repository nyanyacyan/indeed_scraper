# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import asyncio
import os, sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from installer.src.main import Main
from installer.src.method.base.notify.notify import SlackNotify
from installer.src.method.base.utils.logger import Logger
from installer.src.method.base.utils.path import BaseToPath
from installer.src.method.base.utils.error_handler import TestLog, TestResultAction
from installer.src.method.base.utils.time_manager import TimeManager
from installer.src.method.const_str import SlackChannel

# ####################################################################################
# **********************************************************************************

class TestRepeatProcess:
    def __init__(self):
        # logger
        getLogger = Logger()
        self.logger = getLogger.getLogger()

        # 時間管理
        self.fullCurrentDate = datetime.now().strftime("%y%m%d_%H")

        # ランダムスリープ
        self.random_sleep = TimeManager()

        # インスタンス
        self.main = Main()  # ここでメインの処理を呼び出す
        self.test_log = TestLog()
        self.slack = SlackNotify()

        # path
        self.path = BaseToPath()
        self.test_result_log_path = self.path.test_results_path()
        self.error_log_path = self.path.error_logs_path()
        self.test_result_full_path = os.path.join(self.test_result_log_path, f"test_result_{self.fullCurrentDate}_start.txt")
        self.error_log_full_path = os.path.join(self.error_log_path, f"error_log_{self.fullCurrentDate}_start.txt")

        self.slack_channel = SlackChannel.ERROR_CHANNEL.value

    # ----------------------------------------------------------------------------------
    # メインの処理を繰り返し実行する

    async def run_repeated_test(self):
        error_count = 0
        report_count = 0
        max_processes = 12  # 最大の実施数
        while True:
            try:
                self.test_log.generate_test_log(self.test_result_full_path)
                self.slack.slack_notify(message=f"<@U094HH4LT1V> テスト開始: {self.fullCurrentDate}", channel=self.slack_channel)
                self.logger.info(f"🚀 テスト開始 {self.fullCurrentDate}")

                # 処理の実行
                # await self.main.main()

                completed_comment = f"【{report_count} / {max_processes} テスト】 正常に終了しました"
                self.logger.info(completed_comment)

                # テスト結果ログに追記
                self.test_log.append_info(content=completed_comment, log_file_path=self.test_result_full_path)

                report_count += 1

            except Exception as e:
                error_count += 1
                self.logger.error(f"❌ エラーが発生しました: {e}")

                # 結果レポートに追記
                self.test_log.append_error(content=f"エラーが発生しました: {e}",log_file_path=self.test_result_full_path,  e=e)
                self.test_log.append_error(content=f"エラーが発生しました: {e}",log_file_path=self.error_log_full_path,  e=e)


            # ランダムに待機（30〜60分）
            self.random_sleep._random_sleep(1800, 3600)
            self.logger.info(f"現在のエラー数: {error_count}, レポート数: {report_count}")
            if report_count >= max_processes:

                self.logger.info(f"【{report_count} / {max_processes} テスト】 全テストが完了しました。")
                self.logger.info(f"最終エラー数: {error_count}, レポート数: {report_count}")

                # テスト結果ログファイルにテストが終了したことを追記
                result_comment = f"テストが完了しました。最終エラー数: {error_count}, レポート数: {report_count}"
                self.test_log.append_error(content=result_comment, log_file_path=self.test_result_full_path,  e=e)
                self.logger.info("テスト結果ログファイルにテストが完了したことを追記しました。")

                # エラーログファイルを送信
                self.slack.slack_textfile_notify(message=result_comment, file_path=self.test_result_full_path)

                # テスト結果ログファイルを送信
                self.slack.slack_textfile_notify(message=result_comment, file_path=self.error_log_full_path)
                break


if __name__ == "__main__":
    test_process = TestRepeatProcess()
    asyncio.run(test_process.run_repeated_test())
    print("テストが完了しました。")
    print("テスト結果ログファイル:", test_process.test_result_full_path)
    print("エラーログファイル:", test_process.error_log_full_path)
