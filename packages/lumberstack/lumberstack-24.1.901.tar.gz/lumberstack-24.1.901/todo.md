[ ] add 'use local if debugging else use gmt' option to global init?
[ ] custom exceptions
    [ ] if cannot convert msg to string
[ ] granular handler control
    [ ] ability to set log file and console log_level on global_init
    [ ] add custom handlers built off Handler class
        [ ] create DiscordHandler with basic options
            * webhook
            * timezone (should default to global if not provided)
            * loglevel (^^^)
            * formatting (^^^)
            * ... anything else?
        [ ] add Teams the same way