# Linux 比對兩目錄內的檔案差異


### **環境設定**

- Python 2.x



### 注意事項

1. 只比對目錄內的檔案,不比對子目錄
2. 只比對size大子,不比檔案內容



### **使用範例**

1. 參數說明

   ![](images/3.jpg)

2. 目錄pic、pic_backup反黄為差異

![](images/1.jpg)



2. 文字介面下執行

   ```shell
   # python backupfile_compare_by_python.py ~/pic ~/pic_backup png ppt
   ```

   

3. 執行結果,有差異為 "X" 符號

![](images/2.jpg)

