# CSC-UW changes to vanilla SpikeInterface
We should aim to one day use the official SpikeInterface!

Detailed comparison: https://github.com/CSC-UW/spikeinterface/compare/master...wisc/dev

Summary, updated 5/11/2022:
- Explicitly sets MKL BLAS and LAPACK shared object libraries, which is necessary on Linux per [#199](https://github.com/MouseLand/Kilosort/issues/199#issuecomment-754971599).
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/1aae5e902c12e0560b54c1dc74fc43c238a3248e)
  - Perhaps we should submit a PR to spikeinterface / KiloSort install intstructions with info about how to obtain proper BLAS and LAPACK versions, then set the   relevant environment variables in `.bashrc`? Or is there a spikeinterface config file that users can add their BLAS and LAPACK locations to? Or can they be set as a keyword argument somewhere? Like in the Kilosort sorter class? 
- Save diagnositc drift plots by default
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/66ddafa08b5f3f13b301c2ce2d5772d843af7cec)

  - Vanilla Kilosort does not save any of the plots generated during drift correction when run from spikeinterface. 
  In our CSC-UW fork (branch wisc/2.5/dev) [it does](https://github.com/CSC-UW/Kilosort/commit/d74018a6566b8aa22fc68fa75f0e97a4df2dcac1) when the `ops` structure contains a `plotDir` entry set to the path to output debugging plots. No plot is saved if `ops.plotDir` is not specified or is set to `false`
  - This commit sets `ops.PlotDir` to `<kilosort_output_dir>/plots_ks`.
  - (TODO) We can get rid of this commit by always saving debugging plots in CSC-UW/Kilosort `datashift2.m` file.
- Expose lambda parameter to SpikeInterface
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/10dc6a0ded76b750ed5e546625a4bdcb07a0257d)
  - This seems like it would be widely useful as a PR. 
- Expose do_correction option to SpikeInterface
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/89b8c44112a81100029b7a54123ba44ee8f2b3fd)
  - This seems like it would be widely useful as a PR. 
- On UNIX, explicitly set the MATLAB shell to bash. 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/832d00fd6fa4ffb6da89d10dad91d3e8bb7144fa)
  - We need to do this to prevent MATLAB from using Fish. Otherwise [this](https://github.com/MouseLand/Kilosort/blob/74c64485d8dd0bc5dd976d7bf51a46873b08351f/utils/rezToPhy.m#L186) line fails with a `command not found` error. I (TB) don't understand why that is the case (and it doesn't happen when default shell is Zsh or Bash). I think this would be a useful PR but there might be a better way of adressing this, which applies to all sorters (it might even be an issue with Fish itself).

### Changes merged in vanilla Spikeinterface 
- Allows concatenation of datasets with different sample rates. 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/4af9fe5566b3145678982d5cbfb8d8f28ddc7139), [2](https://github.com/CSC-UW/spikeinterface/commit/0ecc2cab58195167a1799c97b1cd55deffa7ff48)
  - I needed this at some point to concatenating datasets from different runs for sorting , because sampling_rate slightly changes across SpikeGLX runs. This change is currently NOT reflected in wisc_ecephys_tools (which should fail when trying to concatenate across runs). 

### Reverted changes
- Attempts to handle cases where user does not have permission to `chmod +x`? 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/26cca16f9310ffc3e93c073fe64005779f2b3c09)
  - Reversion: [1](https://github.com/CSC-UW/spikeinterface/commit/0b5987fcb58283352ccd6d7dc71cab4541f23cdf)

# SpikeInterface: a unified framework for spike sorting

<table>
<tr>
  <td>Latest Release</td>
  <td>
    <a href="https://pypi.org/project/spikeinterface/">
    <img src="https://img.shields.io/pypi/v/spikeinterface.svg" alt="latest release" />
    </a>
  </td>
</tr>
<tr>
  <td>Documentation</td>
  <td>
    <a href="https://spikeinterface.readthedocs.io/">
    <img src="https://readthedocs.org/projects/spikeinterface/badge/?version=latest" alt="latest documentation" />
    </a>
  </td>
</tr>
<tr>
  <td>License</td>
  <td>
    <a href="https://github.com/SpikeInterface/spikeinterface/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/spikeinterface.svg" alt="license" />
    </a>
</td>
</tr>
<tr>
  <td>Build Status</td>
  <td>
    <a href="https://travis-ci.org/SpikeInterface/spikeinterface">
    <img src="https://travis-ci.org/SpikeInterface/spikeinterface.svg?branch=master" alt="travis build status" />
    </a>
  </td>
</tr>
<tr>
	<td>Gitter</td>
	<td>
		<a href="https://gitter.im/SpikeInterface/community">
		<img src="https://badges.gitter.im/SpikeInterface.svg" />
	</a>
	</td>
</tr>
</table>

SpikeInterface is a Python framework designed to unify preexisting spike sorting technologies into a single code base.

With SpikeInterface, users can:

- read/write many extracellular file formats.
- pre-process extracellular recordings.
- run many popular, semi-automatic spike sorters (also in Docker/Singularity containers).
- post-process sorted datasets.
- compare and benchmark spike sorting outputs.
- compute quality metrics to validate and curate spike sorting outputs.
- visualize recordings and spike sorting outputs.
- export report and export toPhy
- offer a powerful Qt-based viewer in separate package `spikeinterface-gui <https://https://github.com/SpikeInterface/spikeinterface-gui>`_
- have some powerful sorting components to build your own sorter.



**Please have a look at the [eLife paper](https://elifesciences.org/articles/61834) that describes in detail this project**

You can also have a look at the [spikeinterface-gui](https://https://github.com/SpikeInterface/spikeinterface-gui).

## Documentation

All documentation for spikeinterface 0.93 can be found [here](https://spikeinterface.readthedocs.io/en/latest/).

Documentation of current API release 0.12.0 is [here](https://spikeinterface.readthedocs.io/en/stable/).



## How to install spikeinteface

You can install the new `spikeinterface` version with pip:

```bash
pip install spikeinterface
```

To get the latest updates, you can install `spikeinterface` from sources:

```bash
git clone https://github.com/SpikeInterface/spikeinterface.git
cd spikeinterface
python setup.py install (or develop)
cd ..
```

## Versions

`spikeinterface` version 0.90 > 0.93:

  * breaks backward compatibility with 0.10/0.11/0.12/0.13 series.
  * has been first released in July 2021 (0.90.0)
  * is not a meta-package anymore
  * it doesn't depend on spikeextractors/spiketoolkit/spikesorters/spikecomparison/spikewidgets anymore


To install the old `spikeinterface` API (version<0.90), you can use pip and point to the old version:

```bash
pip install spikeinterface==0.13
```

We strongly recommend using the new version.

## Citation

If you find SpikeInterface useful in your research, please cite:

```bibtex
@article{buccino2020spikeinterface,
  title={SpikeInterface, a unified framework for spike sorting},
  author={Buccino, Alessio Paolo and Hurwitz, Cole Lincoln and Garcia, Samuel and Magland, Jeremy and Siegle, Joshua H and Hurwitz, Roger and Hennig, Matthias H},
  journal={Elife},
  volume={9},
  pages={e61834},
  year={2020},
  publisher={eLife Sciences Publications Limited}
}
```
