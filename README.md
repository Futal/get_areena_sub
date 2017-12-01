# Get Yle Areena subtitles

This small script download subtitles from Yle Areena, the website of the Finnish national broadcast company.
Its primary goal was to learn using Selenium and improving my skills in using Git and Python. It has be 
useful a couple of times when ripping my own DVDs if the OCR gave bad results for converting the DVD 
subtitles. It may also be useful if you want to create a corpus of standard Finnish and spoken Finnish 
for linguistic studies.


## Installation

Install Python 2, Urllib, Selenium and a web driver such as Firefox or Chromium. You may use Git to retrieve 
a copy of the script. For Debian Stretch on which the script has been tested, activate the non-free 
repositories and install the following two packages (the dependencies will take care that the other 
requirements are also installed):

    $ sudo apt install python-urllib3 firefoxdriver git
    $ git clone https://github.com/Futal/get_areena_sub.git

Copy the repository, for example if 
You just need a copy of get_areena_sub.py, Python 2, Selenium and a driver such as Firefox or Chromium.


## Execution

To run get_areena_sub with Python 2:

    $ python get_areena_sub.py <areena-url>

### `<areena-url>`:

 - For pages in Finnish, it has the form: `https://areena.yle.fi/<program-number>`
 - For pages in Swedish, it has the form: `https://arenan.yle.fi/<program-number>`


## Subtitle file name

Subtitles are saved in the program folder with the following name format:

    <program name> (<subtitle type>).<language code>.srt

### `<program name>`:

The program name is retrieve from the webpage h1 title under the video. 
It is in Finnish or Swedish depending on the URL used (areena or arenan).
The name may not be as broadcasted (e.g. on a Finnish page for a Yle Fem Swedish program).

### `<subtitle type>`:

Subtitle types are those displayed in the video player subtitle menu. The most
common types are:

 - `ohjelmatekstitys`: Finnish subtitles of a Finnish program
 - `käännöstekstitys`: Finnish translation subtitles 
 - `programtextning`: Swedish subtitles of a Swedish program
    
### `<language code>`:

It can be either:
 - `fi`: Finnish
 - `sv`: Swedish

### `srt` file extension:

Subtitles are saved in the SRT subtitle file format. It is the native file format
used by the video player and no conversion happens.


## Limitations

Subtitles can only be downloaded when you can watch the program with the HTML5 video player.
Hence subtitles can neither be downloaded when the program is only available with the Flash video
player, nor when the program is not available in your region (i.e. you do not have a Finnish IP
address).

