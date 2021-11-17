#!/bin/bash

while getopts i:v:r: flag
do
    case "${flag}" in
        i) FOLDER_PATH=${OPTARG};;
        v) SDK_VERSION=${OPTARG};;
        r) GIT_REPOSITORY=${OPTARG};;
    esac
done

BRANCH_NAME="wip-build-$SDK_VERSION"
GIT_PATH="git@github.com:uclouvain/${GIT_REPOSITORY}.git"

echo "######## Push SDK ########";
echo "Folder path: $FOLDER_PATH";
echo "Git path: $GIT_PATH";
echo "Branch name: $BRANCH_NAME";

# Check if git folder exists
if [ ! -d "$FOLDER_PATH" ]; then
    echo "$FOLDER_PATH not found"
    exit 1
fi

# Go to git folder
cd ${FOLDER_PATH}

# Git push
git init
git checkout -b ${BRANCH_NAME}
git add *
git commit -m "Build $BRANCH_NAME"

# Add remote branch
git remote add origin $GIT_PATH

# Remove existing eventual delete branch on remote
git push origin --delete ${BRANCH_NAME}
git push origin ${BRANCH_NAME}