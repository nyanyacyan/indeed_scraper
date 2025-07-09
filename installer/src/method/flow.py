# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Volumes/にゃにゃちゃんHD/Project_file/indeed_scraper/installer/src"
# export PYTHONPATH="/Users/nyanyacyan/Desktop/Project_file/indeed_scraper/installer/src"
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, asyncio, json
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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
from method.base.AI.AiOrder import ChatGPTOrder

# const
from method.const_element import (
    GssInfo,
    ErrCommentInfo,
    PopUpComment,
    Element,
    ChatgptInfo,
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
        self.chat_gpt_info = ChatgptInfo.INDEED.value

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
        self.chat_gpt_order = ChatGPTOrder()

    # **********************************************************************************
    # ----------------------------------------------------------------------------------

    async def _single_process(self):
        """各プロセスを実行する"""
        try:
            # ログインする
            # 手動ログイン# 1
            self.chrome.get(self.const_element["LOGIN_URL"])

            # ユーザーに既存でブラウザを開いていたら閉じるようにアナウンス

            # 対象のページが開いているかどうかを確認
            # ログイン後、検索窓が表示されるまで最大300秒待機
            self.wait.canWaitClick(by=self.const_element["BY_1"], value=self.const_element["VALUE_1"], timeout=300)

            # Googleスプレッドシートから情報取得
            # - 「マスター」シートへアクセス
            target_df = self.get_gss_df_flow.process( worksheet_name=self.const_gss_info["MASTER_WS"] )

            rows_count = len(target_df)
            self.logger.info(f"取得した行数: {rows_count} 行")

            row_count = 0

            # - 1行目から以下の情報を取得
            target_df.iterrows()
            for index, row in target_df.iterrows():
                row_count += 1
                self.logger.info(f"処理中の行: {row_count} / {rows_count} 行目")

                # 各行の情報を取得
                search_word = row[self.const_gss_info["SEARCH_WORDS"]]
                search_region = row[self.const_gss_info["SEARCH_REGION"]]
                excluded_words_first = row[self.const_gss_info["EXCLUDED_WORDS_FIRST"]]
                excluded_words_second = row[self.const_gss_info["EXCLUDED_WORDS_SECOND"]]
                excluded_words_third = row[self.const_gss_info["EXCLUDED_WORDS_THIRD"]]
                excluded_words_fourth = row[self.const_gss_info["EXCLUDED_WORDS_FOURTH"]]
                excluded_words_fifth = row[self.const_gss_info["EXCLUDED_WORDS_FIFTH"]]
                target_worksheet = row[self.const_gss_info["ADD_WS"]]
                get_mode = row[self.const_gss_info["SELECT_MODE"]]

                # デバッグ確認
                self.logger.info(f"処理開始： {index + 1}行目, 対象のWorksheet: {target_worksheet}")
                self.logger.info( f"検索キーワード: {search_word}\n 検索地域: {search_region}\n 対象Worksheet: {target_worksheet}" )
                self.logger.info(f"除外ワード1: {excluded_words_first}\n除外ワード2: {excluded_words_second}\n除外ワード3: {excluded_words_third}\n除外ワード4: {excluded_words_fourth}\n除外ワード5: {excluded_words_fifth}")
                self.logger.info(f"抽出モード: {self.const_gss_info['ALL_PAGES']} を選択しました。")


                self.wait.canWaitClick(by=self.const_element["BY_1"], value=self.const_element["VALUE_1"], timeout=300)

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

                # 対象のデータフレームを取得
                check_df = self.get_gss_df_flow.no_filter_process( worksheet_name= target_worksheet )

                # ChatGPTのWSのデータフレームを取得
                chatgpt_df = self.get_gss_df_flow.no_filter_process(self.const_gss_info["CHATGPT_WS"] )

                count = 1
                # 各 h2 を順にクリックし、詳細画面へ遷移
                gss_write_dict_list = []  # スプレッドシートに書き込むための辞書リスト
                while True:

                    # 表示された h2 タグのリストを取得
                    h2_element_list = self.get_element.getElements(value=self.const_element["VALUE_4"])
                    [self.logger.info(f"取得した h2 要素: {h2_element.text.strip()}") for h2_element in h2_element_list]

                    for i, h2_element in enumerate(h2_element_list):
                        self.logger.info(f"現在 {count} / {len(h2_element_list)} 回目の実施")

                        # 各 h2 要素のテキストを取得
                        h2_title = h2_element.text.strip()
                        self.logger.info(f"現在の h2 要素のテキスト: {h2_title}")
                        self.random_sleep._random_sleep(2, 5)  # ランダムな待機時間を設定

                        # 現在のスプシに同じタイトルがないかを確認する
                        if check_df is not None and not check_df.empty:
                            self.logger.info(f"スプレッドシート '{target_worksheet}' にデータが存在します。")
                            titles = check_df[self.const_gss_info["H2_TITLE"]].tolist()  # タイトルのリストを取得

                            if h2_title in titles:
                                self.logger.warning(f"タイトル '{h2_title}' はすでに存在します。次の h2 へ移動します。")
                                count += 1
                                continue
                        else:
                            self.logger.info(f"スプレッドシート '{target_worksheet}' は空です。新しいデータを追加します。")

                        # h2 要素をクリックして詳細ページへ遷移
                        self.click_element.filter_click_element(element=h2_element)
                        self.random_sleep._random_sleep(2, 5)  # ランダムな待機時間を設定

                        # 現在のページのURLを取得
                        current_url = self.chrome.current_url
                        self.logger.info(f"現在のURL: {current_url}")

                        # 特定HTML要素からテキスト情報を抽出（BeautifulSoup）
                        parent_wrapper = self.get_html_text._get_wrapper( id_name=self.const_element["PARENT_ID"], )# 最初の100文字だけ表示

                        # その中から「求人本文」だけを取り出す
                        children_wrapper = self.get_html_text._get_children_wrapper( parent_wrapper=parent_wrapper, class_name=self.const_element["CHILDREN_CLASS"], )
                        result_text = children_wrapper.get_text(separator="\n", strip=True)
                        self.random_sleep._random_sleep(2, 5)  # ランダムな待機時間を設定

                        # 9 スプシからbasePromptを取得
                        # 基本プロンプト

                        base_prompt = chatgpt_df[self.const_gss_info["BASE_PROMPT_COL"]].iloc[0]

                        # 除外プロンプト
                        except_prompt = chatgpt_df[self.const_gss_info["EXCEPT_PROMPT_COL"]].iloc[0]

                        # 不備プロンプト
                        missing_prompt = chatgpt_df[self.const_gss_info["MISSING_PROMPT_COL"]].iloc[0]

                        # 除外ワードをまとめる
                        excluded_words = [
                            excluded_words_first,
                            excluded_words_second,
                            excluded_words_third,
                            excluded_words_fourth,
                            excluded_words_fifth,
                        ]

                        # 除外プロンプトに追記
                        for i, word in enumerate(excluded_words, start=1):
                            if word:
                                except_prompt += f"\n除外ワード{i}: {word}"

                        # プロンプトを結合
                        complete_prompt = f"{base_prompt}\n{except_prompt}"
                        self.logger.debug(f"完成したプロンプト: {complete_prompt}")

                        response_msg = await self.chat_gpt_order.resultOutput(
                            prompt=complete_prompt,
                            fixedPrompt=missing_prompt,
                            endpointUrl=self.chat_gpt_info["CHATGPT_API_URL"],
                            model=self.chat_gpt_info["CHATGPT_MODEL"],
                            apiKey=self.chat_gpt_info["CHATGPT_API_KEY"],
                            maxTokens=4000,
                            maxlen=100000,
                        )

                        self.logger.info(f"ChatGPTからのレスポンス: {response_msg}, {type(response_msg)}型")

                        # レスポンスがNoneの場合、再リクエストを行う
                        if response_msg is None:
                            self.logger.info("ChatGPTからのレスポンスが None です。再リクエストを行います。")

                            # 再リクエストを行う
                            response_msg = await self.chat_gpt_order.resultOutput(
                                prompt=complete_prompt,
                                fixedPrompt=missing_prompt,
                                endpointUrl=self.chat_gpt_info["CHATGPT_API_URL"],
                                model=self.chat_gpt_info["CHATGPT_MODEL"],
                                apiKey=self.chat_gpt_info["CHATGPT_API_KEY"],
                                maxTokens=4000,
                                maxlen=100000,
                            )

                        # 最初の文字が { でない場合は、辞書ではない可能性が高い
                        if not response_msg.startswith("{"):
                            return None  # 再リクエストフラグとしてNoneを返す

                        if response_msg == "なし":
                            self.logger.info("ChatGPTからのレスポンスが 'なし' です。次の h2 へ移動します。")
                            count += 1  # カウントを増やす
                            continue  # 次の h2 へ移動

                        if isinstance(response_msg, str):
                            response_msg_dict = json.loads(response_msg)
                            self.logger.info(f"ChatGPTレスポンスを辞書形式に変換: {response_msg_dict}, {type(response_msg_dict)}型")
                        else:
                            response_msg_dict = response_msg
                            self.logger.info(f"ChatGPTレスポンスはすでに辞書形式: {response_msg_dict}")

                        # 辞書の項目に追加

                        response_msg_fix = {
                            self.const_gss_info["ADD_DATE"]: self.date_only_stamp,
                            self.const_gss_info["H2_TITLE"]: h2_title,
                            self.const_gss_info["SALARY"]: response_msg_dict.get("勤務地", ""),
                            self.const_gss_info["WORKING_HOURS"]: response_msg_dict.get("給料", ""),
                            self.const_gss_info["PAGE_LINK"]: response_msg_dict.get("勤務時間", ""),
                            self.const_gss_info["WORK_PLACE"]: current_url,
                        }

                        self.logger.info(f"レスポンス辞書に追加された情報: {response_msg_fix}")

                        gss_write_dict_list.append(response_msg_fix)

                        self.logger.info(f"現在 {count} / {len(h2_element_list)} 回目、完了した h2 要素のタイトル: {h2_title}")

                        self.logger.warning(f"【{count}つ目】処理完了\n現在のリストの中身: \n{gss_write_dict_list}")
                        count += 1  # カウントを増やす
                        break # TODO 書込テスト
                        # continue  # 次の h2 へ移動



                    self.logger.info(f"全ての h2 要素の処理が完了しました。")
                    self.logger.info(f"スプレッドシートに書き込むデータ: {gss_write_dict_list}")

                    # 書き込むWorksheetの取得
                    # 書き込むA列の最初のNoneの行数を取得
                    self.logger.info(f"check_df: {check_df}")

                    if check_df is not None and not check_df.empty:
                        len_check_df = len(check_df)
                        self.logger.info(f"対象のWorksheet '{target_worksheet}' の行数: {len_check_df}")
                        none_cell_num = len_check_df + 2
                        write_cell = "A" + str(none_cell_num)

                    else:
                        # 対象のWorksheetが空の場合、最初の行に書き込む
                        write_cell = "A2"

                    # 下記をSpreadsheet_write.pyに定義
                    # set_with_dataframe(ws, df, row=next_row, include_column_header=False)
                    self.gss_write.write_dict_list(
                        gss_info=self.const_gss_info,
                        worksheet_name=target_worksheet,
                        cell=write_cell,
                        input_data=gss_write_dict_list,
                    )

                    self.logger.info(f"スプレッドシート '{target_worksheet}' にデータを書き込みました。セル: {write_cell}")

                    # 抽出モードによる処理の分岐
                    if get_mode == self.const_gss_info["ONE_PAGE"]:
                        self.logger.info(f"抽出モード: {self.const_gss_info['ONE_PAGE']} を選択しました。1ページのみを対象に処理を行います。")
                        break

                    elif get_mode == self.const_gss_info["ALL_PAGES"]:
                        # 全ページを対象に処理を行う
                        self.logger.info(f"抽出モード: {self.const_gss_info['ALL_PAGES']} を選択しました。全ページを対象に処理を行います。")
                        # ここで次のページへ移動する処理を追加
                        try:
                            next_page_button = self.get_element.getElement( value=self.const_element["NEXT_BTN_VALUE"], )
                            if next_page_button:
                                next_page_button.click()
                                self.logger.info("次のページボタンをクリックしました。")
                                self.random_sleep._random_sleep(2, 5)

                                try:
                                    modal_close_element = self.get_element.getElement(value=self.const_element["MODAL_CLOSE_BTN"])
                                    modal_close_element.click()
                                    self.logger.info("モーダルウィンドウを閉じました。")
                                except NoSuchElementException:
                                    self.logger.info("モーダルウィンドウは表示されていません。")

                        except NoSuchElementException:
                            self.logger.warning("次のページボタンがないため、処理を終了します。")
                            break

                    else:
                        self.logger.error(f"抽出モードが不正です: {get_mode}1ページのみで終了します。")
                        break

                self.logger.info(f"全ての h2 要素の処理が完了しました。スプレッドシート '{target_worksheet}' にデータを書き込みました。")
                self.logger.info(f"【{row_count} / {rows_count} 処理完了】次の行の処理に進みます")

            # 15
            # TODO exe化させる
            # →本番用のAPIKEYが必要→差し替えて使う

            #! 全体テストを構築（main.pyを繰り返し実行するCode作成）
            # TODO 書込Formatを作成してなるべくあとから変更可能なように設計
            # TODO 通知はSlackにする→テストの日付ごとに分けるなどの設計を行ってわかりやすくなるようにする


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

    # test_flow = SingleProcess()
    # # 引数入力
    # test_flow._single_process()

    process = SingleProcess()
    asyncio.run(process._single_process())
