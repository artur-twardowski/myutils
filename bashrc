if [ "$color_prompt" = yes ]; then
    PS1='$(PS1_indicators)\n$(PS1_stty) $(PS1_git_branch)\n\[\033[38;5;208m\]\w\[\033[00m\]\n\$ '
else
    PS1='\w\n\$ '
fi

PS1_git_branch() {
    BRANCH_NAME=`git branch --show-current 2>/dev/null`
    if [ $? == 0 ]; then
        REPO_ENDPOINT=`git remote -v | grep origin | grep fetch | awk '{print $2}'`
        REPO_NAME=`basename "$REPO_ENDPOINT" | sed -e 's/.git$//'`
        echo "$REPO_NAME" | grep "https://" > /dev/null
        if [ $? == 0 ]; then
            echo -ne "\x1b[38;5;81m\u2095"
        else
            echo -ne "\x1b[38;5;208m\u209b"
        fi

        echo -ne "\x1b[38;5;48m$REPO_NAME"

        echo -e "\x1b[38;5;45m/$BRANCH_NAME"
    fi
}

PS1_stty() {
    DIMENSIONS=`stty -a | grep "rows" | sed -e 's/;//g' | awk '{print $7 "x" $5}'`
    echo -e "\x1b[38;5;171m$DIMENSIONS\x1b[0m"
}

PS1_indicators() {
    :
}

