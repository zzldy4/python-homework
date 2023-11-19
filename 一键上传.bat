chcp 65001
@echo off
cd C:\Users\zzldy\Desktop\python homework
git add .
git commit -m "实验"
git pull origin main
git push -u origin main
@echo 完成！按 Enter 键退出...
@pause >nul