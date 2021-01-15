# Change Log

## Table of Contents:

- [Version 0.0.1](#15012021---001)

## 15/01/2021 - 0.0.1

- improved readability of the get help function in the Data module
- added a custom exception for when a bot has an illegal presence
- added a function in the framework to generate embeds more easily
- added a cog for providence - provCog
- added two commands to the cog - !help and !userinfo
- combined both on_message callback, and the cog system to handle all kinds of messages
- added a setup override for the providence bot and loaded its cog in it
- removed redundant help command from providence (already covered in the cog)
- commented out the announcement system. It gets annoying after a while. will be back at launch.
- added a change log markdown file