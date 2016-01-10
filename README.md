Rdnzl, my meta-cv
============================

Hi, my name is Florent Pastor. 
This is my meta-cv, which is a website coded with Django and Dart containing an interactive CV, 
and which code also show my skills with those two technologies.

Check it out on ~~http://heymistertree.eu~~ (website temporarily down).

This document will walk you through the project, specifying which of my skills were used for its development.

Git
---

I am commited to clean git repos, with commits that represent only one change
and do not contain small meaningless changes like lines added to the code
inadvertently, or small bug corrections. 

I re-read my code before commiting it. If I spot a mistake to a commit on a dev
branch after it has been pushed, I will commit a patch as a *fixup*. Before 
merging the dev branch, I squash its fixups. An exemple of this can be found in 
the branches ```release/2.0_beforesquash``` and ```release/2.0```.

Also, my computer's repo has two remotes : *origin*, this GitHub repo, and *private-origin*,
a repo stored on my [BitBucket](http://bitbucket.org/) account that contains all the branches on my computer's repo.
It allows me to save my work and to write code on other computers than mine.

Fab files and Docker
--------------------

In the second version of this project, the environment of the project is
included in the repo. It makes the project extremely easy to deploy. In
addition, the evolution of the code and the environment can be stored together,
making the project easier to understand.

```docker-compose``` is used to run the system of container, which is describe
in ```docker-compose[.*].yml``` files. 

A fabfile is used to call ```docker-compose``` with the right arguments, since 
it's a rather tedious task due to the project's complexity.
I am really happy with how simple the fabfile is. There are two parts to it : 
- Functions that sets an environment variables (production or localhost) that
  must be called before)
- Functions that actually calls ```docker-compose```

The project can be run in any of its environment on any machine that has
[Docker](https://www.docker.com/)
and [Fabric](http://www.fabfile.org/) installed, with one simple command.

[Django](https://www.youtube.com/watch?v=IAooXLAPoBQ)
-----------------------------------------------------
Three applications compose this project :

* ```cv``` organize and show my previous work experience
* ```video``` shows the video
* ```themaintemplate``` request rendered HTML from the two previous
  applications and insert it in the main template

All of these application have very few dependance with one another, and they
could be used in another django project. ```themaintemplate``` is more or less 
the only one that needs the others to work.  This makes the project modulable 
and easily extandable.

I also use external libraries whenever its possible to reduce the amount of code
of which I am responsible. The insertion of Google Analytics of for exemple is
done by the [django-analytical](https://github.com/jcassee/django-analytical) 
library, and the compiling of the SASS files is done thanks to
[django-sass-processor](https://github.com/jrief/django-sass-processor).
(Honourable mention to django-analytical library, which could not be more
complete and make the library very simple to use).

I also use different settings for the different environments the project is
used in. Simple exemple : the setting DEBUG is disabled in production.

In a future commit, the server will be more complex : It will be internationalized to work in French and English,
will order its content in a more logical way and will generate a two minute tour of the CV based on a few \#skills the user gave him.
I have also planned to harvest some of the CV's data directly from my [Doyoubuzz](http://www.doyoubuzz.com/) account via their [API](http://doc.doyoubuzz.com/).

Dart
----
Dart is an object oriented equivalent to Javascript. When I first started this
project, I had few experience with Javascript, and Dart seemed more familiar to
the young developer that had spent the past year coding with java that I was.  
Now, a year and a half later, and with a lot more experience with Javascript, I 
can affirm that Dart is quite unnecessary in a project this small. Yes, it
produces huge files that are long to download, its compilation is 
unnecessary overhead and its syntax is heavier that Javascript's.

The only reason this project still contain Dart code is because I had very few
time to update this CV. With that said, I must say that there is a certain joy
to code with this language, using the object paradigm and typed variables. 

Another thing to note about Dart : its integration with Javascript is 
incredibly well done. I am heavily interacting with the [Youtube IFrame
API](https://developers.google.com/youtube/iframe_api_reference) in the 
```video``` application and it works like a charm. Again, the only pitfall is a
syntax heavier than if I had written the code directly in javascript.

All the client side code of this project is in Dart. Each time, there are two
files in the projects :  a file that contains a class that takes a DOM element 
on initialization and make them interactive, and a "bootstrap" file which create 
objects from these classes initialized with actual DOM elements.

A class that is used by both application is in the ```common/``` folder.

The usage of SCSS
----------------
SCSS is used lightly to avoid a few repetitions in the CSS code. An SCSS file
that contains variables and mixins used throughout the whole website is in the
```common/``` folder.

I prefer SCSS to LESS because it allows to make more complex code and its
syntax is compatible with CSS. I prefer PostCSS to SCSS because it allows to
use all the power of Javascript to process CSS files, unfortunatly, its
integration with Django is poor which I why I still use SCSS in this project.

The scripts linked to the page are only changing the content and the classes of the page's elements.
The CSS is responsible of the design and the animations. I make use of a few of CSS3 novelties, including transitions,
and the font is provided by [Google](http://www.google.com/fonts).

The website is responsive and works on mobile. It has three breakpoint : 
- Desktop
- Tablet
- Mobile

URL
---
Each content of the application has its URL. 
When navigating on the website, the URL is changed to match the content it is showing (except when showing the video because I deemed it useless).
Therefore, if you hit refresh or bookmark the link and open it later, it opens on the same content.
