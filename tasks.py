# Task definitions for invoke
# You must first install invoke, https://www.pyinvoke.org/

import fiona # Avoids a bizzare error: AttributeError: module 'fiona' has no attribute '_loading'
import sys
from pathlib import Path
import metapack as mp
from invoke import task
from metapack_build.tasks.package import ns, build as mp_build
from metapack.appurl import SearchUrl

SearchUrl.initialize()  # This makes the 'index:" urls work
sys.path.append(str(Path(__file__).parent.resolve()))

import pylib
import importlib
importlib.reload(pylib) # Because when using a collection with invoke, may already have been loaded


@task
def cache_scores(c):
    """Cache scores from the score points"""
    
    pkg_dir = str(Path(__file__).parent.resolve())
    pkg = mp.open_package(pkg_dir)
    
    df_url = pkg.reference('scorepoints').url
    
    c.run(f"ds_batchscore --exceptions -v -L layers.txt {df_url}")
    

ns.add_task(cache_scores)

@task
def compile_scores(c):
    """Compile the cached scores into a data file. """
    
    pkg_dir = str(Path(__file__).parent.resolve())
    pkg = mp.open_package(pkg_dir)
    
    df_url = pkg.reference('scorepoints').url
    
    c.run(f"ds_batchscore --exceptions -v -o data/scores.csv {df_url}")
  
ns.add_task(compile_scores)


@task( optional=['force'])
def build(c, force=None):
    """Build a scores file in the data directory, then build the package. """

    cache_scores(c)
    compile_scores(c)

    mp_build(c, force)

    
ns.add_task(build)
