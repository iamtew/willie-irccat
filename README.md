willie-irccat
=============

Willie modules to provide irccat-like functionality to your IRC bot. Inspired by the Last.fm bot from here: https://github.com/RJ/irccat

Usage:
------

1. Clone repository: `git clone https://github.com/iamtew/willie-irccat ~/.willie/irccat`
2. Add to your Willie config: `extra = /home/yourname/.willie/irccat`

Send a string to the listening port starting with the channel name, for example:
```
echo "#chatroom The time is $(date +'%T')" | ncat -4 localhost 5234
```

