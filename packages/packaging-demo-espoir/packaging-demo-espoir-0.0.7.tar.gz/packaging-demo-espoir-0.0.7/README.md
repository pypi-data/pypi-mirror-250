# PACKAGINGDATASCIENCE
Why packaging ?

1. Distributing Your Code 
2.  Non-painful import statements 
3.  Reproducibility and dependencies management specifically 


# Packaging terms:
- Module 
- Package
- sub-package
- distribution package 


# Modern way to build package :

* the old format distribution is sdist : source distribution package : python setup.py sdist 

   1. May make assumptions about customer machine:
      e.g. requires "gcc" to run "gcc numpy/*.c"
   2. Is slow: setup.py must be executed, compilation may be required.
   3. Is insecure: setup.py may contain  arbitrary code.
* the  good and new  format distribution is wheel 
   1. First install wheel package 
   2. the command help us to build wheel package : python setup.py bdist_wheel 
   3.  realpython.com/python-wheels/ explain clearly how to read wheel format 
   4.  we need to add build dependencies  for reproducibility and for it we need pyproject.toml file and install build tool : pip install build 
   5. escaping config hell; use setup.cfg : https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
   6. Removing setup.cfg  thanks to pep 621 : peps.python.org/pep-0621/
   7. reconfigure project.toml ->  https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html (In setuptool doc Note New in 61.0.0)
   8. After you will see the information about your package in PKG-INFO inside of packaging-demo-egg-info
   9. Removing setup.py : PEP 517 ; build backends : peps.python.org/pep-0517/
   10. Exemple use case for including data with various formats (in this example is json) into your package 
   11. unzip your whl like this : unzip *.whl after you move to dist repo : cd dist and move to your repo and tape  pip install . 
   12. documentation to specific problems to add data files into your package : https://setuptools.pypa.io/en/latest/userguide/datafiles.html and https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html#using-manifest-in
   13. python -m build --sdist --wheel ./; cd dist; unzip *.whl; cd ..
   14. for example to add data files recursively in your folder recursive-include packaging_demo/ *.json 
   15. equivalent of recursive include you can include in your pyproject.tom[tool.setuptools.package-data]
    my_pkg = ["*.json"] or you can use Hatch build system instead of setuptools : hatch.pypa.io/latest/config/build/#build-system poetry is another tool to build backend but is not pep 601 definition is not compliant 
 

 # Reproducibility 

 1. Dependency graph : add someting dependancies in pyproject.toml  and in terminal tape this command pip install -e.
2. visualize all dépendencies tree  of python libraries  use cli tool call  pipdeptree : pipdeptree --help , pipdeptree -p packaging-demo --grph-output png > dependency-graph.png , pip install graphviz  , and brew install graphviz or sudo apt-get install graphviz help us to the issues dependencies hell : constraint-trees (datascientist didn't document version of the dependencies we use ) the more library  they more constraints you have you had they more dependencies you have lot of constraints 
3. Document all of the exact version of library and the exact  python version and in addition of that you documented  opération system : m series mcbook , linus ..etc  the solution to this is  if you run pip freeze  : this is most vanilla way in python to freeze or lock your dependencies list : set of the exact version that satisfied constraint pip freeze > requirements.txt useful for developpment reproducibilty  poetry , pip-tools same willl help you .
4. you can add [project.optional-dependencies]
dev = ["ruff" , "mypy" , "black"] and after that run in terminal pip install '.[dev]' the same for rich add colors = ["rich] pip install '.[rich]' or pip install '.[colors,dev]' or  all = ["packaging_demo[dev , colors]"] and pip install '.[all]' package index search : snyk.io/advisor/python/package-index ( give you criteria to check package health in terms of security maintenance , community )


# IntrotoContinuous Delivery : Publishing to PyPI

* Product management :

 - Objectives , Discovery and Delivery 
    *1. Product Discovery 
    Discovery is very much about the intense collaboration of product management, user experience design and ingeieering 
    In  discovery we are tackling the various risks before we write even one line of production software.
    The purpose of product discovery is to quickly separate the good ideas from bad. The output of product discovery is a validated product backlog.
    Specifically, this means getting answers to four critical questions:

      a. Will the user buy this (or choose to use it )?
      b. Can the user figure out how to use this ?
      c. Can our engineers build this 
      d. Can our stakeholders support this ? 
      Prototypes : Product discovery involves running a series of very quick experiments , and do these experiements quickly and inexpensively, we use prototypes rather than products 
    *2.  Product  delivery 
    The purpose of all these prototypes and experiments in discovery is to quickly come up with something that provides some evidence it is worth building and that we can then deliver to our customers.
    This means the necessary scale , performance reliability fault tolerance security privacy internationalization and localization have been performed and the product works as advetised. The purpose of product delivery is to build and deliver these production-quality technology products something you can sell and run a business on 

Implementing a pipeline that publishes our package to Pypi : a single example of continuous delivery 

Continuous Delivery is a companion to Continuous Integration is the practice  which make small frequents commits to our code base . 


I constantly updating the codebase : Continuous integration 
I constantly make the integration code available to the users or continuously delivery thoses changes to the users 

 ** Devops : Developer Operations  or software developer operations : devops persons try to make software developper work as efficiently as possible (small frequents commits , ci/cd)
  - Waterfall vs Agile (Design product)

    Waterfall project management : strategy will use to build and delivers a product for end users (like construction happens to  a house , expensive product difficult to change after we construct  to construct house : waterfall method watterfall is linear )
- Agile : move fast ( Deliver quickly as posssible smallest things you can three days to create prototype  )

# Publishing your package to pypi : python package index  repositoritory 
Pypi  is immutable : you can replace an existing package  you can never upload the semantic version 
a second instance for pypi is testpYPI / test.pypi.org : test deployment package . https://pypi.org/
Twine is a cli we use to publish our paclkaqge to pypi : https://twine.readthedocs.io/en/latest/  twine --help twine upload --repository testpypi ./dist/*
Securely use twine cli tools to publish your package 


How to document various command need to runs when we develop code base :
the point is make your development workflow easy when other to contributers 
we take about config file common one on industry standards 
Install makefile tools extensions in vscode and brew install make to install cmake 
the first file we help us to make it is make file use tab instead space and make install : making artifacts : all generated by the code trying to be smart not rebuild all thing that's build the command is make and target which references bash script make file is portable 


Alternatives to make as task runners  : just and pyinvoke , Bash 

* just  https://github.com/casey/just
* pyinvoke  https://www.pyinvoke.org/
* Bash use Taskfile for AdrianCooney : https://github.com/adriancooney/Taskfile use chmod +x run.sh to render exceutable file track set -e or set -ex help you to debug when to want to install anything you can define  use makefile as  interface over your runsh script 
* Make you key or credential in security way for exemple if you use .github.com/ethOizzle/shhgit you can views all keys access free in repo public : it's not recommanded because commit is immutable  don't send sensitive : best managing secrets in productions : environnement variables 



# Github actions continuous delivery 

One kind of event is pull requests which have activity types : pull_request Listeners 
Triggers we have : 
React to pull request event : premerge 

postmerge  and push event

Github action context and secret management  : value to access  anytime in workflow 

In the settings in github section secrets and variables 
Repository secrets is what we interest for 

Access context in workflow  : use github expressions : dollard sign and double bracket
documentation of contexts in github actions : # https://docs.github.com/en/actions/learn-github-actions/contexts#example-printing-context-information-to-the-log
Different betweens variables : access a plain test value  printed   and secrets  are not unprinted  : 


if statements checks in publish yaml file : docs.github.com/en/actions/learn-github-actions/contexts#
after deployment sucessfull in prod we can tag this 


# speed up your workfows or pipeline ci/cd use  dependencies caching  : githubactions cahing 


[github.com/actions/cache](https://github.com/actions/cache/blob/main/examples.md#simple-example)


- uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt' , '**/project.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-

You can set the cache all the emplacement you had pip install 

pass artifacts (upload and downloads) between jobs : github.com/actions/download-artifact


# Software Testing and sample 

pytest tests/  

blackbox tests money in vendors machines  
glassbox tests 

bridle tests : everything your chznge code your change your tests 

Parameters test and testcaseuniverse : everytests you want to test (all combinaisons)

every tests should test one behaviour

Blackbox vs glassbox

Your users  really don't care about your implementation  (too slow , too buggy or insecure)
but your users care about is that your code had the behaviour that they expected (test automatic check the behaviour or core behaviuor of your codebase are still inatact  )

 for example if the product is library  is the Minimum all you functions , class you're exposing (public api) are awork as expected 
 More granular unit tests for private mlodule in you're code  as important test your functionnalities 


 
quick report : each  which lines are executes 
testcoverage is the percetange of lines of your program this actually gonna be execute 
how you're generate this report : coverage.py (pytest-cov)  pip install pytest-cov  pytest --help  
how much the code is covered by the tests : the core idea 

best practices

Run slow test in ci/cd in night and rapid (if bug fixes thoses  in journey)
Run rapid or fast tests in journey on evry commit 
python -m http.server -d  ./htmlcov   : to see your report in a website (locally) after run ./run.sh test 