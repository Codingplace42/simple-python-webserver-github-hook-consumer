LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse origin/master)
echo $LOCAL_HASH
echo $REMOTE_HASH