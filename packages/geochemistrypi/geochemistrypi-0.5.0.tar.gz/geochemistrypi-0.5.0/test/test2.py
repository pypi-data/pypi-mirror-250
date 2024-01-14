# import pandas as pd

# data = pd.read_excel("./Data_Regression.xlsx")
# df = data.iloc[:, 7:11]

# df_clean = df.dropna()

# df_clean.to_excel("./Data_Regression_Clean.xlsx", index=False)


class Parent:
    def __init__(self):
        self.name = "Howard"

    def get_name(self):
        return self.name
    
class Child(Parent):
    def __init__(self, age):
        super().__init__()
        self.age = age

    def get_age(self):
        return self.age

    def get_name(self):
        print(self.name + " is " + str(self.age) + " years old.")

child = Child(36)
child.get_name()