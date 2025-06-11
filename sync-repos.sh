#!/bin/bash

# 蓝奏云项目仓库同步脚本
# 用于自动同步GitHub和Gitee仓库

# 仓库URL
GITHUB_URL="https://github.com/uyevan/LanzouProDock.git"
GITEE_URL="https://gitee.com/uyevan/LanzouPro.git"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}===== 蓝奏云项目仓库同步工具 =====${NC}"
echo "1. 将更改推送到GitHub和Gitee"
echo "2. 仅推送到GitHub"
echo "3. 仅推送到Gitee"
echo "4. 从GitHub拉取并推送到Gitee"
echo "5. 从Gitee拉取并推送到GitHub"
echo -e "请选择操作 [1-5]: "

read choice

# 获取当前commit信息
echo -e "${YELLOW}请输入commit信息: ${NC}"
read commit_message

case $choice in
  1)
    # 同时推送到两个仓库
    echo -e "${GREEN}正在提交更改...${NC}"
    git add .
    git commit -m "$commit_message"
    
    echo -e "${GREEN}推送到GitHub...${NC}"
    git push origin master

    echo -e "${GREEN}添加Gitee远程仓库...${NC}"
    git remote set-url --add origin $GITEE_URL
    
    echo -e "${GREEN}推送到Gitee...${NC}"
    git push origin master
    
    # 恢复原始远程仓库设置
    git remote set-url origin $GITHUB_URL
    ;;
    
  2)
    # 仅推送到GitHub
    echo -e "${GREEN}正在提交更改...${NC}"
    git add .
    git commit -m "$commit_message"
    
    echo -e "${GREEN}推送到GitHub...${NC}"
    git remote set-url origin $GITHUB_URL
    git push origin master
    ;;
    
  3)
    # 仅推送到Gitee
    echo -e "${GREEN}正在提交更改...${NC}"
    git add .
    git commit -m "$commit_message"
    
    echo -e "${GREEN}推送到Gitee...${NC}"
    git remote set-url origin $GITEE_URL
    git push origin master
    
    # 恢复原始远程仓库设置
    git remote set-url origin $GITHUB_URL
    ;;
    
  4)
    # 从GitHub拉取并推送到Gitee
    echo -e "${GREEN}从GitHub拉取最新代码...${NC}"
    git remote set-url origin $GITHUB_URL
    git pull origin master
    
    echo -e "${GREEN}推送到Gitee...${NC}"
    git remote set-url origin $GITEE_URL
    git push origin master
    
    # 恢复原始远程仓库设置
    git remote set-url origin $GITHUB_URL
    ;;
    
  5)
    # 从Gitee拉取并推送到GitHub
    echo -e "${GREEN}从Gitee拉取最新代码...${NC}"
    git remote set-url origin $GITEE_URL
    git pull origin master
    
    echo -e "${GREEN}推送到GitHub...${NC}"
    git remote set-url origin $GITHUB_URL
    git push origin master
    ;;
    
  *)
    echo -e "${YELLOW}无效选择，退出脚本${NC}"
    exit 1
    ;;
esac

echo -e "${GREEN}操作完成!${NC}"
