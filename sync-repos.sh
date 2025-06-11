#!/bin/bash

# 蓝奏云项目仓库同步脚本
# 用于自动同步GitHub和Gitee仓库

# 仓库URL和分支设置
GITHUB_URL="https://github.com/uyevan/LanzouProDock.git"
GITEE_URL="https://gitee.com/uyevan/LanzouPro.git"
GITHUB_BRANCH="master"
GITEE_BRANCH="dev"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查操作是否成功
check_success() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}操作失败，请检查错误信息${NC}"
        exit 1
    fi
}

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

# 询问是否强制推送
echo -e "${YELLOW}是否强制推送(覆盖远程仓库)? (y/n): ${NC}"
read force_push

# 设置强制推送参数
if [[ "$force_push" == "y" || "$force_push" == "Y" ]]; then
    FORCE_FLAG="-f"
    echo -e "${RED}警告: 强制推送可能会覆盖远程仓库的更改${NC}"
else
    FORCE_FLAG=""
fi

# 获取当前分支
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${GREEN}当前分支: ${CURRENT_BRANCH}${NC}"

case $choice in
  1)
    # 同时推送到两个仓库
    echo -e "${GREEN}正在提交更改...${NC}"
    git add .
    git commit -m "$commit_message" || echo -e "${YELLOW}没有要提交的更改或提交失败${NC}"
    
    echo -e "${GREEN}推送到GitHub(${GITHUB_BRANCH})...${NC}"
    git remote set-url origin $GITHUB_URL
    git push $FORCE_FLAG origin ${CURRENT_BRANCH}:${GITHUB_BRANCH}
    check_success
    
    echo -e "${GREEN}推送到Gitee(${GITEE_BRANCH})...${NC}"
    git remote set-url origin $GITEE_URL
    git push $FORCE_FLAG origin ${CURRENT_BRANCH}:${GITEE_BRANCH}
    check_success
    
    # 恢复原始远程仓库设置
    git remote set-url origin $GITHUB_URL
    ;;
    
  2)
    # 仅推送到GitHub
    echo -e "${GREEN}正在提交更改...${NC}"
    git add .
    git commit -m "$commit_message" || echo -e "${YELLOW}没有要提交的更改或提交失败${NC}"
    
    echo -e "${GREEN}推送到GitHub(${GITHUB_BRANCH})...${NC}"
    git remote set-url origin $GITHUB_URL
    git push $FORCE_FLAG origin ${CURRENT_BRANCH}:${GITHUB_BRANCH}
    check_success
    ;;
    
  3)
    # 仅推送到Gitee
    echo -e "${GREEN}正在提交更改...${NC}"
    git add .
    git commit -m "$commit_message" || echo -e "${YELLOW}没有要提交的更改或提交失败${NC}"
    
    echo -e "${GREEN}推送到Gitee(${GITEE_BRANCH})...${NC}"
    git remote set-url origin $GITEE_URL
    git push $FORCE_FLAG origin ${CURRENT_BRANCH}:${GITEE_BRANCH}
    check_success
    
    # 恢复原始远程仓库设置
    git remote set-url origin $GITHUB_URL
    ;;
    
  4)
    # 从GitHub拉取并推送到Gitee
    echo -e "${GREEN}从GitHub拉取最新代码(${GITHUB_BRANCH})...${NC}"
    git remote set-url origin $GITHUB_URL
    git fetch origin ${GITHUB_BRANCH}
    git merge origin/${GITHUB_BRANCH} || echo -e "${YELLOW}合并失败，可能需要手动解决冲突${NC}"
    
    echo -e "${GREEN}推送到Gitee(${GITEE_BRANCH})...${NC}"
    git remote set-url origin $GITEE_URL
    git push $FORCE_FLAG origin ${CURRENT_BRANCH}:${GITEE_BRANCH}
    check_success
    
    # 恢复原始远程仓库设置
    git remote set-url origin $GITHUB_URL
    ;;
    
  5)
    # 从Gitee拉取并推送到GitHub
    echo -e "${GREEN}从Gitee拉取最新代码(${GITEE_BRANCH})...${NC}"
    git remote set-url origin $GITEE_URL
    git fetch origin ${GITEE_BRANCH}
    git merge origin/${GITEE_BRANCH} || echo -e "${YELLOW}合并失败，可能需要手动解决冲突${NC}"
    
    echo -e "${GREEN}推送到GitHub(${GITHUB_BRANCH})...${NC}"
    git remote set-url origin $GITHUB_URL
    git push $FORCE_FLAG origin ${CURRENT_BRANCH}:${GITHUB_BRANCH}
    check_success
    ;;
    
  *)
    echo -e "${YELLOW}无效选择，退出脚本${NC}"
    exit 1
    ;;
esac

echo -e "${GREEN}操作完成!${NC}"
