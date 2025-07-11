from installer.src.main import Main
from installer.src.method.base.utils.logger import Logger
from installer.src.method.base.utils.error_handler import ErrorHandler, InfoHandler, CriticalHandler
from installer.src.method.base.utils.time_manager import TimeManager

error_count = 0
report_count = 0


class TestRepeatProcess:

    def __init__(self):
        # logger
        getLogger = Logger()
        self.logger = getLogger.getLogger()

        # slack notify
        self.info_notify = InfoHandler()
        self.error_notify = ErrorHandler()
        self.critical_notify = CriticalHandler()

        self.random_sleep = TimeManager()

        self.main = Main()  # ここでメインの処理を呼び出す

    def run_repeated_test(self):
        error_count = 0
        report_count = 0
        max_processes = 12  # 最大の実施数
        while True:
            try:
                # 処理の実行
                self.main.main()
                self.logger.info("✅ 正常に終了しました")

                # 5回に1回の定期レポート送信
                report_count += 1
                if report_count % 5 == 0:

                    # TODO 結果レポートに追記
                    self.info_notify.append_test_log()

            except Exception as e:
                error_count += 1
                self.error_notify.slack_notify_with_screenshot()
                self.logger.error(f"❌ エラーが発生しました: {e}")

                # エラーログに追記

                # TODO 結果レポートに追記

            # ランダムに待機（30〜60分）
            self.random_sleep._random_sleep(30, 60)
            self.logger.info(f"現在のエラー数: {error_count}, レポート数: {report_count}")
            if report_count >= max_processes:


                self.logger.info("テストが完了しました。")
                self.logger.info(f"最終エラー数: {error_count}, レポート数: {report_count}")

                # テスト結果ログファイルにテストが終了したことを追記
                self.info_notify.append_test_log(f"テストが完了しました。最終エラー数: {error_count}, レポート数: {report_count}")
                self.logger.info("テスト結果ログファイルにテストが完了したことを追記しました。")

                # TODO エラーログファイルを送信
                self.info_notify.slack_notify_with_screenshot()

                # TODO テスト結果ログファイルを送信
                self.critical_notify.slack_notify_with_screenshot()

                break




