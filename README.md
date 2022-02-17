# BBox Loader

A fast bounding box loader

## Installation

First, we need to install this package's dependency: Intel Threading Building Blocks (TBB).
This allows for parallel when performing query operations in the list, such as finding an item.

```bash
sudo apt install libtbb-dev
```

Now, we can clone and build this package
```bash
git clone git@github.com:omnious/res-bbox-loader.git
cd res-bbox-loader
python setup.py install
```

## Usage

Check out the `loader_example.py` for how to use this package.
