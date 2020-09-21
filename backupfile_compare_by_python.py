# coding:utf-8
import sys, glob, os, time

# 2018.5.8 linux交叉比對兩目錄檔案,缺檔,SIZE不一致 python版本 randi
# 2018.5.22 增加排除副檔名功能 randi
# 2018.6.6 增加檔案日期欄位 randi

# ex: python backupfile_compare_by_python.py 目錄1 目錄2 排除副檔名1 排除副檔名2 ...
# ex: python backupfile_compare_by_python.py /rman-local/20180419 /rman-backup/20180419 log txt

# 檢查參數必需要有2個以上
if len(sys.argv) < 2:
    print "Error: Not enough parameters"
    sys.exit("Error: Not enough parameters")

# 排除的副檔名list
exclude_ext = sys.argv[3:]

# 檢查目錄1存在否
local_path = sys.argv[1]
local_directory_exist = True
if not os.path.exists(local_path):
    print "Error: LOCAL {0} : No such file or directory".format(local_path)
    local_directory_exist = False

# 檢查目錄2存在否
backup_path = sys.argv[2]
backup_directory_exist = True
if not os.path.exists(backup_path):
    print "Error: BACKUP {0} : No such file or directory".format(backup_path)
    backup_directory_exist = False

# 抓取檔案資訊function
# 參數1: 路徑
# 參數2: 需排除的副檔名
# 回傳: size dict、檔案時間 dict
def getFileInfo(par_path, par_exclude_ext):
    os.chdir(par_path)
    par_path = os.getcwd()
    dict_size = {}
    dict_mtime = {}
    for file in glob.glob("*"):
        ff = "{0}/{1}".format(par_path, file)
        if os.path.isfile(ff):
            ext = os.path.splitext(ff)[-1].replace(".", "")
            if not ext in par_exclude_ext: # 排除副檔案
                dict_size[file] = os.path.getsize(ff)
                dict_mtime[file] = time.strftime("%Y-%m-%d %H:%M:%S",
                    time.localtime(os.path.getmtime(ff)))
    return dict_size, dict_mtime

# local的檔案名稱、size
local_size = {}
# local的檔案名稱、檔案時間
local_mtime = {}
if local_directory_exist:
    local_size, local_mtime = getFileInfo(local_path, exclude_ext)

# backup的檔案名稱、size
backup_size = {}
# backup的檔案名稱、檔案時間
backup_mtime = {}
if backup_directory_exist:
    backup_size, backup_mtime = getFileInfo(backup_path, exclude_ext)

# 將local、backup檔案名稱做聯集
list_filename = []
for key in local_size:
    list_filename.append(key)
for key in backup_size:
    if not key in list_filename:
        list_filename.append(key)

# 依檔名排序
list_filename.sort()

# 檔案不存在local目錄
local_diff = []
for item in list_filename:
    if local_size.get(item, "X") == "X":
        local_diff.append("X")
    else:
        local_diff.append(" ")

# 檔案不存在backup目錄
backup_diff = []
for item in list_filename:
    if backup_size.get(item, "X") == "X":
        backup_diff.append("X")
    else:
        backup_diff.append(" ")

# 比對size
# 檔案內容不同size相同,視為相同
size_diff = []
i = 0
for item in list_filename:
    # local、backup才需要比對size
    if local_diff[i] == " " and backup_diff[i] == " ":
        if int(local_size.get(item, 0)) == int(backup_size.get(item, 0)):
            size_diff.append(" ")
        else:
            size_diff.append("X")
    else:
        size_diff.append(" ")
    i += 1

# 2018.6.6 增加
# 檔案日期
backup_time = []
for item in list_filename:
    # 先取local
    if local_mtime.get(item, "X") != "X":
        backup_time.append(local_mtime.get(item))
        continue

    # local沒有取backup
    if backup_mtime.get(item, "X") != "X":
        backup_time.append(backup_mtime.get(item))
        continue

    # 其它
    backup_time.append("X                  ")

# 產生出比對結果
print "LOCAL     BACKUP    SIZE      MODIFICATION TIME    FILENAME                                          "
print "--------  --------  --------  -------------------  -------------------------------------------------"

if len(list_filename) == 0:
    print "No files found"
else:
    i = 0
    for item in list_filename:
        print "{0}         {1}         {2}         {3}  {4}".format(
            local_diff[i], backup_diff[i], size_diff[i], backup_time[i], item)
        i += 1

