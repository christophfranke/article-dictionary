#!/bin/bash

# Define directory variables
TARGET_DIRECTORY="/root/live"
LOG_FILE="/root/git-receive.log"
UPDATE_SCRIPT="/root/update-containers.sh"
BRANCH_NAME="live"

cp "$TARGET_DIRECTORY/scripts/update-containers" "$UPDATE_SCRIPT"
chmod a+x "$UPDATE_SCRIPT"

while read oldrev newrev refname
do
    # Check if the received branch is the target branch
    if [ "$refname" = "refs/heads/$BRANCH_NAME" ]; then

        # Redirect output to the log file
        exec >> "$LOG_FILE" 2>&1

        # Clear the target directory
        rm -rf "$TARGET_DIRECTORY"/*

        # Copy the content of the target branch to the directory
        git --work-tree="$TARGET_DIRECTORY" checkout -f "$BRANCH_NAME" -- .

        # Get the commit message of the new revision
        commit_message=$(git log --format=%B -n 1 "$newrev")
        echo "[$(date)] $BRANCH_NAME branch content copied to $TARGET_DIRECTORY. Commit message: '$commit_message'"

        # Run the update script in the background
        "$UPDATE_SCRIPT" &
    fi
done
