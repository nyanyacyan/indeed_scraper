# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/ccx_csv_to_drive/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/instagram_list_tool/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, time
import pandas as pd
import concurrent.futures
from typing import Dict
from datetime import datetime, date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.utils.time_manager import TimeManager
from method.base.selenium.google_drive_download import GoogleDriveDownload
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.spreadsheet.err_checker_write import GssCheckerErrWrite
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from method.base.utils.file_move import FileMove
from method.base.selenium.google_drive_upload import GoogleDriveUpload
from method.get_gss_df_flow import GetGssDfFlow
from method.base.selenium.driverWait import Wait
# from method.base.utils.date_manager import DateManager
from method.base.utils.sub_date_mrg import DateManager


# const
from method.const_element import ( GssInfo, LoginInfo, ErrCommentInfo, PopUpComment, Element, )

# flow
# from method.good_flow import GetUserToInsta
from method.comment_flow import CommentFlow
from method.good_flow import GoodFlow

deco = Decorators()

# ----------------------------------------------------------------------------------

# **********************************************************************************
# 一連の流れ


class SingleProcess:
    def __init__(self):
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        self.timestamp = datetime.now()
        self.timestamp_two = self.timestamp.strftime("%Y-%m-%d %H:%M")
        self.date_only_stamp = self.timestamp.date().strftime("%m月%d日")

        # ✅ Chrome の起動をここで行う
        self.chromeManager = ChromeManager()
        self.chrome = self.chromeManager.flowSetupChrome()

        # const
        self.const_gss_info = GssInfo.INSTA.value
        self.const_login_info = LoginInfo.INSTA.value
        self.const_element = Element.INSTA.value
        self.const_err_cmt_dict = ErrCommentInfo.INSTA.value
        self.popup_cmt = PopUpComment.INSTA.value

        # Flow
        self.get_gss_df_flow = GetGssDfFlow(chrome=self.chrome)
        # self.get_user_data = GetUserToInsta(chrome=self.chrome)
        self.comment_flow = CommentFlow(chrome=self.chrome)
        self.good_flow = GoodFlow(chrome=self.chrome)

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.drive_download = GoogleDriveDownload()
        self.drive_upload = GoogleDriveUpload()
        self.select_cell = GssSelectCell()
        self.gss_check_err_write = GssCheckerErrWrite()
        self.popup = Popup()
        self.click_element = ClickElement(chrome=self.chrome)
        self.file_move = FileMove()
        self.wait = Wait(chrome=self.chrome)
        self.date_manager = DateManager()
        self.select_cell = GssSelectCell()


    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    def _single_process(self):
        """各プロセスを実行する"""
        try:
            #* 今回はログインあとのフロートする
            # GSSよりデータ取得→dfを作成
            target_df = self.get_gss_df_flow.process(worksheet_name=self.const_gss_info['TARGET_WORKSHEET_NAME'])
            account_info = self.get_gss_df_flow.get_account_process(worksheet_name=self.const_gss_info['ACCOUNT_WORKSHEET_NAME'])

            # ログイン
            self.login.flowLoginID(id_text=account_info['GSS_ID_TEXT'], pass_text=account_info['GSS_PASS_TEXT'], login_info=self.const_login_info)

            # 対象のページが開いているかどうかを確認
            self.wait.canWaitClick(value=self.const_element['value_1'])

            # Googleスプレッドシートから情報取得
            # - 「マスター」シートへアクセス
            # - 1行目から以下の情報を取得
            #   - 検索キーワード
            #   - 検索地域
            #   - 除外ワード

            # 2
            # ログインURLへアクセス
            # - 手動ログイン（ユーザー操作対応）

            # 3
            # ログイン後、検索窓が表示されるまで最大300秒待機

            # 4
            # 新しいタブを開き、クッキー情報を維持したままアクセス

            # 5
            # 検索窓にキーワードと地域を入力し、Enterキーで検索実行

            # 6
            # 表示された h2 タグのリストを取得

            # 7
            # 各 h2 を順にクリックし、詳細画面へ遷移

            # 8
            # 特定HTML要素からテキスト情報を抽出（BeautifulSoup）
            # - 例：`jobsearch-ViewjobPaneWrapper` などの要素対象

            # 9
            # テキストをプロンプト整形 → ChatGPT APIへ送信
            # - 取得対象項目：
            #   - 勤務地
            #   - 給与（日給／時給など）
            #   - 雇用形態
            #   - 除外対象チェック（キーワード含有確認）

            # 10
            # ChatGPTレスポンスを辞書形式に変換・整形

            # 11
            # 除外ワードと照合し、該当する場合はスキップ

            # 12
            # 辞書データをスプレッドシートに書き込み

            # 13
            # 次の h2 へ移動して処理を繰り返し実行

            # 14
            # 次の検索条件行へ移動し、Step [1] から再実行

                        # # 新しいタブを開いてURLにアクセス
                        # main_window = self.chrome.current_window_handle
                        # self.get_element._open_new_page(url=target_user_url)
                        # self.random_sleep._random_sleep(2, 5)


                        # # 投稿完了→スプシに日付の書込
                        # self.logger.debug(f"投稿完了→スプシに日付の書込")
                        # self.logger.debug(f"cell: {gss_date_cell}")
                        # self.gss_write.write_data_by_url(gss_info=self.const_gss_info, cell=gss_date_cell, input_data=self.timestamp)

                        # # 対象のタブを閉じる
                        # self.chrome.close()
                        # self.chrome.switch_to.window(main_window)
                        # self.logger.debug(f"タブを閉じました: {target_user_url}")
                        # self.logger.warning(f"【{account_process_count + 1}つ目】処理完了  URL: {target_user_url}")
                        # account_process_count += 1

        except TimeoutError:
            timeout_comment = "タイムエラー：ログインに失敗している可能性があります。"
            self.logger.error(f"{self.__class__.__name__} {timeout_comment}")

        except Exception as e:
            process_error_comment = ( f"{self.__class__.__name__} 処理中にエラーが発生 {e}" )
            self.logger.error(process_error_comment)

        finally:
            # ✅ Chrome を終了
            self.chrome.quit()
            self.popup.popupCommentOnly( popupTitle=self.popup_cmt["POPUP_COMPLETE_TITLE"], comment=self.popup_cmt["POPUP_COMPLETE_MSG"], )

    # ----------------------------------------------------------------------------------

    def _delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"指定のファイルの削除を実施: {file_path}")

        else:
            self.logger.error( f"{self.__class__.__name__} ファイルが存在しません: {file_path}" )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = SingleProcess()
    # 引数入力
    test_flow._single_process()
