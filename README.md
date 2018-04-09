# Register
Register/Signup tool for Timeline Emulator. Server back-end by Python.

# Usage
```
python TimelineSignup.py
```
or to get help
```
python TimelineSignup.py -h
```
or to set informations like mysql email server, recaptcha etc
```
python TimelineSignup.py -u "root" -p "" -db "times-cp"
```
and so on

# Setup
Put the files on `htdocs/signup` or any directory which lets you access `localhost/signup` web-directory. Then visit [http://localhost/signup](http://localhost/signup) to view the signup page.

**If you wish to host this to a website** make sure to change the domain `localhost` to your domain name in `TimelineSignup.py` and `index.html`. You are done.
