# youtubePlaylistDownloader

## Usage

```
python3 audio_getter.py
```

then it will prompt for playlist url

## SETUP INSTRUCTIONS

### 1. Installing homebrew

Open a new terminal window and enter the following: 

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Once homebrew finishes installing, to update your PATH enter the following: 

```
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```


### 2. Installing python3 from homebrew
In your terminal window, type: 

```
 brew install python
```

To check if the install went correctly, in your terminal, type:

```
python --version
```

If you see
```
Python 3.8.10 [or later]
```


you are all set!

### 3. Set up pipenv
Run the following in the terminal to install pipenv globaly.
```
sudo -H pip install -U pipenv
```

Now, after cloning the repository, navigate to the repository directory in your terminal and then enter the command: 
```
pipenv install
```

You will also new to have ffmpeg installed to run the audio_getter.py.
To do this run:
```
brew install ffmpeg
```
