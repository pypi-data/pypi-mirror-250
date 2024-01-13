# fssh 🐟

> pronounced "fish"

A fast SSH tool for UT Austin CS students.

# Introduction

SSH is tedious. Go to host machine list. Find optimal machine. Enter command. Interact. Login.

It could be faster.

![fssh-demo](https://github.com/migopp/fssh/assets/128272843/7f4c80c1-f871-438b-b1ee-99a1108de418)

# Installation

1. `pip install fssh`
2. run `fssh-setup`
3. profit 💰

# Usage

```
fssh
```

The above commmand will do __everything__ for you.

If that's not what you want, you can opt to add in the `-p` flag to print the optimal machine (it will also copy the correct command to your clipboard, i.e., `ssh <YOUR UTCS USERNAME>@<OPTIMAL HOST>.cs.utexas.edu`).

`fssh -h` for help (there's not a lot, it's pretty simple).

# UTCS Credentials

Part of SSH is entering your UTCS username and SSH passkey—fssh cannot bypass this, as it sadly is not magic. As such, to fully utilize fssh, [the script needs access to this information somehow](https://github.com/migopp/fssh/blob/main/src/fssh/__main__.py).

I have implemented this through a setup script that logs this information to your respective shell profile (where you keep your API keys and such). This information is recorded [_solely_](https://github.com/migopp/fssh/blob/main/src/fssh/setup.py) on your local machine.

Still worried? You can bypass the passphrase component in `fssh-setup`, doing so will net you the `fssh -p` functionality when you call `fssh` by default. You will still need to give your username, but that's public information anyhow.

# Terminal Usage

The full `fssh` functionality works great for most terminals. Not so much for some fancier ones (_cough, cough Warp_). You may not get full functionality of your fancy terminal emulator. In such cases, the `fssh -p` command will probably do you best.
