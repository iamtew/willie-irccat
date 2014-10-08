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

You can also send to a specific user by prefixing the message with an `@`, like so:
```
echo "@iamtew You're the best :)" | ncat -4 localhost 5234
```

And you can specify multiple targets, like this:
```
echo "#chatroom,#otherchannel multi-chat" | ncat -4 localhost 5234
```

