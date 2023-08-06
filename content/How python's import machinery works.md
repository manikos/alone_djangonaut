Title: How python's import machinery works
Date: 2018-01-22
Category: python
Tags: import
Summary: Have you ever wondered what happens under the hood when you type `import my_package.my_module`? This article enlightens some of the (pretty) complicated aspects of the python import machinery.
description: A short walkthrough about the internal mechanisms of python's import machinery.
author: Nick Mavrakis
Status: published


# Glossary
Let's begin with the [basics](https://docs.python.org/3/glossary.html). 
From now on when we say the word *python* we mean python 3.6. Python 3 is the future and (who knows) python 4 will be the future of python 3 etc. 
Stop using python 2!

I'll try to be concise and simple, although the documentation about [modules](https://docs.python.org/3/tutorial/modules.html#modules) and 
[packages](https://docs.python.org/3/tutorial/modules.html#packages) is pretty straight forward. Go ahead and take a look to either learn
what these concepts are or just refresh your memory.


### Python module
When we say *python module* or just [`module`](https://docs.python.org/3/glossary.html#term-module) we mean a simple python file, i.e `models.py` or `utils.py`. 

> A module is a file containing Python definitions and statements. The file name is the module name with the suffix .py appended.

When you put a bunch of modules under a directory then this directory is called a *python package*.


### Python package
When we say *python package* or simply just [`package`](https://docs.python.org/3/glossary.html#term-package) we mean a directory that contains one or more *modules*.

> Packages are a way of structuring Python’s module namespace by using “dotted module names”.

Of course, a package may contain a bunch of other directories (packages) which themselves may contain a bunch of other modules mixed with other packages etc. You get the point.
That's how an application is structured. This, of course, does not apply to Python only but to every programming language out there.

Now, a package may or may not contain a `__init.py__` file which distinguishes it between a [`regular package`](https://docs.python.org/3/glossary.html#term-regular-package) and a 
[`namespace package`](https://docs.python.org/3/glossary.html#term-namespace-package). But I'll not go into details with namespace packages because first of all I have never used
a namespaced package and second, this article assumes a regular package (the one which has a `__init__.py` in it).



# Project setup

The following (super simple) project setup is assumed throughout this article:

```bash
tmp/
  my_package/
    __init__.py
    my_module.py
```
You can follow along with this article by putting the above structure inside a directory, i.e your `~/tmp/` directory.

This is the content of `my_module.py`:

```python
class MyClass:
	def __init__(self):
		print('init called')

	def caps(self, word):
		print(word.upper())
```
Nothing fancy here. Super simple because we want to focus on the import system. Not classes, methods etc.


# The easy way

From now on we will assume that the python interpreter is always enabled under the directory in which the above structure exists. No virtual environments.
I promised to keep it simple in order to get a grip on this import machinery monster.

In my system, I have it under `~/tmp`.

```bash
~> cd tmp
~/tmp> python3.6
Python 3.6.3 (default, Dec  3 2017, 22:10:01) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

*Side tip*: You can change the interactive python prompt from the default one (`>>> `) to i.e `> ` with: `import sys; sys.ps1 = '> '`
```python
~/tmp> python3.6
Python 3.6.3 (default, Dec  3 2017, 22:10:01) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys; sys.ps1 = '> '
> 
```

Now, if we type:

```python
>>> from my_package import my_module
>>>
>>> obj = my_module.MyClass()
init called
>>> obj.caps('hello')
HELLO
>>>
```
Import done! `MyClass` instance created! `caps()` method called! But you already know that. This is the first thing taught when you start learning python.

Go get a coffee/chocolate/tea/beer because here comes the good part. The internals have not yet begun...


# The dynamic way

There is another way to import a module (or package). Using the [import_module](https://docs.python.org/3/library/importlib.html#importlib.import_module) method. 
Well, this is quite easy to understand and you're **encouraged** to use it if you want to import things dynamically (instead of the old classic way of 
calling [`__import__()`](https://docs.python.org/3/library/functions.html#__import__)).

```python
>>> from importlib import import_module
>>>
>>> my_module = import_module('my_package.my_module')
>>> obj = my_module.MyClass()
init called
>>> obj.caps('hello')
HELLO
```
As seen from above, we have named the module, returned by the `import_module` method, as `my_module`, the same as the module's name in order to be consistent.
We could have also name it i.e `mod` (or whatever) but then we must do `obj = mod.MyClass()`. 

Now take a look at this:

```python
>>> from importlib import import_module
>>>
>>> my_module = import_module('my_package')
>>> obj = my_module.my_module.MyClass()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  AttributeError: module 'my_package' has no attribute 'my_module'
```
What? But I have imported `my_package`. Why the `my_module` module cannot be found? Because, simply, it has not been loaded (imported). 
We should import it explicit just like we did in the previous example. When importing a package, it is not assumed that all other
sub-packages/sub-modules are imported too. This applies to all Python import mechanisms, not only to `import_module` method.


# The (almost) manual way

Hang on. We haven't reach our goal to the pure manual way of importing things. 
Here is [another way](https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path#answer-43602557) of importing a 
module (or package) without the direct usage of [import_module](https://docs.python.org/3/library/importlib.html#importlib.import_module) method.

```python
>>> from importlib.util import spec_from_loader, module_from_spec
>>> from importlib.machinery import SourceFileLoader
>>>
>>> spec = spec_from_loader("my_package.my_module", SourceFileLoader("my_package.my_module", "/home/nick/tmp/my_package/my_module.py"))
>>> spec
ModuleSpec(name='my_package.my_module', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f877568fcc0>, origin='/home/nick/tmp/my_package/my_module.py')
>>> dir(spec)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_cached', '_set_fileattr', 'cached', 'has_location', 
'loader', 'loader_state', 'name', 'origin', 'parent', 'submodule_search_locations']
>>>
>>> mod = module_from_spec(spec)
>>> mod
<module 'my_package.my_module' from '/home/nick/tmp/my_package/my_module.py'>
>>> dir(mod)
['__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
>>>
>>> spec.loader.exec_module(mod)
>>> dir(mod)
['MyClass', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
>>>
>>> obj = mod.MyClass()
init called

```
> [READER] Hey, wait mister. What are these? Looks more like [Klingon language](https://en.wikipedia.org/wiki/Klingon_language) than Python!

> [ME] No, no. It does not. It is pretty self-explanatory once we start digging the python's import internals.

Note that there is also another way (the pure manual way) to import a Python module but I keep it for last in order to stay with me till the end :)


<hr>

# Import machinery's concept

Python has a very nice abstraction-philosophy of thinking about how to import things. On the other hand someone else could say that this system is quite complicated. 
Nevertheless, the system comprises of finders, loaders, specifications, modules, caching and a conductor that orchestrates all these, 
named [`python import machinery`](https://docs.python.org/3/reference/import.html). All these come to play whenever you type `import my_package`.

At a glance, the job of the finders is to find (locate) the requested module. If the module can be found, a specification (for that module) is returned. This spec
is used by the loaders to *create the module*, *initialize it* and *execute it*. If the module cannot be found, the classic [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError) exception is raised.


## The procedure

### 1. `sys.modules`

Every time you import a module, the first thing searched is [`sys.modules`](https://docs.python.org/3/library/sys.html#sys.modules) dictionary. 
The keys are just plain strings which consist of module names (with or without the dotted path, which means that are either top-level modules or sub-modules) 
and the value is the actual [`module`](https://docs.python.org/3/library/types.html#types.ModuleType) itself. `sys.modules` dict acts like a cache. 
If it's there, go get it. Do not instantiate the import cycle again.

Let's have a look at the contents of `sys.modules`:

```python
>>> import sys
>>>
>>> print(sys.modules)
{'builtins': <module 'builtins' (built-in)>, 
 'sys': <module 'sys' (built-in)>, 
 '_frozen_importlib': <module '_frozen_importlib' (frozen)>, 
 '_imp': <module '_imp' (built-in)>, 
 '_warnings': <module '_warnings' (built-in)>, 
 '_thread': <module '_thread' (built-in)>, 
 '_weakref': <module '_weakref' (built-in)>, 
 '_frozen_importlib_external': <module '_frozen_importlib_external' (frozen)>, 
 '_io': <module 'io' (built-in)>, 'marshal': <module 'marshal' (built-in)>, 
 'posix': <module 'posix' (built-in)>, 
 'zipimport': <module 'zipimport' (built-in)>, 
 'encodings': <module 'encodings' from '/usr/local/lib/python3.6/encodings/__init__.py'>, 
 'codecs': <module 'codecs' from '/usr/local/lib/python3.6/codecs.py'>, 
 '_codecs': <module '_codecs' (built-in)>, 
 'encodings.aliases': <module 'encodings.aliases' from '/usr/local/lib/python3.6/encodings/aliases.py'>, 
 'encodings.utf_8': <module 'encodings.utf_8' from '/usr/local/lib/python3.6/encodings/utf_8.py'>, 
 '_signal': <module '_signal' (built-in)>, '__main__': <module '__main__' (built-in)>, 
 'encodings.latin_1': <module 'encodings.latin_1' from '/usr/local/lib/python3.6/encodings/latin_1.py'>, 
 'io': <module 'io' from '/usr/local/lib/python3.6/io.py'>, 
 'abc': <module 'abc' from '/usr/local/lib/python3.6/abc.py'>, 
 '_weakrefset': <module '_weakrefset' from '/usr/local/lib/python3.6/_weakrefset.py'>, 
 'site': <module 'site' from '/usr/local/lib/python3.6/site.py'>, 
 'os': <module 'os' from '/usr/local/lib/python3.6/os.py'>, 
 'errno': <module 'errno' (built-in)>, 
 'stat': <module 'stat' from '/usr/local/lib/python3.6/stat.py'>, 
 '_stat': <module '_stat' (built-in)>, 
 'posixpath': <module 'posixpath' from '/usr/local/lib/python3.6/posixpath.py'>, 
 'genericpath': <module 'genericpath' from '/usr/local/lib/python3.6/genericpath.py'>, 
 'os.path': <module 'posixpath' from '/usr/local/lib/python3.6/posixpath.py'>, 
 '_collections_abc': <module '_collections_abc' from '/usr/local/lib/python3.6/_collections_abc.py'>, 
 '_sitebuiltins': <module '_sitebuiltins' from '/usr/local/lib/python3.6/_sitebuiltins.py'>, 
 'sysconfig': <module 'sysconfig' from '/usr/local/lib/python3.6/sysconfig.py'>, 
 '_sysconfigdata_m_linux_x86_64-linux-gnu': <module '_sysconfigdata_m_linux_x86_64-linux-gnu' from '/usr/local/lib/python3.6/_sysconfigdata_m_linux_x86_64-linux-gnu.py'>, 
 'readline': <module 'readline' from '/usr/local/lib/python3.6/lib-dynload/readline.cpython-36m-x86_64-linux-gnu.so'>, 
 'atexit': <module 'atexit' (built-in)>, 
 'rlcompleter': <module 'rlcompleter' from '/usr/local/lib/python3.6/rlcompleter.py'>
}
>>>
>>> 'my_package.my_module' in sys.modules
False
>>> len(sys.modules.keys())
60
```
Can you see `my_package.my_module` in there? No? Good! That's because it has not been imported (yet) and not added to this dictionary. 
If you write `from my_package import my_module` then:

```python
# Continue from previous example

>>> from my_package import my_module
>>> print(sys.modules)
{'builtins': <module 'builtins' (built-in)>, 
 'sys': <module 'sys' (built-in)>, 
 '_frozen_importlib': <module '_frozen_importlib' (frozen)>, 
 # ... same as before
 'my_package': <module 'my_package' from '/home/nick/tmp/my_package/__init__.py'>,
 'my_package.my_module': <module 'my_package.my_module' from '/home/nick/tmp/my_package/my_module.py'>
}
>>> 'my_package' in sys.modules
True
>>> 'my_package.my_module' in sys.modules
True
>>> len(sys.modules.keys())
62
```
As seen from above, when we added the `import` statement, two entries added to `sys.modules`. The top-level module (which acts like a package) and the dotted path
to the module (`my_module.py`) itself. Now, every other time we reference to `my_module` it will be loaded from `sys.modules`.  
The `import` statement took care of all the internals and added it to `sys.modules`, plus made it available to work with it. But how did all these happen? 

Enter import machinery!


### 2. Finders

If the module requested is not found in the `sys.modules` dict, then the list [`sys.meta_path`](https://docs.python.org/3/reference/import.html#the-meta-path) arises. 
This list contains [`meta path finder objects`](https://github.com/python/cpython/blob/3.6/Lib/importlib/abc.py#L47). Lets look at it:

```python
>>> import sys
>>> print(sys.meta_path)
[
  <class '_frozen_importlib.BuiltinImporter'>, 
  <class '_frozen_importlib.FrozenImporter'>,
  <class '_frozen_importlib_external.PathFinder'>
]
```
The job of each one is to locate the requested module by returning the specification (we'll get to that) of the module or simply `None`. The competent for that is the
[`find_spec`](https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder.find_spec) method. This method is called first (for each `meta finder`) whenever 
you `import` something.

*from the [docs](https://docs.python.org/3/reference/import.html#the-meta-path)*
> These finders are queried in order to see if they know how to handle the named module.
> Meta path finders must implement a method called `find_spec()` which takes three arguments: a name, an import path, and (optionally) a target module.

The [`BuiltinImporter`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap.py#L689) is used purely for builtin modules. You may ask which are
these modules. Lets take a look.

```python
>>> import sys
>>> sys.builtin_module_names
('_ast', '_codecs', '_collections', '_functools', '_imp', '_io', '_locale', '_operator', 
 '_signal', '_sre', '_stat', '_string', '_symtable', '_thread', '_tracemalloc', '_warnings', 
 '_weakref', 'atexit', 'builtins', 'errno', 'faulthandler', 'gc', 'itertools', 'marshal', 
 'posix', 'pwd', 'sys', 'time', 'xxsubtype', 'zipimport')
```
So, every time you type `import sys`, or `import itertools` etc, the finder used to locate that module (remember, **not to load it**) is the `BuiltinImporter`.

Next, comes the [`FrozenImporter`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap.py#L762) which is used to locate [frozen modules](https://wiki.python.org/moin/Freeze). 
We will not concern with that type of modules, though.

Last but not least is the [`PathFinder`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L1055) which is responsible for locating any 
module/package not in the range of the previous two. More specifically, it handles modules that are located either on `sys.path`, `sys.path_hooks`, `sys.path_importer_cache` or
the `__path__` attribute on the package.

> If `sys.meta_path` processing reaches the end of its list without returning a spec, then a [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError) is raised.

Imagine the above three (default) guys like persons with a flashlight, each looking at a specific locations to find a module. If all of them fail then either the package
exists but the finders are not looking in the correct location or the package does not exist at all. I think until here, all these are quite easy to understand.

And one more thing: you can [extend](https://docs.python.org/3/reference/import.html#import-hooks) this list writing your own `meta finder` but more on this later.

Lets dive deeper...


#### 2.1 Spec object

[Specification objects](https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec) or just `spec objects` are the meta data of 
[modules](https://docs.python.org/3/library/types.html#types.ModuleType). Every `module` has a `spec` because in order to import a module the
spec is required. Thus, every `module` exposes a `__spec__` attribute. Lets inspect one:

```python
>>> import my_package
>>>
>>> dir(my_package)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__']
>>>
>>> spec = my_package.__spec__
ModuleSpec(name='my_package', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f9673ceee48>, origin='/home/nick/tmp/my_package/__init__.py', submodule_search_locations=['/home/nick/tmp/my_package'])
>>>
>>> dir(spec)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
 '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
 '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
 '_cached', '_initializing', '_set_fileattr', 'cached', 'has_location', 'loader', 'loader_state', 'name', 'origin', 
 'parent', 'submodule_search_locations'
]
>>> spec.origin
'/home/nick/tmp/my_package/__init__.py'
>>> spec.parent
'my_package'
>>> spec.submodule_search_locations
['/home/nick/tmp/my_package']
```
Examining the above code, we can see that the `spec` (object of the `ModuleSpec` class) of `my_package` package has its own methods and attributes. 
One of the attributes it has is the `loader`. The `loader` indicates to the import machinery which loader to use while creating and executing the module.
Remember, until now the module has not yet been created. Only the `spec`. From a spec derives a module.
There are other attributes as well, like `origin` (name of the place from which the module is loaded, “builtin” for built-in modules and the filename for modules loaded from source.), 
`parent` (fully-qualified name of the package) and `submodule_search_locations` (list of strings for where to find submodules), all of which are useful to the importer.

As you have guessed, if you import a module (and not a package) you will see that the `submodule_search_locations` will be `None` since the module is always the
*leaf in the tree*. In technical terms, the module has no [`__path__`](https://docs.python.org/3/reference/import.html#__path__) attribute as opposed to a package.

Conclusion: `spec` objects hold valuable information about the creation of the `modules`. `spec` objects are needed to construct and import a `module`. 


### 3 Path Finder

Remember the list `sys.meta_path` where there three default `meta path finder objects` (aka `importers`)? The most common scenario is where you import packages
and modules from within your project and also other modules not handled by the first two importers. So, the most busy guy is the last one. Let me introduce you
the [`Path Based Finder`](https://docs.python.org/3/reference/import.html#the-path-based-finder).

The `Path Based Finder` (PBF for short) can be imported (if you want to play with him) with different names. All of them are aliases.

```python
>>> from _frozen_importlib_external import PathFinder as A
>>> from importlib._bootstrap_external import PathFinder as B
>>> from importlib.machinery import PathFinder as C
>>>
>>> A == B == C
True
>>> A is B is C
True
>>> id(A) == id(B) == id(C)
True
>>>
>>> dir(A)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
 '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
 '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
 '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_spec', '_legacy_get_spec', 
 '_path_hooks', '_path_importer_cache', 'find_module', 'find_spec', 'invalidate_caches'
]
```
All of them aliases. But, in my opinion I'll stay with the last import statement since I don't want to mess with the underscore prefix imports.

Although, PBF seems like a smart guy, he doesn't know how to import anything. He needs help. Help from other guys. Now this may sound strange. Why
the PBF does not handle the *findings* all by himself? Well, this is an implementation detail and maybe it is for good.

All that PBF does is that he traverses the individual path entries, associating each of them with a `path entry finder` that knows how to handle that particular kind of path.
Where are these *path entries* and these *path entry finders* you may ask. Well, the `sys` package has one more time the answer.

- path entry no1: [`sys.path`](https://docs.python.org/3/library/sys.html#sys.path)
- path entry no2: [`sys.path_hooks`](https://docs.python.org/3/library/sys.html#sys.path_hooks)
- path entry no3: [`sys.path_importer_cache`](https://docs.python.org/3/library/sys.html#sys.path_importer_cache)
- path entry no4: [`__path__`](https://docs.python.org/3/reference/import.html#__path__) attribute on package objects

<hr> 

1. You all know the first one. It's a list of string defined by the environment variable `PYTHONPATH` as well as from other mechanisms (virtualenvs etc). 

2. The second is another list consists of Path Entry Finders (PEF for short) callables. Different from the meta one we're talking about (PBF).

3. The third one is a dictionary, mapping locations (strings) to PEF objects.

4. The last one is the `spec.submodule_search_locations` (or `my_package.__path__`, if you like) which contains a list of strings indicating sub-modules/sub-packages locations.

```python
>>> import sys
>>>
>>> sys.path
['', '/usr/local/lib/python36.zip', '/usr/local/lib/python3.6', '/usr/local/lib/python3.6/lib-dynload', '/usr/local/lib/python3.6/site-packages']
>>>
>>> sys.path_hooks
[<class 'zipimport.zipimporter'>, <function FileFinder.path_hook.<locals>.path_hook_for_FileFinder at 0x7f9673dfa6a8>]
>>>
>>> sys.path_importer_cache
{'/usr/local/lib/python36.zip': None, 
 '/usr/local/lib/python3.6': FileFinder('/usr/local/lib/python3.6'), 
 '/usr/local/lib/python3.6/encodings': FileFinder('/usr/local/lib/python3.6/encodings'), 
 '/usr/local/lib/python3.6/lib-dynload': FileFinder('/usr/local/lib/python3.6/lib-dynload'), 
 '/usr/local/lib/python3.6/site-packages': FileFinder('/usr/local/lib/python3.6/site-packages'), 
 '/home/nick/tmp': FileFinder('/home/nick/tmp'), 
 '/usr/local/lib/python3.6/collections': FileFinder('/usr/local/lib/python3.6/collections'), 
 '/home/nick/tmp/my_package': FileFinder('/home/nick/tmp/my_package'), 
 '/usr/local/lib/python3.6/importlib': FileFinder('/usr/local/lib/python3.6/importlib')
}
```
Feel a little lost with all these? Lets make a very brief recap to see where are we:

1. An import statement is encountered
2. Is the preferred imported name in `sys.modules`?
3. If yes import it, done!
4. If not, call `find_spec()` on each `sys.meta_path` importer and wait for a `spec`  **&larr; this is where we are!**
5. If no `spec` returned, raise `ModuleNotFoundError`
6. If a `spec` returned, create the module (have not talk about it yet)
7. Once the module is created, initialize it with default attributes
8. Add it to `sys.modules` (aka add it to cache)
9. Execute the module

Lets continue!

In order to find what are the above `path entries` and how they are related to the PEF, we must take a look at the 
[`find_spec()`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L11500) implementation of the
last meta path finder in the `sys.meta_path` list, [`PathFinder`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L1055).

```python
def _path_hooks(cls, path):
    """Search sys.path_hooks for a finder for 'path'."""
	if sys.path_hooks is not None and not sys.path_hooks:
		_warnings.warn('sys.path_hooks is empty', ImportWarning)
	for hook in sys.path_hooks:
		try:
			return hook(path)
		except ImportError:
			continue
		else:
			return None


def _path_importer_cache(cls, path):
    """Get the finder for the path entry from sys.path_importer_cache.
	   If the path entry is not in the cache, find the appropriate finder
	   and cache it. If no finder is available, store None.
	"""
	if path == '':
		try:
			path = _os.getcwd()
		except FileNotFoundError:
			# Don't cache the failure as the cwd can easily change to
			# a valid directory later on.
			return None
	try:
		finder = sys.path_importer_cache[path]
	except KeyError:
		finder = cls._path_hooks(path)
		sys.path_importer_cache[path] = finder
	return finder


def _get_spec(cls, fullname, path, target=None):
	"""Find the loader or namespace_path for this module/package name."""
	# [...]
	for entry in path:
		finder = cls._path_importer_cache(entry)
		if finder is not None:
			if hasattr(finder, 'find_spec'):
			    spec = finder.find_spec(fullname, target)
			else:
				spec = cls._legacy_get_spec(fullname, finder)
			if spec is None:
				continue
			if spec.loader is not None:
				return spec
			# other stuff here [...]
	else:
		spec = _bootstrap.ModuleSpec(fullname, None)
		spec.submodule_search_locations = namespace_path
		return spec


def find_spec(cls, fullname, path=None, target=None):
    """Try to find a spec for 'fullname' on sys.path or 'path'.
       The search is based on sys.path_hooks and sys.path_importer_cache.
    """
    if path is None:
	    path = sys.path
    spec = cls._get_spec(fullname, path, target)
    if spec is None:
	    return None
	elif spec.loader is None:
		namespace_path = spec.submodule_search_locations
		if namespace_path:
			# We found at least one namespace path.  Return a
			#  spec which can create the namespace package.
			spec.origin = 'namespace'
			spec.submodule_search_locations = _NamespacePath(fullname, namespace_path, cls._get_spec)
			return spec
		else:
			return None
	else:
		return spec
```
Take a minute to navigate yourself to these pretty self-explained methods. It all starts from the
`find_spec('my_package.my_module', path=['/home/nick/tmp/my_package/my_module.py'])` call.

Done?

OK, lets look at these together. Note, you're looking at the *meat* of how python locates modules in a filesystem.

1. If a `path` is not passed to `find_spec` then the `sys.path` is used. 
2. The `_get_spec()` is called.
3. For each `path entry` in the list of paths (either `sys.path` or the passed `path` parameter) the `_path_importer_cache()` is called with this entry.
4. As said above, the `sys.path_importer_cache` is a dictionary and acts like a cache (as the name implies). The `_path_importer_cache()` method returns 
the value (the Path Entry Finder - [`FileFinder`](https://docs.python.org/3/library/importlib.html#importlib.machinery.FileFinder), if you recall) if a value is found for that path. 
5. If the cache fails, then a new Path Entry Finder *tries* to be created (we're inside the `_path_hooks()` method now) and returned. 
6. If that fails too, then `None` is returned and the `sys.path_importer_cache` gets updated with the key as the *failed* path and the value as `None`. So, next time the 
same path is tried to imported, the cache will get queried, `None` will return and a `ModuleNotFoundError` gets raised.
7. If the creation (initialization, to be more accurate) of the new PEF succeeds (`try` block of the `_path_hooks` method) then this PEF for this path is stored in the cache 
(we are inside the `_path_importer_cache` method now).
8. (back to `_get_spec` method) the `find_spec` method is called. If this fails, then `continue` to next path. If spec found and the spec has a `loader`, return it.
9. Finally, if the `path` list reaches the end without a result (we're still inside the `_get_spec` method), the `else` clause (of the `for` loop) is executed and a new `spec` is created 
without a loader. Just an empty `ModuleSpec` object. This object is returned.
10. Because this `ModuleSpec` object has no loader associated with and the `submodule_search_locations` attribute is an empty list, `None` will be returned by the `find_spec` method.

I want to make clear that a spec is a totally different thing than a finder. A finder is just responsible for *finding* paths, locations, files, URLs, etc. For example, the FileFinder
is responsible to locate paths that interact with the file system. Not URLs. Neither database queries. Just plain strings, i.e `/path/to/a/location` that represent a valid file system
path. A custom Finder could be made to *interpret* other locations, i.e a RedisFinder that can locate redis based urls.

On the other hand, a spec is created given a set of parameters (`location`, `loader`, `submodule_search_location`). The real creation of the spec, the place where the initialization of
the `types.ModuleSpec()` takes place, is just a plain function in the python's source code and its name is [`spec_from_file_location`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L524). 
There is also another place where the `ModuleSpec()` get called, inside the `_get_spec()` method as well. 

Am I too explicit of describing things and got lost (again)? Here is a short version of the above:

1. There are two default Path Entry Finders (`sys.path_hooks`, the `zipimporter` and the `FileFinder`, actually the first one is a class and the second is a [callable](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L1322)) 
which used by the Path Based Finder (`PathFinder`). However, this list can be extended. For example you may make an `HttpFinder` that is 
[able to locate modules through URLs](https://youtu.be/0oTh1CXRaQ0?t=2h50m32s), along with the associated `loader` of course.
2. Python, has already populated a cache with most common paths for you, inside the `sys.path_importer_cache` dict. Most of them are assigned to the `FileFinder` and some to `None`.
3. If the package you're trying to import is not inside the `path` list parameter passed to `find_spec` then, I'm sorry buddy but you'll get an error!
4. Next time you try to import the same package, unless no changes have been made to `sys.path` or `sys.path_importer_cache`, you'll get the same error because this path has been *black listed*
inside the `sys.path_importer_cache`.

Some hints:

- There are two `find_spec` methods. One implemented by the [`PathFinder`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L1150) (the meta one or the Path Based Finder, if you like this name) 
and the other by the [`FileFinder`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L1233) (one of the Path Entry Finders, the other one is the zipimporter).
- Python calls `PathFinder`'s `find_spec` which implicit calls `Filefinder`'s `find_spec`.
- Nevertheless, the `find_spec` will return either a spec or `None`. Period.

Now that we have an idea what a Finder is, lets play with that guy and try to load a spec, using different ways.

```python
>>> import sys
>>>
>>> sys.meta_path
[<class '_frozen_importlib.BuiltinImporter'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib_external.PathFinder'>]
>>> pf = sys.meta_path[-1]
>>> sys.path_importer_cache
{'/usr/local/lib/python36.zip': None, 
 '/usr/local/lib/python3.6': FileFinder('/usr/local/lib/python3.6'), 
 '/usr/local/lib/python3.6/encodings': FileFinder('/usr/local/lib/python3.6/encodings'), 
 '/usr/local/lib/python3.6/lib-dynload': FileFinder('/usr/local/lib/python3.6/lib-dynload'), 
 '/usr/local/lib/python3.6/site-packages': FileFinder('/usr/local/lib/python3.6/site-packages'), 
 '/home/nick/tmp': FileFinder('/home/nick/tmp'), 
 '/usr/local/lib/python3.6/collections': FileFinder('/usr/local/lib/python3.6/collections')
}
>>> del sys.path_importer_cache['/home/nick/tmp']
>>> # now when I try to find the spec for "my_package", the cache will not find it and the
>>> # import mechanism will start.
>>> pf.find_spec('my_package')
ModuleSpec(name='my_package', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7ff3f060fcf8>, origin='/home/nick/tmp/my_package/__init__.py', submodule_search_locations=['/home/nick/tmp/my_package'])
>>> # found it and the cache has been updated
>>> '/home/nick/tmp' in sys.path_importer_cache.keys()
True
>>> # Let's prevent it from locating our package!
>>> del sys.path_importer_cache['/home/nick/tmp']
>>> sys.path
['', '/usr/local/lib/python36.zip', '/usr/local/lib/python3.6', '/usr/local/lib/python3.6/lib-dynload', '/usr/local/lib/python3.6/site-packages']
>>> del sys.path[0]  # the first element, '' (empty string), searches, by default, to the current working directory
>>> # We have removed all potential references of our current working directory. Lets see now
>>> pf.find_spec('my_package')  # yeah! None returned!
>>> # Lets add it back
>>> sys.path.append('/home/nick/tmp')  # the same as ...append('') or sys.path.insert(0, '')
>>> pf.find_spec('my_package')
ModuleSpec(name='my_package', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7ff3f060fcf8>, origin='/home/nick/tmp/my_package/__init__.py', submodule_search_locations=['/home/nick/tmp/my_package'])

```

### 4. Loaders

The hard part is to find the spec. If the spec is found, things are quite easy. You can find the pseudo code of a loader [here](https://docs.python.org/3/reference/import.html#loading).

In a sense, the loader uses the spec to create the module. Most of the times this will return [`None`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L669) 
and the `module` will be created using the default semantics. What that, exactly means? It means that the [`_init_module_attrs`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap.py#L504) 
takes place and [the module object gets *filled* with the appropriate attributes](https://docs.python.org/3/reference/import.html#import-related-module-attributes).
Continuing, after the module is *created*, it has to be added to the `sys.modules` (recall this dict, it's the first cache that gets queried when an `import` statement is encountered) and finally 
get [executed](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L672). Done! Your module, after a long journey, can now be used by the programmer, you!

Have you noticed the *secret sauce* when you import a package or module? It's [this line exactly](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L678) 
(inside the `exec_module` method of the `_LoaderBasics` class, where the [`SourceFileLoader`](https://github.com/python/cpython/blob/3.6/Lib/importlib/_bootstrap_external.py#L836) inherits from):

```bash
_bootstrap._call_with_frames_removed(exec, code, module.__dict__)
```

The module (the python file) gets executed using the (sometimes evil one) [`exec`](https://docs.python.org/3/library/functions.html#exec) builtin function. 
Since, the code is executed, you then have all your python definitions at your feet to work with. 
Here's an [explanation from StackOverflow](https://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile-in-python#answer-29456463) of the differences 
between `eval`, `exec` and `compile`. Very descriptive!

Lets look at an example, a complete example this time:


# The (pure) manual way


```python
>>> import sys
>>> import types
>>> 
>>> # get out lovely finder
>>> pf = sys.meta_path[-1]
>>> pf
<class '_frozen_importlib_external.PathFinder'>
>>> 
>>> # get the spec for "my_package.my_module", path is given as the place to search
>>> spec = pf.find_spec('my_package.my_module', path=['/home/nick/tmp/my_package'])
>>> spec
ModuleSpec(name='my_package.my_module', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f9117dfee48>, origin='/home/nick/tmp/my_package/my_module.py')
>>>
>>> sys.path_importer_cache
{'/usr/local/lib/python36.zip': None, 
 '/usr/local/lib/python3.6': FileFinder('/usr/local/lib/python3.6'), 
 # ... other locations here
 '/home/nick/tmp': FileFinder('/home/nick/tmp'), 
 '/home/nick/tmp/my_package': FileFinder('/home/nick/tmp/my_package')
}
>>> # ~/tmp/my_package was added to the cache along with its associated FileFinder
>>>
>>> mod = spec.loader.create_module(spec)
>>> mod is None
True
>>> # Hmm... loader did not created it, lets do it manually
>>> mod = types.ModuleType(spec.name)  # spec.name == 'my_package.my_module'
>>> mod
<module 'my_package.my_module'>

>>> # module has been created. At this time we should fill it with proper attributes
>>> # but it works without filling it too. I'll fill it.
>>> mod.__name__  # already equals spec.name
'my_package.my_module'
>>> mod.__loader__ = spec.loader
>>> mod.__file__ = spec.origin
>>> mod.__package__ = spec.parent
>>> sys.modules[spec.name] = mod  # add it to cache
>>> mod
<module 'my_package.my_module' from '/home/nick/tmp/my_package/my_module.py'>
>>> # the printed version of mod has changed
>>> dir(mod)
['__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
>>>
>>> # final step. execute the module
>>> spec.loader.exec_module(mod)  # returns None
>>> dir(mod)
['MyClass', '__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
>>>
>>> # Wow! Look at that! MyClass. Lets use it...
>>> obj = mod.MyClass()
init called
>>> obj.caps('it worked!')
IT WORKED!
```

The above all-in manual way of importing our `my_module.py` module, was a bare implementation of the [module loading pseudo code](https://docs.python.org/3/reference/import.html#loading).

By now, you should be able to debug better any `ModuleNotFoundError`s or `ImportError`s. Of course, in most cases, you will not have to swim so deep, as we did here, but at least, 
you know far more than before. In addition to all the above, the `import` statement does a lot more while loading the module but that is an implementation detail and better be 
left to core developers. 

For the last, here some nice sources to look, if you want to learn more or just enjoying reading-watching:

- David Beazley's video on [Modules and Packages: Live and Let Die! - PyCon 2015](https://www.youtube.com/watch?v=0oTh1CXRaQ0)
- [Be careful with exec and eval in Python](http://lucumr.pocoo.org/2011/2/1/exec-in-python/) article by [Armin Ronacher](http://lucumr.pocoo.org/about/) (the creator of [Flask](http://flask.pocoo.org/))
- Another article by [Armin Ronacher](http://lucumr.pocoo.org/about/) [Dealing with the Python Import Blackbox](http://lucumr.pocoo.org/2011/9/21/python-import-blackbox/)
