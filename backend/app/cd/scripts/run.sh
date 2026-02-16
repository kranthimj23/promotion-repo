#!/bin/bash
# Run Command for main.py Orchestration Script

# Set these variables with your values
LOWER_ENV="dev"
HIGHER_ENV="sit"
PROMOTIONAL_REPO="https://github.com/kranthimj23/promotion-repo.git"
NEW_VERSION="2.0.0"
SERVICES_LIST="services_list.txt"
PROMOTE_BRANCH_X_1="release/1.0.0"

# Run the command
python main.py "$LOWER_ENV" "$HIGHER_ENV" "$PROMOTIONAL_REPO" "$NEW_VERSION" "$SERVICES_LIST" "$PROMOTE_BRANCH_X_1"

