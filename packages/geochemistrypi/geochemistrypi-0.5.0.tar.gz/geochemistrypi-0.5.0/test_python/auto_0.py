import pandas as pd
import pyautogui
import pyperclip
import time
import os

class GpyTest(object):
    test_words = ['不是内部或外部命令', 'Traceback (most recent call last)', 'ValueError']
    def __init__(self, data, i):
        self.data = data
        self.training_data = str(self.data.loc[i, 'training_data'])
        self.inference_data = str(self.data.loc[i, 'inference_data'])
        self.start_words = f"geochemistrypi data-mining --training {self.training_data} --inference {self.inference_data}"
        self.copied_text = ""
        self.choice_content = ""
        self.num = i

    def start_cmd(self):
        print(self.start_words)
        time.sleep(3)
        self.copied_text = ""
        pyautogui.typewrite("cls")
        self.enter_press(1)
        pyperclip.copy(str(self.start_words))
        pyautogui.hotkey('ctrl', 'v')
        self.enter_press(1)

    def choice(self, content):
        pyautogui.typewrite(str(content))
        self.choice_content = str(content)
        self.enter_press(1)


    def record_cmd(self):
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        self.copied_text = str(self.copied_text) + "\n" + pyperclip.paste()

    def enter_press(self, i):
        for i in range(i):
            self.record_cmd()
            pyautogui.press("enter")

    def test_order(self):
        self.start_cmd()
        self.enter_press(1)
        time.sleep(8)
        self.choice(self.data.loc[i, 'pre'])
        self.choice(self.data.loc[i, 'new'])
        self.choice(self.data.loc[i, 'run'])
        self.enter_press(1)

        self.choice(self.data.loc[i, 'world_map'])
        self.enter_press(1)

        self.choice(self.data.loc[i, 'data_select'])
        self.enter_press(4)

        self.choice(self.data.loc[i, 'feature'])
        self.enter_press(1)

        self.choice(self.data.loc[i, 'mode_select'])
        self.enter_press(1)

        self.choice(self.data.loc[i, 'x_select'])
        self.enter_press(1)
        self.choice(self.data.loc[i, 'scaling'])
        if str(self.choice_content) == str(1):
            self.choice(self.data.loc[i, 'strategy'])
        else:
            pass
        self.enter_press(1)
        self.choice(self.data.loc[i, 'y_select'])
        self.enter_press(1)

        self.choice(self.data.loc[i, 'feature_selection'])
        if str(self.choice_content) == str(1):
            self.choice(self.data.loc[i, 'fstrategy'])
            self.choice(self.data.loc[i, 'original_features'])
        else:
            pass
        self.enter_press(1)
        self.choice(self.data.loc[i, 'test_ratio'])
        self.enter_press(1)

        self.choice(self.data.loc[i, 'model'])
        self.enter_press(1)

        # 自动调参选择
        self.choice(self.data.loc[i, 'auto_learning'])
        self.enter_press(1)
        if str(self.choice_content) == str(2):
            self.enter_press(1)
            self.choice(self.data.loc[i, 'customize_label'])
            if str(self.choice_content) == str(1):
                self.choice(self.data.loc[i, 'cus_strategy'])
                if str(self.choice_content) == str(1):
                    pass
                elif str(self.choice_content) == str(2):
                    self.choice(self.data.loc[i, 'cus_strategy_content'])
                elif str(self.choice_content) == str(3):
                    self.choice(self.data.loc[i, 'cus_strategy_content'])

            self.enter_press(1)
            self.choice(self.data.loc[i, 'sample_balance'])
            if str(self.choice_content) == str(1):
                self.choice(self.data.loc[i, 'sb_strategy'])
                if str(self.choice_content) == str(1):
                    pass
                elif str(self.choice_content) == str(2):
                    pass
                elif str(self.choice_content) == str(3):
                    pass
            self.enter_press(1)

            self.choice(int(self.data.loc[i, 'estimators']))
            self.choice((self.data.loc[i, 'learning_rate']))
            self.choice(int(self.data.loc[i, 'max_depth']))
            self.choice((self.data.loc[i, 'subsample']))
            self.choice(int(self.data.loc[i, 'colsample_bytree']))
            self.choice(int(self.data.loc[i, 'alpha']))
            self.choice(int(self.data.loc[i, 'lambda']))
            self.enter_press(4)
        else:
            self.enter_press(1)
            self.choice(self.data.loc[i, 'customize_label'])
            if str(self.choice_content) == str(1):
                self.choice(self.data.loc[i, 'cus_strategy'])
            self.enter_press(1)
            self.choice(self.data.loc[i, 'sample_balance'])
            if str(self.choice_content) == str(1):
                self.choice(self.data.loc[i, 'sb_strategy'])
            self.enter_press(4)

        for k in GpyTest.test_words:
            if k in self.copied_text:
                self.data.loc[i, 'result'] = '失败'
            else:
                self.data.loc[i, 'result'] = '成功'
        self.data.loc[i, 'test_document'] = str(f"Test-{self.num}.txt")
        # self.pd = pd.DataFrame(self.pd)
        self.data.to_excel("Test_Result.xlsx")

        file_path = f"./test_document/Test-{self.num}.txt"
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f"./test_document/Test-{self.num}.txt", 'w', encoding='utf-8') as f:
            print(self.copied_text, file=f)
        # con = pd.DataFrame(self.copied_text)
        # con.to_csv(f"Test-{self.num}.txt", sep="\t", index=False)

        # 时间戳标记
        # time_now = int(time.time())
        # time_local = time.localtime(time_now)
        # dt = str(time.strftime("%Y-%m-%d %H:%M:%S", time_local)).replace(" ", "")
        # print(dt)


if __name__ == "__main__":

    data = pd.read_excel("C:/Users/Jin/Desktop/1203/test_flow/test.xlsx")
    for i in range(len(data)):
        test = GpyTest(data, i)
        test.test_order()

