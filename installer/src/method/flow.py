# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Volumes/にゃにゃちゃんHD/Project_file/indeed_scraper/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.keys import Keys

# 自作モジュール
from method.base.utils.logger import Logger
from method.base.selenium.chrome import ChromeManager
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.selenium.seleniumBase import SeleniumBasicOperations
from method.base.spreadsheet.spreadsheetRead import GetDataGSSAPI
from method.base.selenium.get_element import GetElement
from method.base.decorators.decorators import Decorators
from method.base.spreadsheet.spreadsheetWrite import GssWrite
from method.base.spreadsheet.select_cell import GssSelectCell
from method.base.selenium.loginWithId import SingleSiteIDLogin
from method.base.utils.popup import Popup
from method.base.selenium.click_element import ClickElement
from method.base.utils.file_move import FileMove
from method.get_gss_df_flow import GetGssDfFlow
from method.base.selenium.driverWait import Wait
from method.base.selenium.jump_target_page import JumpTargetPage
from method.base.utils.sub_date_mrg import DateManager
from method.base.BS4.getHtml import GetHtmlParts

# const
from method.const_element import (
    GssInfo,
    ErrCommentInfo,
    PopUpComment,
    Element,
)

# flow
# from method.good_flow import GetUserToInsta

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
        self.const_gss_info = GssInfo.INDEED.value
        self.const_element = Element.INDEED.value
        self.const_err_cmt_dict = ErrCommentInfo.INDEED.value
        self.popup_cmt = PopUpComment.INDEED.value

        # Flow
        self.get_gss_df_flow = GetGssDfFlow(chrome=self.chrome)

        # インスタンス
        self.login = SingleSiteIDLogin(chrome=self.chrome)
        self.random_sleep = SeleniumBasicOperations(chrome=self.chrome)
        self.get_element = GetElement(chrome=self.chrome)
        self.selenium = SeleniumBasicOperations(chrome=self.chrome)
        self.gss_read = GetDataGSSAPI()
        self.gss_write = GssWrite()
        self.select_cell = GssSelectCell()
        self.popup = Popup()
        self.click_element = ClickElement(chrome=self.chrome)
        self.file_move = FileMove()
        self.wait = Wait(chrome=self.chrome)
        self.date_manager = DateManager()
        self.select_cell = GssSelectCell()
        self.new_page = JumpTargetPage(chrome=self.chrome)
        self.get_html_text = GetHtmlParts(chrome=self.chrome)

    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    def _single_process(self):
        """各プロセスを実行する"""
        try:
            # TODO ログインする
            # 手動ログイン# 1
            self.chrome.get(self.const_element["LOGIN_URL"])

            # TODO ユーザーに既存でブラウザを開いていたら閉じるようにアナウンス

            # 対象のページが開いているかどうかを確認
            # ログイン後、検索窓が表示されるまで最大300秒待機
            self.wait.canWaitClick(by=self.const_element["BY_1"], value=self.const_element["VALUE_1"], timeout=300)

            # Googleスプレッドシートから情報取得
            # - 「マスター」シートへアクセス
            target_df = self.get_gss_df_flow.process( worksheet_name=self.const_gss_info["MASTER_WS"] )

            # - 1行目から以下の情報を取得
            target_df.iterrows()
            for index, row in target_df.iterrows():
                # 各行の情報を取得
                search_word = row[self.const_gss_info["SEARCH_WORDS"]]
                search_region = row[self.const_gss_info["SEARCH_REGION"]]
                excluded_words_first = row[self.const_gss_info["EXCLUDED_WORDS_FIRST"]]
                excluded_words_second = row[self.const_gss_info["EXCLUDED_WORDS_SECOND"]]
                excluded_words_third = row[self.const_gss_info["EXCLUDED_WORDS_THIRD"]]
                excluded_words_fourth = row[self.const_gss_info["EXCLUDED_WORDS_FOURTH"]]
                excluded_words_fifth = row[self.const_gss_info["EXCLUDED_WORDS_FIFTH"]]
                target_worksheet = row[self.const_gss_info["ADD_WS"]]

                # デバッグ確認
                self.logger.info(f"処理開始： {index + 1}行目, 対象のWorksheet: {target_worksheet}")
                self.logger.info( f"検索キーワード: {search_word}\n 検索地域: {search_region}\n 対象Worksheet: {target_worksheet}" )
                self.logger.info(f"除外ワード1: {excluded_words_first}\n除外ワード2: {excluded_words_second}\n除外ワード3: {excluded_words_third}\n除外ワード4: {excluded_words_fourth}\n除外ワード5: {excluded_words_fifth}")


                # 2 新しいページを開いてHome画面を表示
                self.new_page.flow_jump_target_page( targetUrl=self.const_element["LOGIN_URL"] )

                # 3 Home画面をクリック
                self.click_element.clickElement( by=self.const_element["BY_2"], value=self.const_element["VALUE_2"])

                #5 検索窓にキーワードと地域を入力し、Enterキーで検索実行
                # キーワード入力
                self.click_element.clickClearInput( by=self.const_element["BY_1"], value=self.const_element["VALUE_1"], inputText=search_word)

                # 地域入力
                location = self.click_element.clickClearInput( by=self.const_element["BY_3"], value=self.const_element["VALUE_3"], inputText=search_region)

                # Enterキーで検索実行
                location.send_keys(Keys.RETURN)
                self.logger.info(f"検索キーワード: {search_word}、地域: {search_region} で検索を実行しました。")
                self.logger.info(f"EnterKeyを押して検索を実行しました。")

                # jsでのページ読み込み待ち
                self.wait.jsPageChecker(chrome=self.chrome, timeout=10)


                # 6
                # 表示された h2 タグのリストを取得
                h2_element_list = self.get_element.getElements(by=self.const_element["BY_4"], value=self.const_element["VALUE_4"])

                # 7
                # 各 h2 を順にクリックし、詳細画面へ遷移
                for h2_element in h2_element_list:
                    self.logger.info(f"現在の h2 要素のテキスト: {h2_element.text.strip()}")
                    self.random_sleep._random_sleep(2, 5)  # ランダムな待機時間を設定

                    h2_element.click()
                    # h2要素をクリックして詳細ページへ移動
                    self.click_element.filter_click_element(element=h2_element)

                    # 8
                    # 特定HTML要素からテキスト情報を抽出（BeautifulSoup）
                    parent_wrapper = self.get_html_text._get_wrapper( id_name=self.const_element["PARENT_ID"], )
                    parent_wrapper_text = parent_wrapper.get_text(separator="\n", strip=True)
                    self.logger.info(f"親要素のテキスト: {parent_wrapper_text[:100]}...")  # 最初の100文字だけ表示

                    # その中から「求人本文」だけを取り出す
                    children_wrapper = self.get_html_text._get_children_wrapper(
                        parent_wrapper=parent_wrapper,
                        class_name=self.const_element["CHILDREN_CLASS"],
                    )
                    children_wrapper_text = children_wrapper.get_text(separator="\n", strip=True)
                    self.logger.info(f"子要素のテキスト: {children_wrapper_text[:100]}...")  # 最初の100文字だけ表示


                # 9
                # スプシからbasePromptを取得
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

            # 15
            # TODO exe化させる
            # →本番用のAPIKEYが必要→差し替えて使う

            #! 全体テストを構築（main.pyを繰り返し実行するCode作成）
            # TODO 書込Formatを作成してなるべくあとから変更可能なように設計
            # TODO 通知はSlackにする→テストの日付ごとに分けるなどの設計を行ってわかりやすくなるようにする
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
            process_error_comment = (
                f"{self.__class__.__name__} 処理中にエラーが発生 {e}"
            )
            self.logger.error(process_error_comment)

        finally:
            # ✅ Chrome を終了
            self.chrome.quit()
            self.popup.popupCommentOnly(
                popupTitle=self.popup_cmt["POPUP_COMPLETE_TITLE"],
                comment=self.popup_cmt["POPUP_COMPLETE_MSG"],
            )

    # ----------------------------------------------------------------------------------

    def _delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"指定のファイルの削除を実施: {file_path}")

        else:
            self.logger.error(
                f"{self.__class__.__name__} ファイルが存在しません: {file_path}"
            )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == "__main__":

    test_flow = SingleProcess()
    # 引数入力
    test_flow._single_process()
