from installer.src.main import Main
from installer.src.method.base.utils.logger import Logger
from installer.src.method.base.utils.error_handler import ErrorHandler, InfoHandler, CriticalHandler
from installer.src.method.base.utils.time_manager import TimeManager

error_count = 0
report_count = 0

while True:
    try:
        # --- メイン処理（例：スクレイピングやテスト） ---
        main = Main()  # ここでメインの処理を呼び出す

        # logger
        getLogger = Logger()
        logger = getLogger.getLogger()

        # slack notify
        info_notify = InfoHandler()
        error_notify = ErrorHandler()
        critical_notify = CriticalHandler()

        random_sleep = TimeManager()

        # 処理の実行
        result = main.main()
        logger.info("✅ 正常に終了しました")

        # 5回に1回の定期レポート送信
        report_count += 1
        if report_count % 5 == 0:
            info_notify.append_test_log()

    except Exception as e:
        error_count += 1
        error_notify.slack_notify_with_screenshot()
        logger.error(f"❌ エラーが発生しました: {e}")

    # ランダムに待機（30〜60分）
    wait_min = random.randint(30, 60)
    time.sleep(wait_min * 60)
