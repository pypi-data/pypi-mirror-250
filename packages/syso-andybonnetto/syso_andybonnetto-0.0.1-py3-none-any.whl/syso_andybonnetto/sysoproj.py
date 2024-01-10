import pandas as pd
import numpy as np
import os


class SysoProj():
    
    def __init__(self,project_path, table_name = "Table_0" ,*args, **kwargs):
        super(SysoProj, self).__init__(*args, **kwargs)        
        self.project_path = project_path        
        self.set_table_name(table_name)
        
    def log(self, name, column_name, value = True):
        self._load_dataframe()
        
        if name in list(self.df["Names"]) and column_name in self.df.columns:
            self.df.loc[self.df["Names"] == name, column_name] = value
            
        elif name in list(self.df["Names"]) and column_name not in self.df.columns:
            new_col = [np.nan]*len(self.df.index)
            new_col[list(self.df["Names"]).index(name)] = value
            self.df.insert(len(self.df.columns),column_name,new_col, allow_duplicates=False)
            
        elif name not in list(self.df["Names"]) and column_name in self.df.columns:
            new_row = {col : np.nan for col in self.df.columns}
            new_row[column_name] = value
            new_row["Names"] = name
            self.df.loc[len(self.df)] = new_row
            self.df.index = self.df.index + 1
        
        elif not name in list(self.df["Names"]) and column_name not in self.df.columns:
            new_col = [np.nan]*(len(self.df.index))
            self.df.insert(len(self.df.columns),column_name, new_col, allow_duplicates=False)
            new_row = {col : np.nan for col in self.df.columns}
            new_row[column_name] = value
            new_row["Names"] = name
            self.df.loc[len(self.df)] = new_row
            self.df.index = self.df.index + 1
        
        self._save_dataframe()
        # print(f"Set {name} at {column_name} to {value}")
    
    def set_table_name(self, table_name):
        self.table_name = table_name
        self._load_dataframe()
    
    def _load_dataframe(self):
        
        if not os.path.exists(os.path.join(self.project_path, self.table_name + ".csv")):
            # Create empty dataframe
            df = pd.DataFrame(columns=["Names"], index = [np.nan])
            df.to_csv(os.path.join(self.project_path, self.table_name + ".csv"), index=False)
        
        self.df = pd.read_csv(os.path.join(self.project_path, self.table_name + ".csv"))
        
    def _save_dataframe(self):
        self.df.to_csv(os.path.join(self.project_path, self.table_name + ".csv"), index = False)
        
    def _update_dataframe(self):
        pass